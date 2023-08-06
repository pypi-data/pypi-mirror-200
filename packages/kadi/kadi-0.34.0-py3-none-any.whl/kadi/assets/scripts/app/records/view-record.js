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

import DashboardViewer from 'scripts/components/local/dashboard/DashboardViewer.vue';
import RecordLinksGraph from 'scripts/components/local/RecordLinksGraph.vue';

kadi.base.newVue({
  components: {
    DashboardViewer,
    RecordLinksGraph,
  },
  data: {
    currentTab: null,
    sortFiles: '-last_modified',
    sortFileOptions: [
      ['-last_modified', $t('Last modified (newest first)')],
      ['last_modified', $t('Last modified (oldest first)')],
      ['name', $t('Name (ascending)')],
      ['-name', $t('Name (descending)')],
      ['size', $t('Size (ascending)')],
      ['-size', $t('Size (descending)')],
    ],
    renderLinksGraph: false,
    visualizeLinks: false,
    visualizeLinksParam: 'visualize',
    linkDepth: 1,
    linkDepthParam: 'depth',
    linkDirection: '',
    linkFilter: '',
  },
  watch: {
    visualizeLinks() {
      if (this.visualizeLinks) {
        // If we render the links graph component before it is shown, its size cannot be initialized correctly.
        this.renderLinksGraph = true;
      }

      const url = kadi.utils.setSearchParam(this.visualizeLinksParam, this.visualizeLinks);
      kadi.utils.replaceState(url);
    },
    linkDepth() {
      const url = kadi.utils.setSearchParam(this.linkDepthParam, this.linkDepth);
      kadi.utils.replaceState(url);
    },
  },
  methods: {
    changeTab(tab) {
      this.currentTab = tab;

      let url = null;

      for (const [param, value] of [
        [this.visualizeLinksParam, this.visualizeLinks],
        [this.linkDepthParam, this.linkDepth],
      ]) {
        if (this.currentTab === 'links') {
          url = kadi.utils.setSearchParam(param, value);
        } else {
          url = kadi.utils.removeSearchParam(param);
        }

        kadi.utils.replaceState(url);
      }
    },
    deleteFile(file) {
      if (!window.confirm($t('Are you sure you want to delete this file?'))) {
        return;
      }

      this.$set(file, 'disabled', true);

      axios.delete(file._actions.delete)
        .then(() => {
          this.$refs.filesPagination.update();
          // Update the file revisions as well if they were loaded already.
          if (this.$refs.fileRevisionsPagination) {
            this.$refs.fileRevisionsPagination.update();
          }
          kadi.base.flashSuccess($t('File deleted successfully.'), {scrollTo: false});
        })
        .catch((error) => {
          kadi.base.flashDanger($t('Error deleting file.'), {request: error.request});
          file.disabled = false;
        });
    },
    updateLinkDepth(depth) {
      this.linkDepth = depth;
    },
  },
  created() {
    const visualizeLinks = kadi.utils.getSearchParam(this.visualizeLinksParam);
    if (visualizeLinks === 'true') {
      this.visualizeLinks = true;
    }

    const linkDepth = kadi.utils.getSearchParam(this.linkDepthParam);
    if (linkDepth) {
      this.linkDepth = Number.parseInt(linkDepth, 10) || 1;
    }
  },
  mounted() {
    const record = kadi.context.record;
    kadi.base.visitItem('record', record.title, record.identifier, `/records/${record.id}`);
  },
});
