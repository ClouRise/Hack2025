<template>
  <main>
    <!-- Форма входа -->
    <div v-if="!room" class="join-form">
      <input v-model="roomName" placeholder="Название комнаты">
      <input v-model="userName" placeholder="Ваше имя">
      <button @click="joinRoom" :disabled="loading">
        {{ loading ? 'Подключение...' : 'Присоединиться' }}
      </button>
    </div>

    <!-- Видео-конференция -->
    <div v-else class="conference">
      <!-- Управление -->
      <div class="controls">
        <button @click="toggleAudio">{{ isMuted ? '🔇' : '🎤' }}</button>
        <button @click="toggleVideo">{{ isVideoEnabled ? '📹' : '📷' }}</button>
        <button @click="leaveRoom" class="leave">🚪 Выйти</button>
      </div>

      <!-- Видео участников -->
      <div class="videos">
        <div class="flex justify-center flex-col items-center" v-for="participant in participants" :key="participant.identity">
                  <video ref="videoElements"
          :data-identity="participant.identity" autoplay playsinline muted />
          <h3>{{ participant.name }}hui</h3>
        </div>
      </div>
    </div>

    <!-- Ошибка -->
    <div v-if="error" class="error">{{ error }}</div>
  </main>
  <chat-component v-model:toggleChat="toggleChat"></chat-component>
</template> 

<script setup>
import { useCall } from '@/hooks/useCall';
import { onUnmounted, ref } from 'vue';
import chatComponent from '@/components/chatComponent.vue';

const roomName = ref('')
const userName = ref('')
const toggleChat = ref(false)

// Получение токена от бэкенда
const getToken = async () => {
  const response = await axios.post('http://localhost:8000/liveKit/api/get-token', {
    room_id: roomName.value,
    user_name: userName.value,
    user_id: Date.now()
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

<style scoped>
</style>