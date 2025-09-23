<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div class="max-w-md w-full bg-gray-200 rounded-xl shadow-lg p-8 space-y-6">
      <h1 class="text-2xl font-semibold text-center text-gray-800">Iniciar sesión</h1>
      <p class="text-gray-500 text-xs mt-1">Los campos con * son obligatorios</p>
      <form class="space-y-4" @submit.prevent="handleSubmit">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Correo electrónico *</label>
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
          <label for="password" class="block text-sm font-medium text-gray-700">Contraseña *</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="********"
            class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400"
          />
          <p v-if="passwordError" class="text-red-500 text-xs mt-1"><strong>{{ passwordError }}</strong></p>
        </div>

        <button
          type="submit"
          class="w-full py-2 px-4 bg-indigo-500 hover:bg-indigo-600 hover:cursor-pointer text-white font-semibold rounded-md transition-colors duration-200"
        >
          Ingresar
        </button>
      </form>

      <p class="text-sm text-center text-gray-500">
        ¿No tienes cuenta?
        <a href="/register" class="text-indigo-500 hover:underline">Regístrate</a>
      </p>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { getCurrentUser, loginUser } from '../services/loginService'
import { useToast } from 'vue-toastification'
const router = useRouter()
const toast = useToast()

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const emailError = ref('')
const passwordError = ref('')

function togglePassword() {
  showPassword.value = !showPassword.value
}

async function handleSubmit() {
  if (!email.value){
    emailError.value = 'El Email es obligatorio.'
  } else {
    emailError.value = ''
  }
  if (!password.value){
    passwordError.value = 'La contraseña es obligatoria.'
  } else {
    passwordError.value = ''
  }
  const userData = {
    email: email.value,
    password: password.value
  }
  try{
    await loginUser(userData)
    const token = localStorage.getItem('jwt')
    const userMetaData = await getCurrentUser(token)
    localStorage.setItem('user', JSON.stringify(userMetaData))
    toast.success('¡Bienvenido al Sitio!')
    router.push('/home')
  } catch(error) {
    toast.error('Error iniciando sesión.')
    throw new Error('Error iniciando sesión: ' + error.message)
  }
}

</script>