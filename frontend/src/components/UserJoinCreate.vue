<template>
    <MainCardWindow>
            <template #content>
                <sliderUI 
                v-model="userChoice"    
                :class="showShake ? 'animate-shake' : ''"
                @tryChange ="handleSliderChange"
                >
                    <template #option1>Создать комнату</template>
                    <template #option2>Подключиться к комнате</template>
                </sliderUI>
                    
                <inputUI v-if="userChoice === 'option1'" v-model="roomName" placeholder="Введите название">
                    <template #label>Название комнаты</template>
                </inputUI>

                <inputUI v-if="userChoice === 'option2'" v-model="roomCode" placeholder="Введите код или ссылку-приглашение">
                    <template #label>Код или ссылка-приглашение</template>
                </inputUI>

            </template> 

            <template #button>
                <div class="flex justify-between items-center w-full">
                    <buttonUI 
                        @click="emit('switch-to-userProfile')"
                        class="!bg-gray-100 hover:!bg-gray-200 cursor-pointer !text-violet-600 !shadow-none"
                    >
                        < Профиль
                    </buttonUI>
                    
                    <buttonUI @click="handleUserAction" class="bg-violet-600 hover:bg-violet-700 cursor-pointer">
                        Продолжить
                    </buttonUI>
                </div>
                
            </template>

    </MainCardWindow>
</template>

<script setup>
    import { ref } from 'vue'
    import MainCardWindow from './MainCardWindow.vue';

    const emit = defineEmits(['switch-to-userProfile'])
    const roomCode = ref('')
    const roomName = ref('')
    const userChoice = ref('option2')

    const handleSliderChange = (value) => {
    userChoice.value = value
}
</script>   

<style scoped>

</style>