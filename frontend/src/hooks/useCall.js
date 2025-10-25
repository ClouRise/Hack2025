import { ref, onUnmounted, nextTick, toRaw } from 'vue'
import { Room, RoomEvent, Track, ParticipantEvent, ConnectionQuality } from 'livekit-client'
import axios from 'axios'

export function useCall(roomName, userName) {
  const room = ref(null)
  const participants = ref([])
  const loading = ref(false)
  const error = ref('')
  const isMuted = ref(false)
  const isVideoEnabled = ref(true)
  const videoElements = ref([])
  
  // Добавляем Map для хранения качества соединения каждого участника
  const connectionQualities = ref(new Map())

  const getToken = async () => {
    const response = await axios.post('http://localhost:8000/liveKit/api/get-token', {
      room_name: roomName.value,
      user_name: userName.value,
      user_id: Date.now()
    })
    console.log(response.data)
    return response.data
  }

  const joinRoom = async () => {
    try {
      loading.value = true
      error.value = ''

      const tokenData = await getToken()
      
      room.value = new Room({
        iceServers: [
          {
            urls: 'turn:185.31.164.246:7882'
          }
        ]
      })
      
      // Добавляем обработчики для качества соединения
      room.value
        .on(RoomEvent.ParticipantConnected, participant => {
          setupParticipantQualityTracking(participant)
          updateParticipants()
        })
        .on(RoomEvent.ParticipantDisconnected, participant => {
          cleanupParticipantQualityTracking(participant)
          updateParticipants()
        })
        .on(RoomEvent.TrackSubscribed, handleTrackSubscribed)
        .on(RoomEvent.LocalTrackPublished, handleLocalTrackPublished)
        // Отслеживаем изменение качества соединения
        .on(RoomEvent.ConnectionQualityChanged, (quality, participant) => {
          if (participant) {
            updateParticipantQuality(participant.identity, quality)
          }
        })

      await room.value.connect('ws://185.31.164.246:7880', tokenData.token)
      await toRaw(room.value).localParticipant.enableCameraAndMicrophone()
      
      // Инициализируем качество соединения для локального участника
      updateParticipantQuality(room.value.localParticipant.identity, room.value.localParticipant.connectionQuality)
      updateParticipants()
      
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
    } finally {
      loading.value = false
    }
  }

  // Функция для настройки отслеживания качества участника
  const setupParticipantQualityTracking = (participant) => {
    participant.on(ParticipantEvent.ConnectionQualityChanged, (quality) => {
      updateParticipantQuality(participant.identity, quality)
    })
    
    // Инициализируем начальное качество
    updateParticipantQuality(participant.identity, participant.connectionQuality)
  }

  // Функция для очистки отслеживания качества
  const cleanupParticipantQualityTracking = (participant) => {
    participant.removeAllListeners()
    connectionQualities.value.delete(participant.identity)
  }

  const leaveRoom = async () => {
  if (room.value) {
    await room.value.disconnect()
    room.value = null
    participants.value = []
  }
}

  // Функция обновления качества участника
  const updateParticipantQuality = (identity, quality) => {
    connectionQualities.value.set(identity, quality)
    // Обновляем participants чтобы триггерить реактивность
    updateParticipants()
  }

  // Получаем качество соединения для участника
  const getParticipantQuality = (identity) => {
    return connectionQualities.value.get(identity) || ConnectionQuality.Unknown
  }

  // Функция для получения цвета качества
  const getQualityColor = (quality) => {
    switch (quality) {
      case ConnectionQuality.Excellent:
        return '#00C851'
      case ConnectionQuality.Good:
        return '#FE9900'
      case ConnectionQuality.Poor:
        return '#FA2C37'
      case ConnectionQuality.Unknown:
      default:
        return 'Unknown'
    }
  }

  const updateParticipants = () => {
    if (!room.value) return
    
    console.log(toRaw(room.value));
    
    const allParticipants = [room.value.localParticipant, ...Array.from(toRaw(room.value).remoteParticipants.values())]
    console.log(allParticipants);
    
    participants.value = allParticipants.map(p => ({
      identity: p.identity,
      name: p.name,
      isSpeaking: p.isSpeaking,
      connectionQualityColor: getQualityColor(getParticipantQuality(p.identity)),
    })) 

    nextTick(() => {
      processExistingTracks()
    })  
  }

  const processExistingTracks = () => {
    if (!room.value) return
    
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
        const element = videoElements.value.find(el => 
          el.getAttribute('data-identity') === room.value.localParticipant.identity
        )
        if (element) {
          publication.track.attach(element)
        }
      })
    }
  }

  const handleTrackSubscribed = (track, publication, participant) => {
    if (track.kind === Track.Kind.Video) {
      nextTick(() => {
        const element = videoElements.value.find(el => 
          el.getAttribute('data-identity') === participant.identity
        )
        if (element) track.attach(element)
      })
    } else if (track.kind === Track.Kind.Audio) {
      if (participant !== room.value.localParticipant) {
        track.attach()
      }
    }
  }

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

  // Очистка при размонтировании
  onUnmounted(() => {
    if (room.value) {
      leaveRoom()
    }
  })

  return {
    room,
    participants,
    roomName,
    userName,
    loading,
    error,
    isMuted,
    isVideoEnabled,
    videoElements,
    joinRoom,
    leaveRoom,
    toggleVideo,
    toggleAudio
  }
}