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

<!-- eslint-disable vue/no-mutating-props -->
<template>
  <div class="form-group d-inline-block d-md-block mb-3 extra">
    <div class="form-row mr-0" :class="{'drag': extra.isDragging}">
      <!-- Type selection, which is disabled if validation options have been specified. -->
      <div class="col-xl-2 mb-1 mb-xl-0" :class="{'mr-2 mr-xl-0': nestedType}">
        <select class="custom-select custom-select-sm"
                v-model="extra.type.value"
                :class="{'has-error': extra.type.errors.length > 0 && !extra.isDragging}"
                :disabled="hasOptions && !extra.editValidation"
                @change="changeType">
          <option value="str">String</option>
          <option value="int">Integer</option>
          <option value="float">Float</option>
          <option value="bool">Boolean</option>
          <option value="date">Date</option>
          <option value="dict">Dictionary</option>
          <option value="list">List</option>
        </select>
        <div v-show="!extra.isDragging">
          <div class="invalid-feedback" v-for="error in extra.type.errors" :key="error">{{ error }}</div>
        </div>
      </div>
      <!-- Key input, which is readonly if the current item is within a list, and term IRI toggle. -->
      <div class="col-xl-4 mb-1 mb-xl-0" :class="{'mr-2 mr-xl-0': nestedType}">
        <div class="input-group input-group-sm">
          <div class="input-group-prepend cursor-default">
            <span class="input-group-text">{{ $t('Key') }}</span>
          </div>
          <input class="form-control"
                 :value="keyModel"
                 :class="{'has-error': extra.key.errors.length > 0 && !extra.isDragging,
                          'font-weight-bold': isNestedType}"
                 :readonly="nestedType === 'list'"
                 :tabindex="nestedType === 'list' ? -1 : 0"
                 @change="changeString('key', $event.target.value)"
                 ref="key">
          <div class="input-group-append">
            <button type="button"
                    class="input-group-text btn"
                    tabindex="-1"
                    :class="{'toggle-active': extra.editTerm}"
                    :title="$t('Toggle term IRI')"
                    @click="editTerm">
              <i class="fa-solid fa-link"></i>
            </button>
          </div>
        </div>
        <div v-show="!extra.isDragging">
          <div class="invalid-feedback" v-for="error in extra.key.errors" :key="error">{{ error }}</div>
        </div>
      </div>
      <!-- Value input, depending on the type, and validation toggle for non-nested types. -->
      <div class="mb-1 mb-xl-0" :class="{'col-xl-2': showUnit, 'col-xl-4': !showUnit, 'mr-2 mr-xl-0': nestedType}">
        <div class="input-group input-group-sm">
          <div class="input-group-prepend">
            <span class="input-group-text cursor-default">
              <tooltip-item :title="valueTooltip">
                {{ $t('Value') }} <strong class="text-danger" v-if="isRequired">*</strong>
              </tooltip-item>
            </span>
          </div>
          <!-- Regular input for strings and numeric values, if no validation options have been specified. Also shown
               for nested types in readonly state if no template endpoint is supplied. -->
          <input class="form-control"
                 :value="valueModel"
                 :class="{'has-error': extra.value.errors.length > 0 && !extra.isDragging}"
                 :readonly="isNestedType"
                 :tabindex="isNestedType ? -1 : 0"
                 v-if="!hasOptions && !hasTemplateSelection && !['bool', 'date'].includes(extra.type.value)"
                 @change="changeValue($event.target.value)">
          <!-- Boolean input. -->
          <select class="custom-select"
                  :value="valueModel"
                  :class="{'has-error': extra.value.errors.length > 0 && !extra.isDragging}"
                  v-if="!hasOptions && extra.type.value === 'bool'"
                  @change="changeValue($event.target.value)">
            <option value=""></option>
            <option value="true">true</option>
            <option value="false">false</option>
          </select>
          <!-- Date input. -->
          <input type="hidden" :value="extra.value.value" v-if="extra.type.value === 'date'">
          <date-time-picker :class="{'has-error': extra.value.errors.length > 0 && !extra.isDragging}"
                            :initial-value="extra.value.value"
                            @input="changeValue"
                            v-if="extra.type.value === 'date'">
          </date-time-picker>
          <!-- Selection to be used if validation options have been specified. -->
          <select class="custom-select"
                  :value="valueModel"
                  :class="{'has-error': extra.value.errors.length > 0 && !extra.isDragging}"
                  v-if="hasOptions"
                  @change="changeValue($event.target.value)">
            <option value=""></option>
            <option :value="option" v-for="option in extra.validation.value.options" :key="option">{{ option }}</option>
          </select>
          <!-- Template input for nested types, if an endpoint is supplied. -->
          <dynamic-selection container-classes="select2-single-sm font-italic"
                             :placeholder="$t('Select a metadata template')"
                             :endpoint="templateEndpoint"
                             :reset-on-select="true"
                             @select="selectTemplate"
                             v-if="hasTemplateSelection">
          </dynamic-selection>
          <!-- Validation toggle. -->
          <div class="input-group-append" v-if="!isNestedType && showValidation">
            <button type="button"
                    class="input-group-text btn"
                    tabindex="-1"
                    :class="{'toggle-active': extra.editValidation}"
                    :title="$t('Toggle validation')"
                    @click="editValidation">
              <i class="fa-solid fa-check"></i>
            </button>
          </div>
        </div>
        <div v-show="!extra.isDragging">
          <div class="invalid-feedback" v-for="error in extra.value.errors" :key="error">{{ error }}</div>
        </div>
      </div>
      <!-- Unit input for numeric values. -->
      <div class="col-xl-2 mb-1 mb-xl-0" :class="{'mr-2 mr-xl-0': nestedType}" v-show="showUnit">
        <div class="input-group input-group-sm">
          <div class="input-group-prepend cursor-default">
            <span class="input-group-text">{{ $t('Unit') }}</span>
          </div>
          <input class="form-control"
                 :value="extra.unit.value"
                 :class="{'has-error': extra.unit.errors.length > 0 && !extra.isDragging}"
                 @change="changeString('unit', $event.target.value)">
        </div>
        <div v-show="!extra.isDragging">
          <div class="invalid-feedback" v-for="error in extra.unit.errors" :key="error">{{ error }}</div>
        </div>
      </div>
      <!-- Buttons for adding, removing or duplicating extras and sort handle. -->
      <div class="col-xl-2" :class="{'mr-2 mr-xl-0': nestedType}">
        <div class="btn-group w-100">
          <button type="button"
                  class="btn btn-sm btn-light"
                  tabindex="-1"
                  :title="`${$t('Add extra')} (${$t('Ctrl')}+I)`"
                  @click="$emit('add-extra')">
            <i class="fa-solid fa-plus"></i>
          </button>
          <button type="button"
                  class="btn btn-sm btn-light"
                  tabindex="-1"
                  :title="$t('Remove extra')"
                  @click="$emit('remove-extra')">
            <i class="fa-solid fa-xmark"></i>
          </button>
          <button type="button"
                  class="btn btn-sm btn-light"
                  tabindex="-1"
                  :title="$t('Duplicate extra')"
                  @click="$emit('duplicate-extra')">
            <i class="fa-solid fa-copy"></i>
          </button>
          <span class="btn btn-sm btn-light disabled sort-handle" tabindex="-1">
            <i class="fa-solid fa-bars"></i>
          </span>
        </div>
      </div>
    </div>
    <!-- Term IRI input. -->
    <div v-show="extra.editTerm && !extra.isDragging">
      <div class="card mt-1 mr-2" :class="{'has-error': extra.term.errors.length > 0}">
        <div class="form-row align-items-center my-2 mx-1">
          <div class="col-sm-2 text-muted mb-2 mb-sm-0">{{ $t('Term IRI') }}</div>
          <div class="col-sm-10">
            <input class="form-control form-control-sm"
                   :value="extra.term.value"
                   @change="changeString('term', $event.target.value)">
            <small class="form-text text-muted">
              {{ $t('An IRI specifying an existing term that the metadatum should represent.') }}
            </small>
          </div>
        </div>
      </div>
      <div class="invalid-feedback" v-for="error in extra.term.errors" :key="error">{{ error }}</div>
    </div>
    <!-- Validation instructions for non-nested values. -->
    <div v-show="extra.editValidation && !isNestedType && !extra.isDragging">
      <extras-editor-item-validation :class="{'has-error': extra.validation.errors.length > 0}"
                                     :type="extra.type.value"
                                     :convert-value="convertValue"
                                     :initial-validation="extra.validation.value"
                                     @validate="validate">
      </extras-editor-item-validation>
      <div class="invalid-feedback" v-for="error in extra.validation.errors" :key="error">{{ error }}</div>
    </div>
    <!-- Nested values. -->
    <div class="card mt-1 pl-3 py-2 extras"
         :class="{'even': depth % 2 == 0, 'nested': depth > 0}"
         v-show="!extra.isDragging"
         v-if="isNestedType">
      <extras-editor-items :extras="extra.value.value"
                           :show-validation="showValidation"
                           :template-endpoint="templateEndpoint"
                           :nested-type="extra.type.value"
                           :depth="depth + 1"
                           @save-checkpoint="$emit('save-checkpoint')">
      </extras-editor-items>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.extra {
  .drag {
    background-color: #dee6ed;
    border-radius: 0.5rem;
    padding: 0.5rem 0 0.5rem 0.5rem;
  }

  .sort-handle {
    cursor: pointer;

    &:hover {
      background-color: white;
    }
  }

  .toggle-active {
    background-color: #d4dddf;
  }
}

