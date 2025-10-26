<template>
  <div class="w-screen h-screen flex justify-between">

    <main class="w-full h-full flex flex-col" :style="(toggleChat || toggleUsers) ? 'width: calc(100% - 20%)' : ''">
      <div class="h-full w-full">
        <!-- Форма входа -->
         <!-- <div v-if="!room" class="join-form">
          <input v-model="store.room_id" placeholder="Название комнаты">
          <input v-model="store.user_name" placeholder="Ваше имя">
          <button @click="joinRoom" :disabled="loading">
            {{ loading ? 'Подключение...' : 'Присоединиться' }}
          </button>
        </div>

        <div v-else>  -->

          <div class="video-container w-full h-full p-3 gap-3">

            <div class="flex justify-center flex-col items-center relative video" v-for="participant in participants"
              :key="participant.identity">
              <video class="rounded-3xl border-2 border-orange-300 w-full h-full" ref="videoElements" :data-identity="participant.identity" autoplay playsinline muted></video>
              <div class="panel-user bg-orange-50 absolute left-5 bottom-5 flex rounded-xl border-1 gap-2 border-orange-300 px-4 items-center py-2">
                <div :style="'background: ' + participant.connectionQualityColor"  style="border-radius: 100px; width: 10px; height: 10px;"></div>
                <h1>{{ participant.name }}</h1>
              </div>
            </div>

          </div>

        <!-- </div> -->
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
import { onMounted, onUnmounted, ref } from 'vue';
import chatComponent from '@/components/chatComponent.vue';
import usersComponent from '@/components/usersComponent.vue';
import { useAppStore } from '@/stores/app';
import { storeToRefs } from 'pinia';

const store = useAppStore()
//  const roomName = ref('')
//  const userName = ref('')
const toggleChat = ref(false)
const toggleUsers = ref(false)

const { room_id, user_name } = storeToRefs(store)

const { room,
  loading,
  error,
  participants,
  isMuted,
  isVideoEnabled,
  videoElements, joinRoom, leaveRoom, toggleAudio, toggleVideo } = useCall(room_id, user_name)

onMounted(() => {
  joinRoom()
})

onUnmounted(() => {
  leaveRoom()
})
</script>

<style scoped>
.video-container{
      display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    grid-template-rows: repeat(auto-fill, minmax(150px, 1fr));
    gap: 10px;
    padding: 10px;
    box-sizing: border-box;
}
.video{
  flex: 1;
  min-height: 0; /* Важно для пропорционального сжатия */
}
.video:hover .panel-user{
  opacity: 100;
  transition: opacity 0.2s ease-in-out;
}
.panel-user{
  opacity: 0;
  transition: opacity 0.2s ease-in-out;
}
</style>