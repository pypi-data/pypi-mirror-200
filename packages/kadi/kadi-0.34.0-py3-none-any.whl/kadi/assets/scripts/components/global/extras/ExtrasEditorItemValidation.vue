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
  <div class="card mt-1 mr-2">
    <div class="form-row align-items-center my-2 mx-1">
      <div class="col-md-2 text-muted mb-2 mb-md-0">{{ $t('Required') }}</div>
      <div class="col-md-10">
        <input type="checkbox" class="align-middle" v-model="required">
      </div>
    </div>
    <div class="form-row align-items-center my-2 mx-1" v-if="['str', 'int', 'float'].includes(type)">
      <div class="col-md-2 text-muted mb-2 mb-md-0">{{ $t('Options') }}</div>
      <div class="col-md-10">
        <vue-draggable handle=".sort-handle" :list="options" :force-fallback="true" @end="endDrag">
          <div class="form-row my-1" :key="option.id" v-for="(option, index) in options">
            <div class="col-md-10 mb-1 mb-md-0">
              <input class="form-control form-control-sm"
                     :value="option.value"
                     @change="changeOption(option, $event.target.value)">
            </div>
            <div class="col-md-2 btn-group btn-group-sm">
              <button type="button" class="btn btn-light" tabindex="-1" @click="addOption(null, index)">
                <i class="fa-solid fa-plus"></i>
              </button>
              <button type="button"
                      class="btn btn-light"
                      tabindex="-1"
                      @click="removeOption(index)"
                      v-if="options.length > 1">
                <i class="fa-solid fa-xmark"></i>
              </button>
              <span class="btn btn-sm btn-light disabled sort-handle" tabindex="-1">
                <i class="fa-solid fa-bars"></i>
              </span>
            </div>
          </div>
        </vue-draggable>
      </div>
    </div>
    <div class="form-row align-items-center my-2 mx-1" v-if="['int', 'float'].includes(type)">
      <div class="col-md-2 text-muted mb-2 mb-md-0">{{ $t('Range') }}</div>
      <div class="col-md-10">
        <div class="d-flex justify-content-between">
          <div class="input-group input-group-sm mr-1">
            <div class="input-group-prepend cursor-default">
              <span class="input-group-text">&ge;</span>
            </div>
            <input class="form-control" :value="range.min" @change="changeRange('min', $event.target.value)">
          </div>
          <div class="input-group input-group-sm ml-1">
            <div class="input-group-prepend cursor-default">
              <span class="input-group-text">&le;</span>
            </div>
            <input class="form-control" :value="range.max" @change="changeRange('max', $event.target.value)">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.sort-handle {
  cursor: pointer;

  &:hover {
    background-color: white;
  }
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
      initialized: false,
      required: false,
      options: [],
      range: {
        min: null,
        max: null,
      },
    };
  },
  props: {
    type: String,
    convertValue: Function,
    initialValidation: {
      type: Object,
      default: () => ({}),
    },
  },
  watch: {
    type() {
      for (const option of this.options) {
        this.changeOption(option, option.value, false);
      }
      for (const prop of ['min', 'max']) {
        this.changeRange(prop, this.range[prop], false);
      }

      this.updateValidation();
    },
    required() {
      this.updateValidation();
    },
  },
  methods: {
    updateValidation() {
      if (!this.initialized) {
        return;
      }

      if (kadi.utils.isNestedType(this.type)) {
        this.$emit('validate', null);
        return;
      }

      const validation = {
        required: this.required,
      };

      if (['str', 'int', 'float'].includes(this.type)) {
        validation.options = [];

        for (const option of this.options) {
          if (option.value !== null) {
            validation.options.push(option.value);
          }
        }
      }

      if (['int', 'float'].includes(this.type)) {
        validation.range = {min: this.range.min, max: this.range.max};
      }

      this.$emit('validate', validation);
    },
    addOption(option = null, index = null) {
      const newOption = {
        id: kadi.utils.randomAlnum(),
        value: this.convertValue(option),
      };

      if (index !== null) {
        this.options.splice(index + 1, 0, newOption);
      } else {
        this.options.push(newOption);
      }
    },
    removeOption(index) {
      const option = this.options.splice(index, 1)[0];

      if (option.value !== null) {
        this.updateValidation();
      }
    },
    changeOption(option, value, updateValidation = true) {
      const prevValue = option.value;
      // Set the value to the given value as is first, as otherwise the view is not updated correctly if the converted
      // value ('newValue') is the same as before.
      option.value = value;

      let newValue = this.convertValue(value);

      // Check if this option already exists and reset the new value if so.
      const index = this.options.findIndex((o) => o.value === newValue && o.id !== option.id);

      if (index !== -1) {
        newValue = null;
      }

      option.value = newValue;

      if (updateValidation && prevValue !== newValue) {
        this.updateValidation();
      }
    },
    changeRange(prop, value, updateValidation = true) {
      const prevValue = this.range[prop];
      // See comment in 'changeOption'.
      this.range[prop] = value;

      const newValue = this.convertValue(value);
      this.range[prop] = newValue;

      if (updateValidation && prevValue !== newValue) {
        this.updateValidation();
      }
    },
    endDrag(e) {
      if (e.oldIndex !== e.newIndex) {
        this.updateValidation();
      }
    },
  },
  mounted() {
    this.addOption();

    // This initialization is enough, since the whole component is re-rendered anyways when e.g. using the undo/redo
    // functionality.
    if (this.initialValidation) {
      this.required = this.initialValidation.required || false;

      const options = this.initialValidation.options;

      if (options && options.length > 0) {
        this.removeOption(0);

        for (const option of this.initialValidation.options) {
          this.addOption(option);
        }
      }

      const range = this.initialValidation.range;

      if (range) {
        for (const prop of ['min', 'max']) {
          this.range[prop] = range[prop];
        }
      }
    }

    // Skip first potential change.
    this.$nextTick(() => this.initialized = true);
  },
};
</script>
