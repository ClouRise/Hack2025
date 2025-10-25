<template>
    <div>
<<<<<<< Updated upstream
        <h1 class="text-orange-600">Axenix <span class="text-blue-600 text-italy">Meet</span></h1>
=======
        <h1>start page</h1>
        
        
        <AuthorizationWindow>
            <template #content>

                <sliderUI>
                    <template #option1>Вход</template>
                    <template #option2>Регистрация</template>
                </sliderUI>

                <inputUI placeholder="Введите email">
                    <template #label>Email</template>
                </inputUI>

                <inputUI type="password" placeholder="Придумайте пароль">
                    <template #label>Пароль</template>
                </inputUI>

                <inputUI type="password" placeholder="Введите пароль">
                    <template #label>Повторите пароль</template>
                </inputUI>

            </template>

            <template #button>
                <buttonUI>Вход</buttonUI>
            </template>

        </AuthorizationWindow>
>>>>>>> Stashed changes
    </div>
</template>

<script>
    export default {
        
    }
<script setup>
import { ref } from 'vue';
import AuthorizationWindow from '@/components/AuthorizationWindow.vue';
</script>

<style scoped>

</style>