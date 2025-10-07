import { defineStore } from "pinia";

/**
 * Centralized Pinia store that manages authentication state.
 * @returns {import('pinia').Store<'auth', { token: string | null, user: Record<string, unknown> | null }, {}, { setToken(newToken: string | null): void, setUser(newUser: Record<string, unknown> | null): void, LogOut(): void }>}
 */
export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    user: null
  }),
  getters: {
    /**
     * Evaluate whether the user is currently authenticated.
     * @param {{ token: string | null }} state - Reactive state managed by Pinia.
     * @returns {boolean} True when a token is present.
     */
    isAuthenticated: (state) => !!state.token
  },
  actions: {
    /**
     * Store the authentication token returned by the backend.
     * @param {string | null} newToken - JWT token to persist in the store.
     * @returns {void}
     */
    setToken(newToken) {
      this.token = newToken
    },
    /**
     * Persist the user metadata returned by the backend.
     * @param {Record<string, unknown> | null} newUser - User payload to store.
     * @returns {void}
     */
    setUser(newUser) {
      this.user = newUser
    },
    /**
     * Clear every authentication related value from the store.
     * @returns {void}
     */
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
