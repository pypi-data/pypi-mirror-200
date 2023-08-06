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
  <div>
    <div class="form-check mb-2" v-if="['record', 'collection', 'template'].includes(resourceType)">
      <input type="checkbox" class="form-check-input" :id="`user-${suffix}`" v-model="filter.user">
      <label class="form-check-label" :for="`user-${suffix}`">{{ $t('Exclude user information') }}</label>
    </div>
    <div class="form-check mb-2" v-if="resourceType === 'collection'">
      <input type="checkbox" class="form-check-input" :id="`records-${suffix}`" v-model="filter.records">
      <label class="form-check-label" :for="`records-${suffix}`">{{ $t('Exclude records') }}</label>
    </div>
    <div class="mb-2" v-if="['record', 'collection'].includes(resourceType) && !filter.records">
      <label class="form-control-label" :for="`links-${suffix}`">{{ $t('Exclude record links') }}</label>
      <select class="custom-select custom-select-sm" :id="`links-${suffix}`" v-model="filter.links">
        <option value=""></option>
        <option value="out">{{ $t('Outgoing') }}</option>
        <option value="in">{{ $t('Incoming') }}</option>
        <option value="both">{{ $t('Both') }}</option>
      </select>
    </div>
    <div class="mb-2" v-if="resourceType === 'extras' && exportType === 'json'">
      <label class="form-control-label" :for="`format-${suffix}`">{{ $t('Extra metadata format') }}</label>
      <select class="custom-select custom-select-sm" :id="`format-${suffix}`" v-model="filter.extras_format">
        <option value="standard">{{ $t('Standard') }}</option>
        <option value="plain">{{ $t('Plain') }}</option>
      </select>
    </div>
    <div v-if="['record', 'extras', 'template'].includes(resourceType) && extras.length > 0">
      <div class="row mb-2">
        <div class="col-md-6 mb-2 mb-md-0">{{ $t('Exclude extra metadata') }}</div>
        <div class="col-md-6 d-md-flex justify-content-end" v-if="resourceType === 'record' && allowExtrasPropagation">
          <div class="form-check form-check-inline">
            <input type="checkbox" class="form-check-input" :id="`propagate-${suffix}`" v-model="filter.propagate">
            <label class="form-check-label" :for="`propagate-${suffix}`">{{ $t('Apply to linked records') }}</label>
          </div>
        </div>
      </div>
      <div class="card bg-light">
        <div class="card-body">
          <extras-selector :extras="extras" @select="filter.extras = $event"></extras-selector>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      suffix: kadi.utils.randomAlnum(), // To create unique IDs.
      filter: {
        user: false,
        records: false,
        links: '',
        extras_format: 'standard',
        extras: {},
        propagate: false,
      },
    };
  },
  props: {
    resourceType: String,
    exportType: String,
    extras: {
      type: Array,
      default: () => [],
    },
    allowExtrasPropagation: {
      type: Boolean,
      default: true,
    },
  },
  watch: {
    filter: {
      handler() {
        const filter = {};

        if (this.filter.user !== false) {
          filter.user = this.filter.user;
        }
        if (this.filter.records !== false) {
          filter.records = this.filter.records;
        }
        if (this.filter.links !== '') {
          filter.links = this.filter.links === 'both' ? true : this.filter.links;
        }
        if (this.filter.extras_format !== 'standard') {
          filter.format = this.filter.extras_format;
        }
        if (Object.keys(this.filter.extras).length > 0) {
          filter.extras = this.filter.extras;
        }
        if (this.filter.propagate) {
          filter.propagate_extras = true;
        }

        this.$emit('filter', filter);
      },
      deep: true,
    },
  },
};
</script>
