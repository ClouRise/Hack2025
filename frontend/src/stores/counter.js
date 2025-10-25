import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('app', () => {
  const user_name = ref('')
  const user_id = ref(null)

  return { user_name, user_id }
})
