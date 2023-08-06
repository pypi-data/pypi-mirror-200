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

/** Base class for all upload providers. */
export default class BaseUpload {
  constructor(uploadType, resumable = false) {
    this.uploadType = uploadType;
    this.resumable = resumable;
  }

  create(blob, name, size, storageType, origin = null, forceReplace = false) {
    return {
      id: kadi.utils.randomAlnum(),
      uploadType: this.uploadType,
      storageType,
      blob,
      name,
      size,
      state: 'pending',
      progress: 0,
      origin, // An identifier to distinguish where an upload originated from.
      createdAt: null,
      forceReplace, // To force replacing an existing file without warning the user.
      skipReplace: false, // To skip replacing an existing file without warning the user.
      replacedFile: null, // A reference to a file that is being replaced.
      viewFileEndpoint: null, // Endpoint to view the uploaded file.
      controller: null, // An abort controller to cancel ongoing requests.
    };
  }

  /* eslint-disable no-unused-vars */
  // eslint-disable-next-line require-await
  async upload(upload) {
    throw new Error(`Not implemented for upload type '${this.uploadType}'.`);
  }

  cancel(upload) {
    throw new Error(`Not implemented for upload type '${this.uploadType}'.`);
  }

  isPausable(upload) {
    if (this.resumable) {
      throw new Error(`Not implemented for upload type '${this.uploadType}'.`);
    }
    return false;
  }

  isResumable(upload) {
    if (this.resumable) {
      throw new Error(`Not implemented for upload type '${this.uploadType}'.`);
    }
    return false;
  }
  /* eslint-enable no-unused-vars */
}
