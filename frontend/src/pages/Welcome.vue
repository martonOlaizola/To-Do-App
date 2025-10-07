<template>
  <main class="flex-1 flex items-center justify-center">
    <div class="pt-40 pb-35 text-center space-y-6 bg-gray/80 text-[#373C41] rounded-[10pt] p-[10pt]">
      <h1 class="text-3xl font-bold text-gray-800">Bienvenido</h1>
      <p class="text-gray-600">Una To-Do App desarrollada con Vue3 (frontend) y FastAPI+PostgreSQL (backend).</p>
      <button
        @click="goToLogin"
        class="bg-gray-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition"
      >
        Iniciar sesión
      </button>
    </div>
  </main>
</template>
<script setup>
import {useRouter} from 'vue-router'
const router = useRouter()

/**
 * Redirect the visitor to the login view.
 * @returns {void}
 */
function goToLogin() {
  router.push('/login')
}
</script>
