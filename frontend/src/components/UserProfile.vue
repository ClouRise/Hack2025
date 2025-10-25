<template>
    <MainCardWindow>
        <template #content>
            <div class="flex justify-between items-center mb-6">
                <p class="text-orange-600 text-2xl font-semibold">
                    Ваш профиль         
                </p> 
                <buttonUI 
                    @click="emit('switch-to-auth')"
                    class="!bg-gray-100 hover:!bg-gray-200 cursor-pointer !text-violet-600 !shadow-none"
                >
                    Выйти
                </buttonUI>
            </div>
             <div class="flex flex-col items-center mb-6">
                <div class="relative">
                    <div 
                        class="w-24 h-24 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden cursor-pointer hover:opacity-80 transition-opacity"
                        @click="changeAvatar"
                    >
                        <img 
                            v-if="avatarUrl"
                            :src="avatarUrl" 
                            alt="Аватар"
                            class="w-full h-full object-cover"
                        />
                        <div v-else class="text-violet-600 text-2xl font-bold">
                            {{ userName.charAt(0).toUpperCase() }}
                        </div>
                    </div>
                </div>
            </div>
            <inputUI    v-model="userName"  placeholder="Введите имя">
                <template #label>Имя</template>
            </inputUI>
            <div class="h-full flex justify-end">
                <buttonUI @click="emit('switch-to-inAccount')" class="bg-violet-600 hover:bg-violet-700 cursor-pointer">
                Продолжить
            </buttonUI> 
            </div>
        </template>
    </MainCardWindow>
</template>

<script setup>
import { ref } from 'vue';
import MainCardWindow from './MainCardWindow.vue';
const emit = defineEmits(['switch-to-auth','switch-to-inAccount'])
const userName = ref('')
const avatarUrl = ref('src/assets/ava.png')    
   
</script>

<style scoped>

</style>