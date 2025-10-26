<template>
    <MainCardWindow>
            <template #content>
                <p class="text-orange-600 text-2xl text-start font-semibold">
                    Вы в режиме гостя          
                </p> 
                <sliderUI 
                v-model="userChoice"    
                :class="showShake ? 'animate-shake' : ''"
                @tryChange ="handleSliderChange"
                >
                    <template #option1>Создать комнату</template>
                    <template #option2>Подключиться к комнате</template>
                </sliderUI>
                    
                <inputUI v-if="userChoice === 'option2'" v-model="store.room_id" placeholder="Введите код или ссылку-приглашение">
                    <template #label>Код или ссылка-приглашение</template>
                </inputUI>

                <inputUI v-if="userChoice === 'option2'" v-model="store.user_name"  placeholder="Введите имя">
                    <template #label>Имя</template>
                </inputUI>

                <errorAlertUI v-if="showErrorModal">Для создания комнаты вы должны быть авторизованы.</errorAlertUI>

            </template> 

            <template #button>
                <div class="flex justify-between items-center w-full">
                    <buttonUI 
                        @click="emit('switch-to-auth')"
                        class="!bg-gray-100 hover:!bg-gray-200 cursor-pointer !text-violet-600 !shadow-none"
                    >
                        Авторизация
                    </buttonUI>
                    
                    <buttonUI @click="$router.push('/call')" class="bg-violet-600 hover:bg-violet-700 cursor-pointer">
                        Продолжить
                    </buttonUI> 
                </div>
                
            </template>

        </MainCardWindow>
</template>

<script setup>
    import { ref,watch } from 'vue';
    import MainCardWindow from './MainCardWindow.vue';
    import { useAppStore } from '@/stores/app';
import { useCall } from '@/hooks/useCall';

    const store = useAppStore()

    //const {joinRoom} = useCall(store.room_id, store.user_name)
    const emit = defineEmits(['switch-to-auth'])
    const userChoice = ref('option2')
    const showShake = ref(false)
    const showErrorModal = ref(false)
    const prevUserChoice = ref('option2')

    watch(userChoice,(newVal,oldVal)=>{
        prevUserChoice.value = oldVal
    })

    const handleSliderChange = (value) => {
  if (value === 'option1') {
    // тряска и ошибка
    showShake.value = true
    showErrorModal.value = true
    console.log(showErrorModal.value)

    setTimeout(() => {
        userChoice.value = prevUserChoice.value
    }, 0);

    setTimeout(() => {
      showErrorModal.value = false
    }, 2500)
    setTimeout(() => {
      showShake.value = false
    }, 500)
  } else {
    // нормальное переключение
    userChoice.value = value
  }
}
</script>

<style scoped>
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}
.animate-shake {
  animation: shake 0.3s ease-in-out;
}
</style>