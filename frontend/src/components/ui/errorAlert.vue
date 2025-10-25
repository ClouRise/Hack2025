<template>
  <div class="absolute inset-0 bg-opacity-50 backdrop-blur-sm flex items-center justify-center z-50 rounded-xl">
    <!-- Ширина определяется контентом, добавляем только горизонтальные отступы -->
    <div class="bg-white border-2  border-red-300 rounded-xl p-6 m-4 max-w-88 shadow-xl">
      <p class="text-red-600 text-base text-xl text-start font-medium whitespace-nowrap">
        Внимание!
      </p>
      <p class="text-red-600 text-base text-xl text-start font-medium whitespace-wrap">
        <slot>Сообщение об ошибке</slot>
      </p>
    </div>
  </div>
</template>

<script setup>
defineOptions({
  name: 'errorAlertUI'
})
</script>