<template>

  <button :style="isVoid ? 'width: 55px; height: 55px' : ''" :class="isVoid ? 'bg-violet-50 text-zinc-600 rounded-lg hover:bg-violet-200 transition-colors flex justify-center items-center border border-violet-300 shadow-md' : 'bg-blue-500 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-600 transition-colors'">

    <slot>Кнопка</slot>
  </button>
</template>

<script setup>
defineOptions({
  name: 'buttonUI'
})
const props = defineProps({
    isVoid: Boolean
})
const isVoid = props.isVoid
</script>