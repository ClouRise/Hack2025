<template>
    <div :style="toggleChat ? 'width: 20%' : 'display: none'" class="bg-zinc-100 h-full">


        
    </div>
</template>

<script setup>


const props = defineProps({
    toggleChat: Boolean
})

const toggleChat = props.toggleChat

</script>

<style scoped>

</style>