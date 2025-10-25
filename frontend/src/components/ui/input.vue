<template>
  <div class="w-full">
    <!-- Слот для заголовка -->
    <label class="block text-sm font-medium text-gray-700 mb-1">
      <slot name="label">Заголовок</slot>
    </label>
    
    <!-- Input -->
    <input
      :type="type"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
      :placeholder="placeholder"
    >
  </div>
</template>

<script setup>
defineOptions({
  name: 'InputUI'
})

defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  placeholder: {
    type: String,
    default: ''
  }
})

defineEmits(['update:modelValue'])
</script>