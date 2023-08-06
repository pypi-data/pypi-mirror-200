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
  <div class="form-group">
    <label class="form-control-label">{{ field.label }}</label>
    <div class="card">
      <div class="card-body p-2">
        <vue-draggable handle=".sort-handle" :list="currentLayout" :force-fallback="true">
          <div class="border rounded p-2"
               :class="{'mb-2': index < currentLayout.length - 1}"
               v-for="(resourceConfig, index) in currentLayout"
               :key="resourceConfig.resource">
            <div class="sort-handle pb-2">
              <i class="fa-solid fa-bars"></i>
              <strong>{{ resourceTypes[resourceConfig.resource] }}</strong>
            </div>
            <div class="form-row">
              <div class="col-md-4 mb-2 mb-md-0">
                {{ $t('Visibility') }}
                <select class="custom-select custom-select-sm" v-model="resourceConfig.visibility">
                  <option v-for="visibility in visibilityTypes" :key="visibility.key" :value="visibility.key">
                    {{ visibility.title }}
                  </option>
                </select>
              </div>
              <div class="col-md-4 mb-2 mb-md-0">
                {{ $t('Creator') }}
                <select class="custom-select custom-select-sm" v-model="resourceConfig.creator">
                  <option v-for="creator in creatorTypes" :key="creator.key" :value="creator.key">
                    {{ creator.title }}
                  </option>
                </select>
              </div>
              <div class="col-md-4">
                {{ $t('Maximum amount of items:') }} {{ resourceConfig.max_items }}
                <range-slider class="pt-1"
                              :max="10"
                              :step="2"
                              :initial-value="resourceConfig.max_items"
                              @input="resourceConfig.max_items = $event">
                </range-slider>
              </div>
            </div>
          </div>
        </vue-draggable>
      </div>
    </div>
    <small class="form-text text-muted">{{ field.description }}</small>
    <input type="hidden" :name="field.name" :value="serializedLayout">
  </div>
</template>

<style scoped>
.sort-handle {
  cursor: pointer;
}
</style>

<script>
import VueDraggable from 'vuedraggable';

export default {
  components: {
    VueDraggable,
  },
  data() {
    return {
      resourceTypes: {
        record: $t('Records'),
        collection: $t('Collections'),
        template: $t('Templates'),
        group: $t('Groups'),
      },
      visibilityTypes: [
        {key: 'all', title: $t('All')},
        {key: 'private', title: $t('Private')},
        {key: 'public', title: $t('Public')},
      ],
      creatorTypes: [
        {key: 'any', title: $t('Any')},
        {key: 'self', title: $t('Self')},
      ],
      defaultResourceOrder: ['record', 'collection', 'template', 'group'],
      defaultResourceConfig: {creator: 'any', visibility: 'all', max_items: 0},
      currentLayout: [],
    };
  },
  props: {
    field: Object,
  },
  computed: {
    serializedLayout() {
      return JSON.stringify(this.currentLayout);
    },
  },
  mounted() {
    // Determine the initial layout settings based on the field data and the default resource config.
    const currentResourceTypes = [];

    for (const resourceConfig of this.field.data) {
      if (!currentResourceTypes.includes(resourceConfig.resource)) {
        this.currentLayout.push(resourceConfig);
        currentResourceTypes.push(resourceConfig.resource);
      }
    }
    for (const resourceType of this.defaultResourceOrder) {
      if (!currentResourceTypes.includes(resourceType)) {
        this.currentLayout.push({resource: resourceType, ...this.defaultResourceConfig});
      }
    }
  },
};
</script>
