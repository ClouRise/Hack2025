<template>
  <div class="bg-gray-100 rounded-xl p-1 flex w-full mx-auto relative">
    <div
      class="absolute bg-white shadow rounded-lg transition-all duration-300 z-0"
      :class="[
        'h-[calc(100%-0.5rem)] top-1',
        activeSlide === 'option1' ? 'w-1/2 left-1' : 'w-1/2 left-[calc(50%-0.25rem)]'
      ]"
    ></div>
    
    <button
      @click="activeSlide = 'option1'"
      class="flex-1 py-3 px-4 relative z-10 font-medium transition-colors"
      :class="activeSlide === 'option1' ? 'text-foreground' : 'text-gray-500'"
    >
      <slot name="option1">Опция 1</slot>
    </button>
    
    <button
      @click="activeSlide = 'option2'"
      class="flex-1 py-3 px-4 relative z-10 font-medium transition-colors"
      :class="activeSlide === 'option2' ? 'text-foreground' : 'text-gray-500'"
    >
      <slot name="option2">Опция 2</slot>
    </button>
  </div>
</template>


<script setup>
defineOptions({
    name: 'sliderUI'
})
import { ref } from 'vue'

const activeSlide = ref('option1') // начальное положение слайдера
</script>

<style scoped>

</style>