/* Copyright 2021 Karlsruhe Institute of Technology
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. */

import BaseUpload from 'scripts/lib/uploads/core.js';

/** Upload provider for chunked uploads. */
export default class ChunkedUpload extends BaseUpload {
  constructor(newUploadEndpoint, getUploadsEndpoint, onSuccess, onError, onCancel, onPause) {
    super('chunked', true);

    this.newUploadEndpoint = newUploadEndpoint;
    this.getUploadsEndpoint = getUploadsEndpoint;
    this.successCallback = onSuccess;
    this.errorCallback = onError;
    this.cancelCallback = onCancel;
    this.pauseCallback = onPause;
  }

  static getTotalChunkSize(upload) {
    // eslint-disable-next-line no-param-reassign
    return upload.chunks.reduce((acc, chunk) => (chunk.state === 'active' ? acc += chunk.size : acc), 0);
  }

  static getUploadProgress(upload, additionalSize = 0) {
    // Special case for files with a size of 0.
    if (upload.size === 0) {
      return (upload.chunks.length > 0 && upload.chunks[0].state === 'active') ? 100 : 0;
    }
    return ((ChunkedUpload.getTotalChunkSize(upload) + additionalSize) / upload.size) * 100;
  }

  static findNextChunkIndex(upload) {
    let chunkIndex = null;
    for (let index = 0; index < upload.chunkCount; index++) {
      const found = upload.chunks.find((chunk) => chunk.index === index && chunk.state === 'active');

      if (!found) {
        chunkIndex = index;
        break;
      }
    }

    return chunkIndex;
  }

  static uploadChunk(upload, blob, index) {
    // The chunk and its metadata are uploaded using multipart/form-data encoding.
    const formData = new FormData();

    formData.append('blob', blob);
    formData.append('index', index);
    formData.append('size', blob.size);

    const controller = new AbortController();
    upload.controller = controller;

    const config = {
      onUploadProgress: (e) => {
        // Stop the progress from jumping around when pausing the upload.
        upload.progress = Math.max(
          ChunkedUpload.getUploadProgress(upload, Math.min(e.loaded, blob.size)),
          upload.progress,
        );
      },
      signal: controller.signal,
    };

    return axios.put(upload.uploadChunkEndpoint, formData, config)
      .then((response) => {
        upload.chunks = response.data.chunks;
        upload.progress = ChunkedUpload.getUploadProgress(upload);
      })
      .finally(() => upload.controller = null);
  }


  create(blob, name, size, storageType, origin = null, forceReplace = false) {
    const upload = super.create(blob, name, size, storageType, origin, forceReplace);

    // Storage specific upload properties.
    upload.chunks = [];
    upload.chunkCount = null;
    upload.chunkSize = null;
    upload.uploadChunkEndpoint = null;
    upload.finishUploadEndpoint = null;
    upload.deleteUploadEndpoint = null;
    upload.getStatusEndpoint = null;

    return upload;
  }

  async upload(upload) {
    // Check if the upload was already initiated. We could check any property that will be set from the backend.
    if (!upload.createdAt) {
      try {
        await this.initiateUpload(upload);
      } catch (error) {
        if (!await this.errorCallback(error, upload)) {
          return;
        }

        if (error.request.status === 409) {
          try {
            // Restart the upload using a different endpoint.
            await this.initiateUpload(upload, error.response.data.file._actions.edit_data);

            // eslint-disable-next-line require-atomic-updates
            upload.replacedFile = error.response.data.file;
          } catch (error) {
            await this.errorCallback(error, upload);
          }
        }
      }
    }

    if (!await this.uploadChunks(upload)) {
      return;
    }

    /* eslint-disable require-atomic-updates */
    upload.state = 'processing';

    try {
      await axios.post(upload.finishUploadEndpoint);
    } catch (error) {
      upload.state = 'uploading';

      if (error.request.status === 413) {
        kadi.base.flashWarning(error.response.data.description);
      } else {
        kadi.base.flashDanger($t('Error finishing upload.'), {request: error.request});
      }

      this.pauseCallback(upload);
      return;
    }

    this.finalizeUpload(upload);
    /* eslint-disable require-atomic-updates */
  }

  /* eslint-disable class-methods-use-this */
  cancel(upload) {
    if (upload.deleteUploadEndpoint) {
      return axios.delete(upload.deleteUploadEndpoint);
    }

    return Promise.resolve();
  }

  isPausable(upload) {
    return ['pending', 'uploading'].includes(upload.state);
  }

  isResumable(upload) {
    // Special case for files with a size of 0.
    if (upload.size === 0) {
      return upload.state === 'paused'
        && (upload.blob !== null || (upload.chunks.length > 0 && upload.chunks[0].state === 'active'));
    }

    return upload.state === 'paused'
      && (upload.blob !== null || ChunkedUpload.getTotalChunkSize(upload) === upload.size);
  }
  /* eslint-enable class-methods-use-this */

