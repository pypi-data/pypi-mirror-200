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
  <div>
    <div :class="{'mt-2': nestedType && extras.length > 0}">
      <vue-draggable handle=".sort-handle"
                     scroll-sensitivity="100"
                     scroll-speed="15"
                     :list="extras"
                     :group="{name: 'extras'}"
                     :force-fallback="true"
                     :empty-insert-threshold="35"
                     @start="startDrag"
                     @end="endDrag">
        <div v-for="(extra, index) in extras" :key="extra.id">
          <extras-editor-item :extra="extra"
                              :index="index"
                              :show-validation="showValidation"
                              :template-endpoint="templateEndpoint"
                              :nested-type="nestedType"
                              :depth="depth"
                              @add-extra="addExtra(null, index, true)"
                              @remove-extra="removeExtra(extra)"
                              @duplicate-extra="duplicateExtra(extra)"
                              @init-nested-value="initNestedValue(extra, $event)"
                              @save-checkpoint="$emit('save-checkpoint')">
          </extras-editor-item>
        </div>
      </vue-draggable>
    </div>
    <div class="form-row align-items-center mr-0">
      <div class="col-xl-3">
        <button type="button"
                class="btn btn-sm btn-link text-primary p-0"
                tabindex="-1"
                @click="addExtra(null, null, true)">
          <i class="fa-solid fa-plus mr-1"></i> {{ $t('Add extra') }}
        </button>
      </div>
      <div class="col-xl-9">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<!-- eslint-disable vue/no-mutating-props -->
<script>
import VueDraggable from 'vuedraggable';

export default {
  components: {
    VueDraggable,
  },
  props: {
    extras: Array,
    showValidation: Boolean,
    templateEndpoint: String,
    // Can also be used to detect whether we are in a nested context at all.
    nestedType: {
      type: String,
      default: null,
    },
    depth: {
      type: Number,
      default: 0,
    },
  },
  methods: {
    newExtra(extraToCopy = null, copyErrors = true, copyValues = true) {
      const extra = {
        // To prevent issues when reordering extras, using undo/redo, etc.
        id: kadi.utils.randomAlnum(),
        isDragging: false,
        editTerm: false,
        editValidation: false,
        type: {value: 'str', errors: []},
        key: {value: null, errors: []},
        value: {value: null, errors: []},
        unit: {value: null, errors: []},
        term: {value: null, errors: []},
        validation: {value: null, errors: []},
      };

      // Always perform a deep copy if an extra is to be copied.
      if (extraToCopy) {
        extra.editTerm = extraToCopy.editTerm || false;
        extra.editValidation = extraToCopy.editValidation || false;

        // Assume the extra is formatted as formdata if the type (which should always exist) is an object.
        const isFormdata = kadi.utils.isObject(extraToCopy.type);

        // Copy all properties completely except for the value, since it might be nested.
        for (const prop of ['type', 'key', 'value', 'unit', 'term', 'validation']) {
          if (extraToCopy[prop]) {
            if (prop !== 'value') {
              const value = isFormdata ? extraToCopy[prop].value : extraToCopy[prop];
              extra[prop].value = kadi.utils.deepClone(value);
            }

            if (isFormdata && copyErrors) {
              extra[prop].errors = extraToCopy[prop].errors.slice();
            }
          }
        }

        // Copy the value (recursively, in case it is nested).
        const value = isFormdata ? extraToCopy.value.value : extraToCopy.value;

        if (kadi.utils.isNestedType(extra.type.value)) {
          extra.value.value = [];
          value.forEach((nestedExtra) => extra.value.value.push(this.newExtra(nestedExtra, copyErrors, copyValues)));
        } else if (copyValues) {
          extra.value.value = value;
        }
      }

      return extra;
    },
    addExtra(extra = null, index = null, focus = false, createCheckpoint = true) {
      let newExtra = null;

      // If no extra to copy is given and we are inside a list with at least one extra, copy the structure of the last
      // extra, without values.
      if (extra === null && this.nestedType === 'list' && this.extras.length > 0) {
        newExtra = this.newExtra(this.extras[this.extras.length - 1], true, false);
      } else {
        newExtra = this.newExtra(extra);
      }

      if (index !== null) {
        this.extras.splice(index + 1, 0, newExtra);
      } else {
        this.extras.push(newExtra);
      }

      if (focus) {
        this.$nextTick(() => this.focusExtra(newExtra));
      }

      if (createCheckpoint) {
        this.$emit('save-checkpoint');
      }

      return newExtra;
    },
    addExtras(extras, createCheckpoint = true) {
      extras.forEach((extra) => this.addExtra(extra, null, false, false));

      if (createCheckpoint) {
        this.$emit('save-checkpoint');
      }
    },
    removeExtra(extra, createCheckpoint = true) {
      kadi.utils.removeFromArray(this.extras, extra);

      if (createCheckpoint) {
        this.$emit('save-checkpoint');
      }
    },
    removeExtras(createCheckpoint = true) {
      this.extras.length = 0;

      if (createCheckpoint) {
        this.$emit('save-checkpoint');
      }
    },
    duplicateExtra(extra) {
      const index = this.extras.indexOf(extra);
      const copy = this.newExtra(extra, false);
      this.extras.splice(index + 1, 0, copy);
      this.$emit('save-checkpoint');
    },
    focusExtra(extra) {
      this.$nextTick(() => {
        extra.input.focus();
        kadi.utils.scrollIntoView(extra.input);
      });
    },
    initNestedValue(extra, templateEndpoint = null) {
      if (templateEndpoint === null) {
        extra.value.value = [this.newExtra()];
      } else {
        this.loadTemplate(templateEndpoint).then((extras) => {
          const newExtras = [];
          for (const _extra of extras) {
            newExtras.push(this.newExtra(_extra));
          }
          extra.value.value = newExtras;

          this.$emit('save-checkpoint');
        });
      }
    },
    loadTemplate(endpoint) {
      return axios.get(endpoint)
        .then((response) => {
          return response.data.data;
        })
        .catch((error) => {
          kadi.base.flashDanger($t('Error loading template.'), {request: error.request});
        });
    },
    startDrag(e) {
      const extra = e.item._underlying_vm_;
      extra.isDragging = true;
    },
    endDrag(e) {
      const extra = e.item._underlying_vm_;
      extra.isDragging = false;

      if (e.from !== e.to || e.oldIndex !== e.newIndex) {
        this.$emit('save-checkpoint');
      }
    },
  },
};
</script>
