<template>
    <div class="bg-violet-50 h-full flex flex-col justify-between border-l-1 border-violet-200 relative">
        <div class="w-full flex justify-between p-3 items-center border-b-1 border-violet-200">
            <img style="height: 35px;" class="cursor-pointer" @click="$emit('update:toggleChat', false)" src="../assets/icons/close.svg" alt="">
            <div class="w-full flex justify-center items-center">
                <h3 class="text-violet-900 font-bold text-lg">Чат</h3>
            </div>
        </div>
        <div class="h-full bg-violet-100 overflow-y-auto">
            <ul class="divide-y">
                <li class="w-full" v-for="message in messageList" :key="message.id">
                    <h4>{{ message.username }}</h4>
                    <div>
                        <p>{{ message.message }}</p>
                        <p>{{ message.created_at }}</p>
                    </div>
                </li>
            </ul>
        </div>
        <div class="bg-violet-50 flex justify-between border-t-1 border-violet-200 px-4 py-6 items-center gap-4" style="height: 108px;">
            <input class="bg-violet-50 text-zinc-600 px-3 rounded-lg hover:bg-violet-100 hover:border-violet-400 transition-colors border border-violet-300 w-full h-full" type="text">
            <buttonUI style="width: 60px; height: auto; margin: 0; padding: 10px;" class="bg-violet-600 border-2 border-violet-600 hover:bg-violet-800 transition-color p-0 m-0"><img style="height: 30px; width: 30px;" class="cursor-pointer" src="../assets/icons/send_w.svg" alt=""></buttonUI>
        </div>
    </div>
</template>

<script setup>

</script>
