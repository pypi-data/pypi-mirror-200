<!-- Copyright 2021 Karlsruhe Institute of Technology
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
  <dynamic-pagination :endpoint="endpoint"
                      :placeholder="placeholder"
                      :per-page="perPage"
                      :enable-filter="enableFilter"
                      ref="pagination">
    <template #default="props">
      <p>
        <strong>{{ title }}</strong>
        <span class="badge badge-pill badge-light text-muted border border-muted">{{ props.total }}</span>
      </p>
      <ul class="list-group" v-if="props.total > 0">
        <li class="list-group-item bg-light py-2">
          <div class="row">
            <div class="col-lg-3">{{ $t('Name') }}</div>
            <div class="col-lg-4">{{ $t('Record') }}</div>
            <div class="col-lg-3">{{ $t('Created at') }}</div>
          </div>
        </li>
        <li class="list-group-item py-1" v-for="link in props.items" :key="link.id">
          <div class="row align-items-center">
            <div class="col-lg-3 mb-2 mb-lg-0">
              <a :href="link._links.view">
                <strong>{{ link.name }}</strong>
              </a>
              <br>
              <a :href="link._links.edit">
                <small>
                  <i class="fa-solid fa-pencil"></i> {{ $t('Edit link') }}
                </small>
              </a>
            </div>
            <div class="col-lg-4 mb-2 mb-lg-0">
              <a :href="direction === 'out' ? link.record_to._links.view : link.record_from._links.view">
                <basic-resource-info :resource="direction === 'out' ? link.record_to : link.record_from"
                                     :compact-layout="true">
                </basic-resource-info>
              </a>
            </div>
            <div class="col-lg-4 mb-2 mb-lg-0">
              <local-timestamp :timestamp="link.created_at"></local-timestamp>
              <br>
              <small class="text-muted">
                (<from-now :timestamp="link.created_at"></from-now>)
              </small>
            </div>
            <div class="col-lg-1 d-lg-flex justify-content-end">
              <button type="button"
                      class="btn btn-sm btn-danger"
                      :title="$t('Remove link')"
                      :disabled="link.disabled"
                      @click="removeLink(link)">
                <i class="fa-solid fa-trash"></i>
              </button>
            </div>
          </div>
        </li>
      </ul>
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
      default: 5,
    },
    enableFilter: {
      type: Boolean,
      default: true,
    },
  },
  methods: {
    removeLink(link) {
      if (!window.confirm($t('Are you sure you want to remove this record link?'))) {
        return;
      }

      this.$set(link, 'disabled', true);

      axios.delete(link._actions.remove)
        .then(() => {
          this.$refs.pagination.update();
          kadi.base.flashSuccess($t('Record link removed successfully.'), {scrollTo: false});
        })
        .catch((error) => {
          kadi.base.flashDanger($t('Error removing record link.'), {request: error.request});
          link.disabled = false;
        });
    },
  },
};
</script>
