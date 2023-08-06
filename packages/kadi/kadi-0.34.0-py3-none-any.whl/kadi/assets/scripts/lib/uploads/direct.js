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

/** Upload provider for direct uploads. */
export default class DirectUpload extends BaseUpload {
  constructor(uploadEndpoint, onSuccess, onError) {
    super('direct');

    this.uploadEndpoint = uploadEndpoint;
    this.successCallback = onSuccess;
    this.errorCallback = onError;
  }

  async upload(upload) {
    const formData = new FormData();

    // We could already set this flag based on whether the replacement should be forced, but we let the upload manager
    // handle this instead for consistency, at the potential cost of an additional request.
    formData.append('replace_file', false);
    formData.append('storage_type', upload.storageType);
    formData.append('name', upload.name);
    formData.append('size', upload.size);
    formData.append('blob', upload.blob);

    const retryUpload = await this.uploadFile(upload, formData);

    if (retryUpload) {
      formData.set('replace_file', true);
      await this.uploadFile(upload, formData);
    }
  }

  /* eslint-disable class-methods-use-this */
  // eslint-disable-next-line no-unused-vars
  cancel(upload) {
    // We have nothing storage specific to cancel here.
    return Promise.resolve();
  }

  async uploadFile(upload, formData) {
    let retryUpload = false;

    const controller = new AbortController();
    upload.controller = controller;

    const config = {
      onUploadProgress: (e) => {
        upload.progress = (e.loaded / e.total) * 100;
      },
      signal: controller.signal,
    };

    try {
      const response = await axios.post(this.uploadEndpoint, formData, config);
      const data = response.data;

      upload.state = 'completed';
      upload.createdAt = data.created_at;
      upload.viewFileEndpoint = data._links.view;

      this.successCallback(upload, data);
    } catch (error) {
      // Check if the request was canceled.
      if (axios.isCancel(error)) {
        return false;
      }

      const replaceFile = await this.errorCallback(error, upload);

      if (error.request.status === 409 && replaceFile) {
        retryUpload = true;

        // eslint-disable-next-line require-atomic-updates
        upload.replacedFile = error.response.data.file;
      }
    } finally {
      // eslint-disable-next-line require-atomic-updates
      upload.controller = null;
    }

    return retryUpload;
  }
  /* eslint-enable class-methods-use-this */
}
