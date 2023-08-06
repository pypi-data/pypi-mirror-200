<!-- Copyright 2020 Karlsruhe Institute of Technology
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
  <dynamic-pagination :endpoint="endpoint" :placeholder="placeholder" :per-page="perPage" :enable-filter="enableFilter">
    <template #default="paginationProps">
      <p>
        <strong>{{ title }}</strong>
        <span class="badge badge-pill badge-light text-muted border border-muted">{{ paginationProps.total }}</span>
      </p>
      <card-deck :items="paginationProps.items">
        <template #default="props">
          <div class="card-body py-2">
            <a class="text-default stretched-link" :href="props.item._links.view">
              <strong>
                <em class="wb-break-all">{{ props.item.name }}</em>
              </strong>
              <hr class="my-2">
              <basic-resource-info :resource="getLinkedRecord(props.item)" :compact-layout="true"></basic-resource-info>
            </a>
          </div>
          <div class="card-footer py-1">
            <small class="text-muted">
              {{ $t('Last modified') }} <from-now :timestamp="props.item.last_modified"></from-now>
            </small>
          </div>
          <div class="card-footer elevated py-1">
            <a :href="getLinkedRecord(props.item)._links.view">
              <i class="fa-solid fa-eye"></i> {{ $t('View linked record') }}
            </a>
          </div>
        </template>
      </card-deck>
    </template>
  </dynamic-pagination>
</template>

<script>
export default {
  props: {
    title: String,
    endpoint: String,
    direction: String,
    placeholder: {
      type: String,
      default: $t('No record links.'),
    },
    perPage: {
      type: Number,
      default: 6,
    },
    enableFilter: {
      type: Boolean,
      default: true,
    },
  },
  methods: {
    getLinkedRecord(link) {
      return this.direction === 'out' ? link.record_to : link.record_from;
    },
  },
};
</script>
