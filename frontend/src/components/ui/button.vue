<template>
  <button class="text-white px-6 py-2 rounded-lg font-medium transition-colors">
    <slot>Кнопка</slot>
  </button>
</template>

<script setup>
defineOptions({
  name: 'buttonUI'
})
</script>