  initiateUpload(upload, endpoint = null) {
    let requestFunc = null;
    let _endpoint = endpoint;

    const data = {
      size: upload.size,
      storage: {storage_type: upload.storageType},
    };

    if (!_endpoint) {
      requestFunc = axios.post;
      _endpoint = this.newUploadEndpoint;
      data.name = upload.name;
    } else {
      requestFunc = axios.put;
    }

    // Initial request to initiate the upload process and to retrieve the upload infos.
    return requestFunc(_endpoint, data)
      .then((response) => {
        const data = response.data;

        upload.createdAt = data.created_at;
        upload.chunkCount = data.chunk_count;
        upload.chunkSize = data._meta.chunk_size;
        upload.uploadChunkEndpoint = data._actions.upload_chunk;
        upload.finishUploadEndpoint = data._actions.finish_upload;
        upload.deleteUploadEndpoint = data._actions.delete;
        upload.getStatusEndpoint = data._links.status;
      });
  }

  async uploadChunks(upload) {
    const errorMsg = $t('Error uploading chunk.');

    // Loop until all chunks have been uploaded successfully. Currently, the chunks are uploaded sequentially.
    while (true) {
      // Check if the upload state was modified elsewhere.
      if (upload.state !== 'uploading') {
        return false;
      }

      // Find the next chunk index to upload.
      const chunkIndex = ChunkedUpload.findNextChunkIndex(upload);

      // No index for the next chunk could be found, so we are done uploading.
      if (chunkIndex === null) {
        break;
      }

      const start = chunkIndex * upload.chunkSize;
      const end = Math.min(start + upload.chunkSize, upload.size);
      const blob = upload.blob.slice(start, end);

      let timeout = 0;

      // Loop until the current chunk was uploaded successfully or the upload cannot be completed.
      while (true) {
        // Check if the upload state was modified from outside.
        if (upload.state !== 'uploading') {
          return false;
        }

        try {
          /* eslint-disable no-await-in-loop */
          await ChunkedUpload.uploadChunk(upload, blob, chunkIndex);
          break;
        } catch (error) {
          // Check if the request was canceled.
          if (axios.isCancel(error)) {
            return false;
          }

          // There is no point in retrying when some quota was exceeded.
          if (error.request.status === 413) {
            kadi.base.flashWarning(error.response.data.description);
            this.pauseCallback(upload);
            return false;
          }

          timeout += 5_000;

          const timeoutMsg = $t('Retrying in {{timeout}} seconds.', {timeout: timeout / 1_000});
          kadi.base.flashDanger(`${errorMsg} ${timeoutMsg}`, {request: error.request, timeout});

          await kadi.utils.sleep(timeout);
          /* eslint-enable no-await-in-loop */
        }
      }
    }

    return true;
  }

  finalizeUpload(upload) {
    let timeout = 0;

    const _updateStatus = () => {
      if (timeout < 30_000) {
        timeout += 1_000;
      }

      axios.get(upload.getStatusEndpoint)
        .then((response) => {
          const data = response.data;

          if (data._meta.file) {
            // The upload finished successfully.
            upload.state = 'completed';
            upload.viewFileEndpoint = data._meta.file._links.view;

            this.successCallback(upload, data);
          } else if (data._meta.error) {
            // The upload finished with an error.
            kadi.base.flashDanger(data._meta.error);

            this.cancelCallback(true, upload);
          } else {
            // The upload is still processing.
            window.setTimeout(_updateStatus, timeout);
          }
        })
        .catch((error) => {
          kadi.base.flashDanger($t('Error updating upload status.'), {request: error.request});
        });
    };

    window.setTimeout(_updateStatus, 100);
  }

  loadUploads() {
    return axios.get(this.getUploadsEndpoint)
      .then((response) => {
        const uploads = [];

        response.data.items.forEach((uploadData) => {
          // Create a new upload based on the data.
          const upload = this.create(null, uploadData.name, uploadData.size, uploadData.storage.storage_type);

          // Set the storage specific upload properties.
          upload.chunks = uploadData.chunks;
          upload.chunkCount = uploadData.chunk_count;
          upload.chunkSize = response.data._meta.chunk_size;
          upload.uploadChunkEndpoint = uploadData._actions.upload_chunk;
          upload.finishUploadEndpoint = uploadData._actions.finish_upload;
          upload.deleteUploadEndpoint = uploadData._actions.delete;
          upload.getStatusEndpoint = uploadData._links.status;

          // Update some other properties based on the data.
          upload.state = uploadData.state;
          upload.createdAt = uploadData.created_at;
          upload.replacedFile = uploadData.file;

          upload.progress = ChunkedUpload.getUploadProgress(upload);

          if (upload.state === 'active') {
            upload.state = 'paused';
          } else if (upload.state === 'processing') {
            this.finalizeUpload(upload);
          }

          uploads.push(upload);
        });

        return uploads;
      });
  }
}
