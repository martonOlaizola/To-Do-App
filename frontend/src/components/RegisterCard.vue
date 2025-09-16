<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div class="max-w-md w-full bg-gray-200 rounded-xl shadow-lg p-8 space-y-6">
      <h1 class="text-2xl font-semibold text-center text-gray-800">Iniciar sesión</h1>

      <form class="space-y-4" @submit.prevent="handleSubmit">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Correo electrónico</label>
          <input
            type="email"
            id="email"
            v-model="email"
            placeholder="tucorreo@ejemplo.com"
            class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400"
          />
          <p v-if="emailError" class="text-red-500 text-xs mt-1"><strong>*{{ emailError }}*</strong></p>

        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
          <input
            type="password"
            id="password"
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="********"
            class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400"
          />
          <p v-if="passwordError" class="text-red-500 text-xs mt-1"><strong>*{{ passwordError }}*</strong></p>
        </div>
        
        <div>
          <label for="re-password" class="block text-sm font-medium text-gray-700">Confirmar Contraseña</label>
          <input
            type="password"
            id="re-password"
            v-model="rePassword"
            :type="showRePassword ? 'text' : 'password'"
            placeholder="********"
            class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400"
          />
          <p v-if="rePasswordError" class="text-red-500 text-xs mt-1"><strong>*{{ rePasswordError }}*</strong></p>
        </div>

        <button
          type="submit"
          class="w-full py-2 px-4 bg-indigo-500 hover:bg-indigo-600 text-white font-semibold rounded-md transition-colors duration-200"
        >
          Crear Cuenta
        </button>
      </form>

      <p class="text-sm text-center text-gray-500">
        ¿Ya tienes cuenta?
        <a href="/register" class="text-indigo-500 hover:underline">Iniciar Sesión</a>
      </p>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()

const email = ref('')
const password = ref('')
const rePassword = ref('')
const showPassword = ref(false)
const showRePassword = ref(false)
const emailError = ref('')
const passwordError = ref('')
const rePasswordError = ref('')

function togglePassword() {
  showPassword.value = !showPassword.value
}
function toggleRePassword() {
  showRePassword.value = !showRePassword.value
}
function handleSubmit() {
  if (!email.value){
  emailError.value = 'El Email es obligatorio.'
  } else {
    emailError.value = ''
  }
  if (!password.value){
    passwordError.value = 'La contraseña es obligatoria.'
    return
  }
  if (!rePassword.value){
    rePasswordError.value = 'Por favor, repita la contraseña.'
  } else if (password.value !== rePassword.value){
    rePasswordError.value = 'Las contraseñas no coinciden.'
    return
  } else {
    rePasswordError.value = ''
  }
  
  if (email.value && password.value && rePassword.value){
    const payload = {
      email: email.value,
      password: password.value,
      rePassword: rePassword.value
    }
    delete payload.rePassword
    localStorage.setItem("payload", JSON.stringify(payload))
    router.push('/home')
  }
}
</script>