.extras {
  border-color: #d4d4d4;
  margin-right: -1px;

  @media (min-width: 1200px) {
    min-width: 750px;
  }

  &.even {
    background-color: #f2f2f2;
  }

  &.nested {
    border-bottom-right-radius: 0;
    border-top-right-radius: 0;
  }
}
</style>

<!-- eslint-disable vue/no-mutating-props -->
<script>
export default {
  data() {
    return {
      prevType: null,
    };
  },
  props: {
    extra: Object,
    index: Number,
    showValidation: Boolean,
    templateEndpoint: String,
    nestedType: String,
    depth: Number,
  },
  computed: {
    keyModel: {
      get() {
        return this.nestedType === 'list' ? `(${this.index + 1})` : this.extra.key.value;
      },
      set(value) {
        this.extra.key.value = value;
      },
    },
    valueModel() {
      return this.isNestedType ? '' : this.extra.value.value;
    },
    valueTooltip() {
      let title = '';

      if (this.hasRange) {
        const range = this.extra.validation.value.range;

        if (range.min !== null) {
          title += `\u2265 ${range.min}`;
        }
        if (range.max !== null) {
          if (range.min) {
            title += ', ';
          }
          title += `\u2264 ${range.max}`;
        }
      }

      return title;
    },
    showUnit() {
      return ['int', 'float'].includes(this.extra.type.value);
    },
    isNestedType() {
      return kadi.utils.isNestedType(this.extra.type.value);
    },
    isRequired() {
      const validation = this.extra.validation.value;
      return validation && validation.required;
    },
    hasOptions() {
      const validation = this.extra.validation.value;
      return validation && validation.options && validation.options.length > 0;
    },
    hasRange() {
      const validation = this.extra.validation.value;
      return validation && validation.range && (validation.range.min !== null || validation.range.max !== null);
    },
    hasTemplateSelection() {
      return this.templateEndpoint && this.isNestedType;
    },
  },
  watch: {
    showValidation() {
      if (!this.showValidation) {
        this.extra.editValidation = false;
      }
    },
  },
  methods: {
    clampRangeValue(value) {
      if (!this.hasRange) {
        return value;
      }

      const range = this.extra.validation.value.range;

      if (range.min !== null && this.extra.value.value < range.min) {
        return range.min;
      }
      if (range.max !== null && this.extra.value.value > range.max) {
        return range.max;
      }

      return value;
    },
    convertValue(value, applyValidation = false) {
      if (value === null) {
        return value;
      }

      let newValue = value;

      if (typeof newValue === 'string') {
        newValue = newValue.trim();
      }

      const type = this.extra.type.value;

      if (type === 'str') {
        newValue = String(newValue);
      } else if (['int', 'float'].includes(type)) {
        if (newValue) {
          if (type === 'int') {
            newValue = Number.parseInt(newValue, 10);
          } else {
            newValue = Number.parseFloat(newValue, 10);
          }

          if (window.isNaN(newValue)) {
            newValue = 0;
          }

          if (type === 'int') {
            if (newValue > Number.MAX_SAFE_INTEGER) {
              newValue = Number.MAX_SAFE_INTEGER;
            } else if (newValue < -Number.MAX_SAFE_INTEGER) {
              newValue = -Number.MAX_SAFE_INTEGER;
            }
          } else if (!window.isFinite(newValue)) {
            newValue = Number.MAX_VALUE;
          }

          if (applyValidation) {
            newValue = this.clampRangeValue(newValue);
          }
        }
      } else if (type === 'bool') {
        if (newValue === 'true') {
          newValue = true;
        } else if (newValue === 'false') {
          newValue = false;
        }
      }

      if (newValue === '') {
        newValue = null;
      }

      return newValue;
    },
    changeType() {
      this.extra.value.value = this.convertValue(this.extra.value.value, true);

      const specialInputTypes = ['bool', 'date'];
      if ((!this.isNestedType && kadi.utils.isNestedType(this.prevType))
          || specialInputTypes.includes(this.extra.type.value)
          || specialInputTypes.includes(this.prevType)) {
        this.extra.value.value = null;
      }

      if (this.isNestedType && !kadi.utils.isNestedType(this.prevType)) {
        this.$emit('init-nested-value');
      }

      this.prevType = this.extra.type.value;

      // No need to create a checkpoint here, since changing a type also triggers the "validate" function, which will
      // create the checkpoint only after possible changes in the validation based on the type have occured as well.
    },
    changeString(prop, value) {
      const oldValue = this.extra[prop].value;
      // Set the value to the given value as is first, as otherwise the view is not updated correctly if the converted
      // value ('newValue') is the same as before.
      this.extra[prop].value = value;

      let newValue = value.trim();
      if (newValue === '') {
        newValue = null;
      }

      this.extra[prop].value = newValue;

      if (oldValue !== newValue) {
        this.$emit('save-checkpoint');
      }
    },
    changeValue(value) {
      const oldValue = this.extra.value.value;
      // See comment in 'changeString'.
      this.extra.value.value = value;

      const newValue = this.convertValue(value, true);
      this.extra.value.value = newValue;

      if (oldValue !== newValue) {
        this.$emit('save-checkpoint');
      }
    },
    validate(validation) {
      this.extra.validation.value = validation;

      // Apply the validation to the current value, if applicable.
      if (this.extra.value.value) {
        if (this.hasOptions) {
          const options = this.extra.validation.value.options;

          if (!options.includes(this.extra.value.value)) {
            this.extra.value.value = null;
          }
        }

        this.extra.value.value = this.clampRangeValue(this.extra.value.value);
      }

      this.$emit('save-checkpoint');
    },
    selectTemplate(template) {
      this.$emit('init-nested-value', template.endpoint);
    },
    editTerm() {
      this.extra.editValidation = false;
      this.extra.editTerm = !this.extra.editTerm;
    },
    editValidation() {
      this.extra.editTerm = false;
      this.extra.editValidation = !this.extra.editValidation;
    },
    keydownHandler(e) {
      if (e.ctrlKey && e.key === 'i') {
        e.preventDefault();
        e.stopPropagation();

        this.$emit('add-extra');
      }
    },
  },
  mounted() {
    this.extra.input = this.$refs.key;
    this.prevType = this.extra.type.value;

    if (this.extra.term.errors.length > 0) {
      this.extra.editTerm = true;
    }
    if (this.extra.validation.errors.length > 0) {
      this.extra.editValidation = true;
    }

    this.$el.addEventListener('keydown', this.keydownHandler);
  },
  beforeDestroy() {
    this.$el.removeEventListener('keydown', this.keydownHandler);
  },
};
</script>
