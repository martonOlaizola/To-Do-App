<template>
  <div class="w-full">
    <label
      :for="id"
      :class="[
        'flex items-center gap-1 text-xs font-medium mb-1',
        colorTextLabel || 'text-black'
      ]"
    >
      {{ label }}
    </label>
    <div class="relative">
      <input
        v-bind="$attrs"
        :type="type"
        :id="id"
        :placeholder="placeholder"
        :value="modelValue"
        :disabled="disabled"
        :class="[
          'main-input w-full px-3 py-[6px] border rounded text-sm focus:outline-none transition-colors',
          'focus:ring-2 focus:ring-blue-400',
          errorToShow ? 'border-red-500' : 'border-gray-300',
          disabled ? 'bg-gray-100 text-gray-500 cursor-not-allowed' : 'bg-white text-gray-800'
        ]"
        ref="inputRef"
        @input="$emit('update:modelValue', $event.target.value)"
        @blur="touched = true"
      />
      <slot name="icon" />
    </div>
    <p v-if="errorToShow" class="text-red-500 text-xs mt-1">
      {{ errorToShow }}
    </p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

defineOptions({ inheritAttrs: false })

const props = defineProps({
  colorTextLabel : String,
  label: String,
  id: String,
  placeholder: String,
  info: String,
  type: {
    type: String,
    default: 'text'
  },
  modelValue: String,
  error: String,
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const inputRef = ref(null)
const touched = ref(false)

/**
 * Resolve the native browser validation message when available.
 * @type {import('vue').ComputedRef<string>}
 */
const nativeError = computed(() => {
  if (!inputRef.value || !touched.value) return ''
  return inputRef.value.validationMessage || ''
})

/**
 * Pick the most relevant error message to display to the user.
 * @type {import('vue').ComputedRef<string>}
 */
const errorToShow = computed(() => {
  return props.error || nativeError.value
})

defineExpose({
  /**
   * Scroll the input into view and focus it when an error is present.
   * @returns {void}
   */
  scrollToError() {
    if (errorToShow.value && inputRef.value) {
      inputRef.value.scrollIntoView({ behavior: 'smooth', block: 'center' })
      inputRef.value.focus()
    }
  }
})
</script>

<style scoped>
.main-input {
  transition: background-color 0.2s, color 0.2s, border-color 0.2s;
}
</style>
