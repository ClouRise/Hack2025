<template>
  <div>
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
        <video 
          v-for="participant in participants" 
          :key="participant.identity"
          ref="videoElements"
          :data-identity="participant.identity"
          autoplay 
          playsinline
          muted
        />
      </div>
    </div>

    <!-- Ошибка -->
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, onUnmounted, nextTick, toRaw } from 'vue'
import { Room, RoomEvent, Track } from 'livekit-client'
import axios from 'axios'

// Состояние
const room = ref(null)
const participants = ref([])
const roomName = ref('')
const userName = ref('')
const loading = ref(false)
const error = ref('')
const isMuted = ref(false)
const isVideoEnabled = ref(true)
const videoElements = ref([])

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

// Присоединение к комнате
const joinRoom = async () => {
  try {
    loading.value = true
    error.value = ''

    const tokenData = await getToken()
    
    // Создаем и подключаем комнату
    room.value = new Room({
      iceServers: [
        {
          urls: 'turn:185.31.164.246:7882'
        }
      ]
    })
    
    // События
    room.value
      .on(RoomEvent.ParticipantConnected, updateParticipants)
      .on(RoomEvent.ParticipantDisconnected, updateParticipants)
      .on(RoomEvent.TrackSubscribed, handleTrackSubscribed)
       .on(RoomEvent.LocalTrackPublished, handleLocalTrackPublished)

    // Подключаемся
    await room.value.connect('ws://185.31.164.246:7880', tokenData.token)
    // Включаем камеру и микрофон
    await toRaw(room.value).localParticipant.enableCameraAndMicrophone()
    updateParticipants()
    
  } catch (err) {
    error.value = err.response?.data?.detail || err.message
  } finally {
    loading.value = false
  }
}

// Выход из комнаты
const leaveRoom = async () => {
  if (room.value) {
    await room.value.disconnect()
    room.value = null
    participants.value = []
  }
}

// Обновление списка участников
const updateParticipants = () => {
  if (!room.value) return
  
  console.log(toRaw(room.value));
  
  const allParticipants = [room.value.localParticipant, ...Array.from(toRaw(room.value).remoteParticipants.values())]
  console.log(allParticipants);
  
  participants.value = allParticipants.map(p => (
    console.log(p.identity),
    console.log(p.name),
    console.log(p.isSpeaking),
    {
    identity: p.identity,
    name: p.name,
    isSpeaking: p.isSpeaking
  })) 

  nextTick(() => {
    processExistingTracks()
  })  
  
}

const processExistingTracks = () => {
  if (!room.value) return
  
  // Обрабатываем локальные треки
  toRaw(room.value).localParticipant.trackPublications.forEach(publication => {
    if (publication.track && publication.track.kind === Track.Kind.Video) {
      handleLocalTrackPublished(publication)
    }
  })
  toRaw(room.value).remoteParticipants.forEach(participant => {
    participant.trackPublications.forEach(publication => {
      if (publication.track && publication.isSubscribed) {
        handleTrackSubscribed(publication.track, publication, participant)
      }
    })
  })
}

const handleLocalTrackPublished = (publication) => {
  if (publication.track && publication.track.kind === Track.Kind.Video) {
    nextTick(() => {
      // Ищем элемент для локального участника
      const element = videoElements.value.find(el => 
        el.getAttribute('data-identity') === room.value.localParticipant.identity
      )
      if (element) {
        publication.track.attach(element)
      }
    })
  }
}

// Обработка видео-треков
const handleTrackSubscribed = (track, publication, participant) => {
  if (track.kind === Track.Kind.Video) {
    nextTick(() => {
      const element = videoElements.value.find(el => 
        el.getAttribute('data-identity') === participant.identity
      )
      if (element) track.attach(element)
    })
  } else if (track.kind === Track.Kind.Audio) {
    // ДОБАВЬТЕ ЭТО: обработка аудио для удаленных участников
    if (participant !== room.value.localParticipant) {
      track.attach() // воспроизводим звук удаленного участника
    }
  }
}

// Управление аудио/видео
const toggleAudio = async () => {
  if (!room.value) return
  isMuted.value = !isMuted.value
  await toRaw(room.value).localParticipant.setMicrophoneEnabled(!isMuted.value)
}

const toggleVideo = async () => {
  if (!room.value) return
  isVideoEnabled.value = !isVideoEnabled.value
  await room.value.localParticipant.setCameraEnabled(isVideoEnabled.value)
}

// Авто-выход при размонтировании
onUnmounted(() => {
  leaveRoom()
})
</script>

<style scoped>
.videos {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 10px;
  margin-top: 20px;
}

video {
  width: 100%;
  height: 200px;
  background: #000;
  border-radius: 8px;
}

.controls {
  margin: 20px 0;
}

button {
  padding: 10px 15px;
  margin: 0 5px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.leave {
  background: #ff4444;
  color: white;
}

.error {
  color: red;
  margin-top: 10px;
}

.join-form input {
  display: block;
  margin: 10px 0;
  padding: 10px;
  width: 200px;
}
</style>