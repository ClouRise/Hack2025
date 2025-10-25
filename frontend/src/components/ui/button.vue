<template>
  <button class="bg-blue-500 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-600 transition-colors">
    <slot>Кнопка</slot>
  </button>
</template>

<script setup>
defineOptions({
  name: 'buttonUI'
})
</script>