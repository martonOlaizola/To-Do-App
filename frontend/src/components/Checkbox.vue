<template>
  <label
    :for="inputId"
    class="inline-flex items-start gap-2 cursor-pointer select-none"
  >
    <span class="relative flex items-center justify-center">
      <input
        ref="inputRef"
        :id="inputId"
        type="checkbox"
        class="peer sr-only"
        :name="name"
        :value="value"
        :checked="isChecked"
        :disabled="disabled"
        @change="handleChange"
      />
      <span
        class="flex h-5 w-5 items-center justify-center rounded border border-gray-300 bg-white transition
              peer-focus-visible:outline peer-focus-visible:outline-2 peer-focus-visible:outline-offset-2 peer-focus-visible:outline-indigo-500
              peer-checked:border-indigo-500 peer-checked:bg-white
              peer-disabled:cursor-not-allowed peer-disabled:border-gray-200 peer-disabled:bg-gray-100"
      >
        <i v-if="!isIndeterminate && isChecked" class="fa-regular fa-square-check"></i>
        <span
          v-else-if="isIndeterminate"
          class="h-1 w-3 rounded bg-white"
        />
      </span>
    </span>

    <span class="flex flex-col leading-tight text-gray-800 peer-disabled:text-gray-400">
      <span v-if="label" class="font-medium">{{ label }}</span>
      <span v-if="description" class="text-sm text-gray-500">{{ description }}</span>
    </span>
  </label>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue"

const props = defineProps({
  modelValue: {
    type: [Boolean, Array],
    default: false,
  },
  value: {
    type: [String, Number, Boolean, Object],
    default: true,
  },
  label: {
    type: String,
    default: "",
  },
  description: {
    type: String,
    default: "",
  },
  indeterminate: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  id: {
    type: String,
    default: null,
  },
  name: {
    type: String,
    default: null,
  },
})

const emit = defineEmits(["update:modelValue", "change"])

const inputRef = ref(null)
/**
 * Computed identifier used to associate the label and the input element.
 * @type {import('vue').ComputedRef<string>}
 */
const inputId = computed(
  () => props.id ?? `checkbox-${Math.random().toString(36).slice(2, 9)}`
)

/**
 * Normalize any truthy value representation into a boolean.
 * @param {unknown} value - Value provided through v-model or manual binding.
 * @returns {boolean} True when the value should be considered checked.
 */
const normalizeBoolean = value => {
  if (typeof value === "string") {
    const normalized = value.trim().toLowerCase()
    if (["true", "1", "yes", "si"].includes(normalized)) {
      return true
    }
    if (["false", "0", "no"].includes(normalized)) {
      return false
    }
  }
  return Boolean(value)
}

/**
 * Determine whether the checkbox should be rendered as checked.
 * @type {import('vue').ComputedRef<boolean>}
 */
const isChecked = computed(() => {
  if (Array.isArray(props.modelValue)) {
    return props.modelValue.includes(props.value)
  }
  return normalizeBoolean(props.modelValue)
})

/**
 * Flag that reflects the visual indeterminate state.
 * @type {import('vue').ComputedRef<boolean>}
 */
const isIndeterminate = computed(() => props.indeterminate)

/**
 * Sync the DOM indeterminate property with the reactive prop.
 * @returns {void}
 */
const syncIndeterminate = () => {
  if (inputRef.value) {
    inputRef.value.indeterminate = props.indeterminate
  }
}

onMounted(syncIndeterminate)
watch(() => props.indeterminate, syncIndeterminate)

/**
 * Emit the checkbox state whenever the native input changes.
 * @param {Event & { target: HTMLInputElement }} event - Native change event dispatched by the input.
 * @returns {void}
 */
const handleChange = event => {
  const { checked } = event.target
  let nextValue

  if (Array.isArray(props.modelValue)) {
    nextValue = checked
      ? [...props.modelValue, props.value]
      : props.modelValue.filter(item => item !== props.value)
  } else {
    nextValue = checked
  }

  emit("update:modelValue", nextValue)
  emit("change", nextValue)
}
</script>
