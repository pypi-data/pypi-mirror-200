<!-- Copyright 2023 Karlsruhe Institute of Technology
   -
   - Licensed under the Apache License, Version 2.0 (the "License");
   - you may not use this file except in compliance with the License.
   - You may obtain a copy of the License at
   -
   -     http://www.apache.org/licenses/LICENSE-2.0
   -
   - Unless required by applicable law or agreed to in writing, software
   - distributed under the License is distributed on an "AS IS" BASIS,
   - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   - See the License for the specific language governing permissions and
   - limitations under the License. -->

<template>
  <div class="card bg-light">
    <div class="card-header py-2" v-if="currentSearch">
      <div class="form-row d-flex align-items-center" v-if="!editing">
        <div class="col-8">
          <tooltip-item :title="$t('Unsaved changes')" v-if="unsavedChanges">
            <i class="fa-solid fa-triangle-exclamation"></i>
          </tooltip-item>
          {{ $t('Current search:') }}
          <strong>{{ currentSearch.name }}</strong>
        </div>
        <div class="col-4 d-flex justify-content-end">
          <div class="btn-group btn-group-sm">
            <button class="btn btn-light fixed-btn" :title="$t('Edit search')" @click="startEditing">
              <i class="fa-solid fa-pencil"></i>
            </button>
            <button class="btn btn-danger fixed-btn" :title="$t('Remove search')" @click="removeSearch">
              <i class="fa-solid fa-trash"></i>
            </button>
          </div>
        </div>
      </div>
      <div class="input-group input-group-sm" v-else>
        <input class="form-control" v-model.trim="editSearchName">
        <div class="input-group-append">
          <button class="btn btn-light fixed-btn" :title="$t('Cancel')" @click="finishEditing">
            <i class="fa-solid fa-xmark"></i>
          </button>
          <button class="btn btn-light fixed-btn" :title="$t('Save')" :disabled="!editSearchName" @click="editSearch">
            <i class="fa-solid fa-check"></i>
          </button>
        </div>
      </div>
    </div>
    <div class="card-body py-3">
      <div class="form-row" v-if="!saving">
        <div class="col-9">
          <dynamic-selection container-classes="select2-single-sm"
                             :endpoint="selectEndpoint"
                             :request-params="{object: objectType}"
                             :placeholder="$t('Select a saved search')"
                             :reset-on-select="true"
                             @select="loadSearch($event.id)">
          </dynamic-selection>
        </div>
        <div class="col-3">
          <button class="btn btn-sm btn-block btn-light" :title="$t('New search')" @click="saving = true">
            <i class="fa-solid fa-plus"></i>
          </button>
        </div>
      </div>
      <div class="input-group input-group-sm" v-else>
        <input class="form-control" :placeholder="$t('Name')" v-model.trim="newSearchName">
        <div class="input-group-append">
          <button class="btn btn-light fixed-btn" :title="$t('Cancel')" @click="finishSaving">
            <i class="fa-solid fa-xmark"></i>
          </button>
          <button class="btn btn-light fixed-btn" :title="$t('Save')" :disabled="!newSearchName" @click="saveSearch">
            <i class="fa-solid fa-check"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fixed-btn {
  width: 35px;
}
</style>

<script>
export default {
  data() {
    return {
      currentSearch: null,
      unsavedChanges: false,
      newSearchName: '',
      editSearchName: '',
      saving: false,
      editing: false,
      deleting: false,
    };
  },
  props: {
    objectType: String,
    selectEndpoint: String,
    createEndpoint: String,
    loadBaseEndpoint: String,
    savedSearchParam: {
      type: String,
      default: 'saved_search',
    },
    ignoredParams: {
      type: Array,
      default: () => ['page'],
    },
  },
  watch: {
    currentSearch() {
      let url = null;

      if (this.currentSearch) {
        url = kadi.utils.setSearchParam(this.savedSearchParam, this.currentSearch.id);
      } else {
        url = kadi.utils.removeSearchParam(this.savedSearchParam);
      }

      kadi.utils.replaceState(url);
    },
  },
  methods: {
    onReplaceState() {
      if (this.currentSearch) {
        this.unsavedChanges = this.currentSearch.query_string !== this.getQueryString();
      } else {
        this.unsavedChanges = false;
      }
    },
    getQueryString() {
      const searchParams = new URLSearchParams(new URL(window.location).search);
      const ignoredParams = [...this.ignoredParams, this.savedSearchParam];

      for (const param of ignoredParams) {
        searchParams.delete(param);
      }

      return searchParams.toString();
    },
    finishSaving() {
      this.saving = false;
      this.newSearchName = '';
    },
    startEditing() {
      this.editing = true;
      this.editSearchName = this.currentSearch.name;
    },
    finishEditing() {
      this.editing = false;
      this.editSearchName = '';
    },
    saveSearch() {
      const data = {
        name: this.newSearchName,
        object: this.objectType,
        query_string: this.getQueryString(),
      };

      axios.post(this.createEndpoint, data)
        .then((response) => {
          this.currentSearch = response.data;
          kadi.base.flashSuccess($t('Search saved successfully.'));
        })
        .catch((error) => kadi.base.flashDanger($t('Error saving search.'), {request: error.request}))
        .finally(() => this.finishSaving());
    },
    editSearch() {
      const queryString = this.getQueryString();

      // Check if there is anything to actually save.
      if (this.editSearchName === this.currentSearch.name && queryString === this.currentSearch.query_string) {
        this.finishEditing();
        return;
      }

      const data = {
        name: this.editSearchName,
        query_string: queryString,
      };

      axios.patch(this.currentSearch._actions.edit, data)
        .then((response) => {
          this.currentSearch = response.data;
          kadi.base.flashSuccess($t('Search updated successfully.'));
        })
        .catch((error) => kadi.base.flashDanger($t('Error updating search.'), {request: error.request}))
        .finally(() => this.finishEditing());
    },
    removeSearch() {
      if (!window.confirm($t('Are you sure you want to remove this search?'))) {
        return;
      }

      this.deleting = true;

      axios.delete(this.currentSearch._actions.remove)
        .then(() => {
          this.currentSearch = null;
          kadi.base.flashSuccess($t('Search deleted successfully.'));
        })
        .catch((error) => kadi.base.flashDanger($t('Error removing search.'), {request: error.request}))
        .finally(() => this.deleting = false);
    },
    loadSearch(id, refreshPage = true) {
      const errorMsg = $t('Error loading saved search.');

      axios.get(`${this.loadBaseEndpoint}/${id}`)
        .then((response) => {
          const data = response.data;

          if (data.object !== this.objectType) {
            kadi.base.flashDanger(errorMsg);
          } else {
            if (refreshPage) {
              window.location.href = data._links.view;
            } else {
              this.currentSearch = data;
            }
          }
        })
        .catch((error) => kadi.base.flashDanger(errorMsg, {request: error.request}));
    },
  },
  mounted() {
    window.addEventListener('replacestate', this.onReplaceState);

    const id = kadi.utils.getSearchParam(this.savedSearchParam);

    if (id) {
      this.loadSearch(id, false);
    }
  },
  beforeDestroy() {
    window.removeEventListener('replacestate', this.onReplaceState);
  },
};
</script>
