<template>
  <header class="w-full bg-gray-900 shadow-md px-6 py-3 flex items-center justify-between">

    <h1 class="text-xl font-semibold text-gray-200 text-center sm:absolute sm:left-1/2 sm:transform sm:-translate-x-1/2">
      To-Do APP
    </h1>

    <div class="ml-auto relative">
      <button
        @click="open = !open"
        class="flex items-center gap-2 px-4 py-2 bg-gray-200 hover:bg-gray-400 rounded-lg transition-colors"
      >
      <i class="fa-solid fa-bars"></i>
      <i class="fa-solid fa-caret-down"></i>
      </button>

      <div
        v-if="open"
        class="absolute top-12 right-0 bg-white border border-gray-200 rounded-xl shadow-lg w-48 py-2 z-10"
      >
        <button class="w-full text-left px-4 py-2 hover:bg-gray-100 text-gray-700" @click="handleLogin">
          Iniciar sesión
        </button>
        <button class="w-full text-left px-4 py-2 hover:bg-gray-100 text-gray-700" @click="handleRegister">
          Registro
        </button>
        <button class="w-full text-left px-4 py-2 hover:bg-gray-100 text-red-500" @click="handleLogout">
          Cerrar sesión
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from 'vue-router'
import { useAuthStore } from "../stores/authStore";

const router = useRouter()
const open = ref(false);
const authStore = useAuthStore()

/**
 * Navigate to the login route and close the dropdown menu.
 * @returns {void}
 */
function handleLogin(){
  router.push('/login')
  open.value = false
}

/**
 * Navigate to the register route and close the dropdown menu.
 * @returns {void}
 */
function handleRegister(){
  router.push('/register')
  open.value = false
}

/**
 * Clear the authentication state and redirect to the welcome page.
 * @returns {void}
 */
function handleLogout(){
  authStore.LogOut()
  router.push('/')
  open.value = false
}
</script>
