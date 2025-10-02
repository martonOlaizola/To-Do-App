<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div class="max-w-md w-full bg-gray-200 rounded-xl shadow-lg p-8 space-y-6">
      <h1 class="text-2xl font-semibold text-center text-gray-800">Iniciar sesión</h1>
      <p class="text-gray-500 text-xs mt-1">Los campos con * son obligatorios</p>
      <form class="space-y-4" @submit.prevent="onSubmit">
        <div>
          <InputField
          id="email"
          label="Email *"
          placeholder="usuario@email.com"
          :colorTextLabel="'text-gray'"
          v-model="email"
          :error="emailError"
          />
          <p v-if="emailError" class="text-red-500 text-xs mt-1"><strong>*{{ emailError }}*</strong></p>
        </div>

        <div>
          <InputField
          id="password"
          label="Contraseña *"
          :type="showPassword ? 'text' : 'password'"
          :colorTextLabel="'text-gray'"
          v-model="password"
          :error="passwordError"
          > 
            <template #icon>
              <button
              type="button"
              class="absolute inset-y-0 right-2 flex items-center text-gray-500 :hover cursor-pointer" 
              @click="togglePassword"
              >
              <i v-if="!showPassword" class="fa-solid fa-eye"/>
              <i v-else class="fa-solid fa-eye-slash"/>
              </button>
            </template>
          </InputField>
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
import * as yup from 'yup'
import { useToast } from 'vue-toastification'
import { useField, useForm } from 'vee-validate'
import { getCurrentUser, loginUser } from '../services/loginService'
import InputField from '../components/InputField.vue'
import { useAuthStore } from '../stores/authStore'

const router = useRouter()
const toast = useToast()
const authStore = useAuthStore()

const showPassword = ref(false)
const schema = yup.object({
  email: yup.string()
    .required("Por favor, ingrese su email.").
    email("Respete el formato de email"),
  password: yup.string().
    required("Por favor, ingrese su contraseña").
    min(8, "Mínimo 8 caracteres"),
})

const { handleSubmit } = useForm({
  validationSchema: schema,
  initialValues: {
    email: '',
    password: '',
  }
})
const { value: email, errorMessage: emailError } = useField('email')
const { value: password, errorMessage: passwordError } = useField('password')

function togglePassword() {
  showPassword.value = !showPassword.value
}

const onSubmit = handleSubmit(async (values) => {
  try{
    const userData = {
      email: values.email,
      password: values.password
    }
    const token = await loginUser(userData)
    const userMetaData = await getCurrentUser(token)
    authStore.setToken(token)
    authStore.setUser(userMetaData)
    toast.success('¡Bienvenido al Sitio!')
    router.push('/home')
  } catch(error) {
    toast.error('Error iniciando sesión.')
    throw new Error(`Error: ${error}`)
  }
})

</script>