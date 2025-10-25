<template>
    <div>
<<<<<<< Updated upstream
        <h1 class="text-orange-600">Axenix <span class="text-blue-600 text-italy">Meet</span></h1>
        <h1>start page</h1>
    
        <AuthorizationWindow v-if="currentWindow === 'auth'">
            <template #content>

                <sliderUI v-model="authType">
                    <template #option1 class="cursor-pointer">Вход</template>
                    <template #option2>Регистрация</template>
                </sliderUI>

                 <p 
                    class="text-violet-600 text-base text-center cursor-pointer hover:text-violet-700 transition-colors font-medium"
                    @click="showGuestWindow"
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
                <buttonUI class="bg-violet-600 hover:bg-violet-700 cursor-pointer">{{ authType === 'option1' ? 'Войти' : 'Зарегистрироваться' }}</buttonUI>
            </template>

        </AuthorizationWindow>
>>>>>>> Stashed changes
    </div>
</template>

<script setup>
import { ref } from 'vue';
import AuthorizationWindow from '@/components/AuthorizationWindow.vue';
const authType = ref('option1')
const userChoice = ref('option2')
const prevUserChoice = ref(userChoice.value)
const currentWindow = ref('auth') 
const showShake = ref(false)
const showErrorModal = ref(false)

const showGuestWindow = () => {
  currentWindow.value = 'guest'
  userChoice.value = 'option2'
}

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
    }, 4000)
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