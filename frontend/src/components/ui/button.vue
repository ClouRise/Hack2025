<template>
<<<<<<< Updated upstream
  <button class="text-white px-6 py-2 rounded-lg font-medium transition-colors">
=======
  <button class="bg-blue-500 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-600 transition-colors">
>>>>>>> Stashed changes
    <slot>Кнопка</slot>
  </button>
</template>

<script setup>
defineOptions({
  name: 'buttonUI'
})
</script>