<template>
  <!-- Фон -->
    <!-- Модалка -->
    <div class="bg-white rounded-xl p-6 w-96 max-w-full mx-4 shadow-xl">
      <!-- Слот для контента -->
      <div class="space-y-4">
        <slot name="content"></slot>
      </div>
      
      <!-- Слот для кнопки -->
      <div class="flex justify-end mt-6">
        <slot name="button"></slot>
      </div>
    </div>
</template>

<script setup>

</script>