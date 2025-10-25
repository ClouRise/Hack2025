<template>
  <div class="w-screen h-screen flex justify-between">

    <main class="w-full h-full flex flex-col" :style="(toggleChat || toggleUsers) ? 'width: calc(100% - 20%)' : ''">
      <div class="h-full">
        <!-- Форма входа -->
        <div v-if="!room" class="join-form">
          <input v-model="roomName" placeholder="Название комнаты">
          <input v-model="userName" placeholder="Ваше имя">
          <button @click="joinRoom" :disabled="loading">
            {{ loading ? 'Подключение...' : 'Присоединиться' }}
          </button>
        </div>

        <div v-else>

          <div class="videos">

            <div class="flex justify-center flex-col items-center" v-for="participant in participants"
              :key="participant.identity">
              <video ref="videoElements" :data-identity="participant.identity" autoplay playsinline muted></video>
              <h3>{{ participant.name }}hui</h3>
            </div>

          </div>

        </div>
      </div>

      <footer class="bg-violet-50 flex justify-between px-4 py-2 items-center border-t-1 border-violet-200" style="height: 100px;">

        <buttonUI :isVoid="true" class=""><img style="height: 40px; width: 40px;" src="../assets/icons/dots_horizontal.svg" alt=""></buttonUI>
        
        <div class="flex gap-5">
          <buttonUI :isVoid="true" @click="toggleAudio"><div class="w-full h-full relative flex justify-center items-center"><img style="height: 40px; width: 40px;" src="../assets/icons/Microphone.svg" alt=""><img :style="isMuted ? 'display: block' : 'display: none'" src="../assets/icons/stop.svg" alt="" style="position: absolute; right: 3px; bottom: 3px; width: 28px;"></div></buttonUI>
          <buttonUI :isVoid="true" @click="toggleVideo"><div class="w-full h-full relative flex justify-center items-center"><img style="height: 40px; width: 40px;" src="../assets/icons/Record.svg" alt=""><img :style="!isVideoEnabled ? 'display: block' : 'display: none'" src="../assets/icons/stop.svg" alt="" style="position: absolute; right: 3px; bottom: 3px; width: 28px;"></div></buttonUI>
          <buttonUI style="width: 55px; height: 55px; padding: 0;" @click="leaveRoom" class="bg-red-100 border border-red-600 hover:bg-red-200 transition-color flex justify-center items-center shadow-md"><img style="height: 40px; width: 40px;" src="../assets/icons/Missed_call.svg" alt=""></buttonUI>
        </div>

        <div class="flex gap-5">
            <buttonUI :isVoid="true" @click="toggleUsers = true"><img style="height: 40px; width: 40px;" src="../assets/icons/users.svg" alt=""></buttonUI>
            <buttonUI :isVoid="true" @click="toggleChat = true"><img style="height: 40px; width: 40px;" src="../assets/icons/chat.svg" alt=""></buttonUI>
        </div>

      </footer>
    </main>
    <chat-component :style="toggleChat ? 'width: 20%; position: absolute; right: 0; top: 0;' : 'display: none'"
      v-model:toggleChat="toggleChat"></chat-component>
    <users-component :style="toggleUsers ? 'width: 20%; position: absolute; right: 0; top: 0;' : 'display: none'"
      v-model:toggleUsers="toggleUsers"></users-component>
  </div>
</template>

<script setup>


import { useCall } from '@/hooks/useCall';
import { onUnmounted, ref } from 'vue';
import chatComponent from '@/components/chatComponent.vue';
import usersComponent from '@/components/usersComponent.vue';


const roomName = ref('')
const userName = ref('')
const toggleChat = ref(false)
const toggleUsers = ref(false)

// Получение токена от бэкенда
const getToken = async () => {
  const response = await axios.post('http://localhost:8000/liveKit/api/get-token', {
    room_name: roomName.value,
    user_name: userName.value,
    user_id: `${Date.now()}`.toString()
  })
  console.log(response.data)
  return response.data
}
const { room,
  participants,
  loading,
  error,
  isMuted,
  isVideoEnabled,
  videoElements, joinRoom, leaveRoom, toggleAudio, toggleVideo } = useCall(roomName, userName)


onUnmounted(() => {
  leaveRoom()
})
</script>

<style scoped></style>