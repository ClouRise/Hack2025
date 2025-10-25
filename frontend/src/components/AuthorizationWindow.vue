<template>
  <!-- Фон -->
    <!-- Модалка -->
    <div class="relative">
      <div class="bg-white rounded-xl p-6 w-94 max-w-96 mx-4 my-4 shadow-xl">
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

</script>