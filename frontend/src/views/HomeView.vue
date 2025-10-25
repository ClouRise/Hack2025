<template>
    <div class="relative flex justify-center items-center flex-col">
        <h1 class="text-orange-600 font-quicksand">Axenix <span class="text-blue-600 text-italy font-Quicksand">Meet</span></h1>
        <h1>start page</h1>
    
        <AuthWindow
        v-if="currentWindow === 'auth'"
        @switch-to-guest="currentWindow = 'guest'"
        @switch-to-userProfile="currentWindow = 'userProfile'"
        @auth-success="handleAuthSuccess"
        ></AuthWindow>

        <GuestWindow
        v-else-if="currentWindow === 'guest'"
        @switch-to-auth="currentWindow = 'auth'"
        @join-room="handleJoinRoom"
        ></GuestWindow>

        <UserJoinCreate
        v-else-if="currentWindow === 'inAccount'"
        @switch-to-userProfile="currentWindow = 'userProfile'"
        @join-room="handleJoinRoom"
        @create-room="handlecreateRoom"
        ></UserJoinCreate>

        <UserProfile
        v-else-if="currentWindow==='userProfile'"
        @switch-to-auth="currentWindow = 'auth'"
        @switch-to-inAccount="currentWindow = 'inAccount'"
        >
        </UserProfile>
        
            
        </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import AuthWindow from '@/components/AuthWindow.vue'
import GuestWindow from '@/components/GuestWindow.vue'
import UserJoinCreate from '@/components/UserJoinCreate.vue';
import UserProfile from '@/components/UserProfile.vue';
const currentWindow = ref('auth') 

</script>

<style scoped>

</style>