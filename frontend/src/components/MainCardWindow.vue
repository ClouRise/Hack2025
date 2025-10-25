<template>
  <!-- Фон -->
    <!-- Модалка -->
    <div class="relative h-full">
      <div class="bg-white rounded-xl p-6 w-94 max-w-96 max-h-120 h-full mx-4 my-4 shadow-xl">
      <!-- Слот для контента -->
      <div class="space-y-4">
        <slot name="content"></slot>
      </div>
      
      <!-- Слот для кнопки -->
      <div class="flex justify-end mt-6">
        <slot name="button"> </slot>
      </div>
    </div>
    </div>
</template>

<script setup>

</script>`