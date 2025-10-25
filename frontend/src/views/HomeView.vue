<template>
    <div class="relative flex justify-center items-center flex-col">
        <h1 class="text-orange-600">Axenix <span class="text-blue-600 text-italy">Meet</span></h1>
        <h1>start page</h1>
<<<<<<< Updated upstream
    
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
=======
        
        
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
>>>>>>> Stashed changes
                    <template #label>Повторите пароль</template>
                </inputUI>

            </template>

            <template #button>
<<<<<<< Updated upstream
                <buttonUI class="bg-violet-600 hover:bg-violet-700 cursor-pointer">{{ authType === 'option1' ? 'Войти' : 'Зарегистрироваться' }}</buttonUI>
            </template>

        </AuthorizationWindow>
        
        <AuthorizationWindow v-else-if="currentWindow === 'guest'">
            <template #content>

                <sliderUI 
                v-model="userChoice"  
                :class="showShake ? 'animate-shake' : ''"
                @tryChange ="handleSliderChange"
                >
                    <template #option1 class="cursor-pointer">Создать комнату</template>
                    <template #option2>Подключиться к комнате</template>
                </sliderUI>
                    
                <inputUI v-if="userChoice === 'option2'" placeholder="Введите код или ссылку-приглашение">
                    <template #label>Код или ссылка-приглашение</template>
                </inputUI>

                <inputUI v-if="userChoice === 'option2'" placeholder="Введите имя">
                    <template #label>Имя</template>
                </inputUI>

                <errorAlertUI v-if="showErrorModal">Для создания комнаты вы должны быть авторизованы.</errorAlertUI>

            </template> 

            <template class="relative" #button>
                <div class="flex justify-between items-center w-full">
                    <!-- Кнопка назад -->
                    <buttonUI 
                        @click="currentWindow = 'auth'; authType = 'option2';"
                        class="!bg-gray-100 hover:!bg-gray-200 cursor-pointer !text-violet-600 !shadow-none"
                    >
                        Авторизация
                    </buttonUI>
                    
                    <!-- Кнопка продолжить -->
                    <buttonUI class="bg-violet-600 hover:bg-violet-700 cursor-pointer">
                        Продолжить
                    </buttonUI>
                </div>
                
            </template>

            
    </AuthorizationWindow>

    
=======
                <buttonUI>Вход</buttonUI>
            </template>

        </AuthorizationWindow>
>>>>>>> Stashed changes
    </div>
</template>

<script setup>
<<<<<<< Updated upstream
import { ref, watch } from 'vue';
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


=======
import { ref } from 'vue';
import AuthorizationWindow from '@/components/AuthorizationWindow.vue';
>>>>>>> Stashed changes
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