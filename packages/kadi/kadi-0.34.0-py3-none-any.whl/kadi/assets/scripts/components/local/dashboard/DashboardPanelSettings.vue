<!-- Copyright 2022 Karlsruhe Institute of Technology
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
  <div ref="modalDialog"
       class="modal fade"
       id="dashboard-panel-settings-modal"
       tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            {{ $t('Edit dashboard panel') }}
          </h5>
          <button type="button" class="close" data-dismiss="modal">
            <span>
              <i class="fa-solid fa-xmark fa-xs"></i>
            </span>
          </button>
        </div>
        <div class="modal-body">
          <div v-if="panel_">
            <form>
              <div class="form-group">
                <label>{{ $t('Title') }}</label>
                <input class="form-control" v-model="panel_.title">
              </div>
              <div class="form-group">
                <label>{{ $t('Subtitle') }}</label>
                <input class="form-control" v-model="panel_.subtitle">
              </div>
            </form>

            <div v-if="panel_.settingsComponent">
              <hr>
              <component :is="panel_.settingsComponent"
                         :id="panel_.i"
                         :settings="panel_.settings"
                         :endpoints="endpoints"
                         :settings-dialog-selector="settingsDialogSelector"
                         @settings-updated="onSettingsUpdated">
              </component>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button"
                  class="btn btn-primary"
                  data-dismiss="modal"
                  @click="$emit('panel-updated', panel_)">
            {{ $t('Apply') }}
          </button>
          <button type="button" class="btn btn-secondary" data-dismiss="modal">
            {{ $t('Close') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DashboardMarkdownSettings from './DashboardMarkdownSettings.vue';

export default {
  components: {
    DashboardMarkdownSettings,
  },
  data() {
    return {
      panel_: {},
      settingsDialogSelector: '',
    };
  },
  props: {
    panel: Object,
    endpoints: Object,
  },
  watch: {
    panel() {
      this.panel_ = kadi.utils.deepClone(this.panel);
    },
  },
  methods: {
    show() {
      $(this.$refs.modalDialog).modal('show');
    },
    onSettingsUpdated(newSettings) {
      this.panel_.settings = newSettings;
    },
  },
  mounted() {
    this.settingsDialogSelector = `#${this.$refs.modalDialog.id}`;
  },
};
</script>
