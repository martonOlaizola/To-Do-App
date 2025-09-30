import { defineStore } from "pinia";

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    user: null
  }),
  getters: {
    isAuthenticated: (state) => !!state.token
  },
  actions: {
    setToken(newToken) {
      this.token = newToken
    },
    setUser(newUser) {
      this.user = newUser
    },
    LogOut() {
      this.$reset()
    }
  },
  
  persist: {
    key: 'auth',
    storage: localStorage,
    paths: ['token']
  }
})