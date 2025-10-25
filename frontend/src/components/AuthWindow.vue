<template>
     <MainCardWindow>
            <template #content>

                <sliderUI v-model="authType">
                    <template #option1 class="cursor-pointer">Вход</template>
                    <template #option2>Регистрация</template>
                </sliderUI>

                 <p 
                    class="text-violet-600 text-base text-center cursor-pointer hover:text-violet-700 transition-colors font-medium"
                    @click="emit('switch-to-guest')"
                    >
                    Войти как гость
                </p> 
                            
                <inputUI v-if="authType === 'option1'" placeholder="Введите email">
                    <template #label>Email</template>
                </inputUI>
                
                <inputUI v-if="authType === 'option1'" type="password" placeholder="Введите пароль">
                    <template #label>Пароль</template>
                </inputUI>

                <inputUI v-if="authType === 'option2'" placeholder="Введите email">
                    <template #label>Email</template>
                </inputUI>

                <inputUI v-if="authType === 'option2'" type="password" placeholder="Придумайте пароль">
                    <template #label>Пароль</template>
                </inputUI>

                <inputUI v-if="authType === 'option2'" type="password" placeholder="Повторите пароль">
                    <template #label>Повторите пароль</template>
                </inputUI>

            </template>

            <template #button>
                <buttonUI @click="emit('switch-to-userProfile')" class="bg-violet-600 hover:bg-violet-700 cursor-pointer">{{ authType === 'option1' ? 'Войти' : 'Зарегистрироваться' }}</buttonUI>
            </template>

        </MainCardWindow>
</template>

<script setup>
    import { ref } from 'vue'
        const emit = defineEmits(['switch-to-guest', 'switch-to-userProfile'])
    import MainCardWindow from './MainCardWindow.vue';
    const authType = ref('option1')
</script>

<style scoped>

</style>