<template>
    <MainCardWindow>
        <template #content>

            <sliderUI v-model="authType">
                <template #option1 class="cursor-pointer">Вход</template>
                <template #option2>Регистрация</template>
            </sliderUI>

            <p class="text-violet-600 text-base text-center cursor-pointer hover:text-violet-700 transition-colors font-medium"
                @click="emit('switch-to-guest')">
                Войти как гость
            </p>

            <inputUI v-model="emailLogIn" v-if="authType === 'option1'" placeholder="Введите email">
                <template #label>Email</template>
            </inputUI>

            <inputUI v-model="passLogIn" v-if="authType === 'option1'" type="password" placeholder="Введите пароль">
                <template #label>Пароль</template>
            </inputUI>

            <inputUI v-model="emailSignUp" v-if="authType === 'option2'" placeholder="Введите email">
                <template #label>Email</template>
            </inputUI>

            <inputUI v-model="passSignUp" v-if="authType === 'option2'" type="password" placeholder="Придумайте пароль">
                <template #label>Пароль</template>
            </inputUI>

            <inputUI v-model="confirmPassSignUp" v-if="authType === 'option2'" type="password"
                placeholder="Повторите пароль">
                <template #label>Повторите пароль</template>
            </inputUI>

        </template>

        <template v-if="authType === 'option1'" #button>
            <buttonUI @click="login" class="bg-violet-600 hover:bg-violet-700 cursor-pointer">Войти</buttonUI>
        </template>

        <template v-if="authType === 'option2'" #button>
            <buttonUI @click="register" class="bg-violet-600 hover:bg-violet-700 cursor-pointer">Зарегистрироваться</buttonUI>
        </template>

    </MainCardWindow>
</template>

<script setup>
import { ref, watch } from 'vue'
const emit = defineEmits(['switch-to-guest', 'switch-to-userProfile'])
import MainCardWindow from './MainCardWindow.vue';
import { useRequest } from '@/hooks/useRequest';

const authType = ref('option1')

const emailLogIn = ref('')
const passLogIn = ref('')

const emailSignUp = ref('')
const passSignUp = ref('')
const confirmPassSignUp = ref('')

const { data, loading, requestGet, requestPost } = useRequest()

const login = async () => {
    try {
        loading.value = true;

        const response = await requestPost('http://localhost:8000/users/token', {
            username: emailLogIn.value,
            password: passLogIn.value, 
        });

        if (response && response.access_token) {
            localStorage.setItem('auth_token', response.access_token);
            emit('switch-to-userProfile');
        } else {
            console.error('Ошибка входа: неверный ответ от сервера');
            alert('Ошибка входа. Проверьте email и пароль.');
        }
    } catch (error) {
        console.error('Ошибка входа:', error);
        alert('Ошибка входа. Проверьте email и пароль.');
    } finally {
        loading.value = false;
    }
}

const register = async () => {
    try {
        if (passSignUp.value !== confirmPassSignUp.value) {
            alert('Пароли не совпадают');
            return;
        }

        if (passSignUp.value.length < 6) {
            alert('Пароль должен содержать минимум 6 символов');
            return;
        }

        loading.value = true;

        const response = await requestPost('http://localhost:8000/users/register', {
            email: emailSignUp.value,
            password: passSignUp.value,
            username: confirmPassSignUp.value 
        });

        if (response) {
            
            console.log('Успешная регистрация:', response);
            alert('Регистрация успешна! Теперь вы можете войти.');
            
            authType.value = 'option1';
            
            emailSignUp.value = '';
            passSignUp.value = '';
            confirmPassSignUp.value = '';
            emit('switch-to-userProfile');
        }
    } catch (error) {
        console.error('Ошибка регистрации:', error);
        alert('Ошибка регистрации. Возможно, пользователь с таким email уже существует.');
    } finally {
        loading.value = false;
    }
}
</script>

<style scoped></style>