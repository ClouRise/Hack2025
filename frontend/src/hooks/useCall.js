    import { ref, onUnmounted, nextTick, toRaw } from 'vue'
import { Room, RoomEvent, Track } from 'livekit-client'
import axios from 'axios'

export function useCall(roomName, userName) {

const room = ref(null)
const participants = ref([])
const loading = ref(false)
const error = ref('')
const isMuted = ref(false)
const isVideoEnabled = ref(true)
const videoElements = ref([])

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
    
    room.value
      .on(RoomEvent.ParticipantConnected, updateParticipants)
      .on(RoomEvent.ParticipantDisconnected, updateParticipants)
      .on(RoomEvent.TrackSubscribed, handleTrackSubscribed)
       .on(RoomEvent.LocalTrackPublished, handleLocalTrackPublished)

    await room.value.connect('ws://185.31.164.246:7880', tokenData.token)
    await toRaw(room.value).localParticipant.enableCameraAndMicrophone()
    updateParticipants()
    
  } catch (err) {
    error.value = err.response?.data?.detail || err.message
  } finally {
    loading.value = false
  }
}

const leaveRoom = async () => {
  if (room.value) {
    await room.value.disconnect()
    room.value = null
    participants.value = []
  }
}

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