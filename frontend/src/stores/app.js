import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', () => {
  const user_name = ref('')
  const user_id = ref(null)
  const room_id = ref('')
  const participants = ref([])

  const baseUrlServer = ''

  return { user_name, user_id, baseUrlServer, room_id , participants}
})
