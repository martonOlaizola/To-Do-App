<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div class="max-w-md w-full bg-gray-200 rounded-xl shadow-lg p-8 space-y-6">
      <h1 class="text-2xl font-semibold text-center text-gray-800">Registrate</h1>

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
        </div>
        <div>
        <InputField
          id="password"
          label="Contraseña *"
          :type="showPassword ? 'text' : 'password'"
          :colorTextLabel="'text-gray'"
          placeholder="********"
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
        </div>
        
        <div>
          <InputField
          id="rePassword"
          label="Repetir Contraseña *"
          :type="showRePassword ? 'text' : 'password'"
          :colorTextLabel="'text-gray'"
          placeholder="********"
          v-model="rePassword"
          :error="rePasswordError"
          > 
            <template #icon>
              <button
              type="button"
              class="absolute inset-y-0 right-2 flex items-center text-gray-500 :hover cursor-pointer" 
              @click="toggleRePassword"
              >
              <i v-if="!showRePassword" class="fa-solid fa-eye"/>
              <i v-else class="fa-solid fa-eye-slash"/>
              </button>
            </template>
          </InputField>
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
import * as yup from 'yup'
import { useForm, useField } from 'vee-validate'
import { getCurrentUser, loginUser, registerUser } from '../services/loginService'
import InputField from './InputField.vue'
import { useAuthStore } from '../stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const showPassword = ref(false)
const showRePassword = ref(false)
const schema = yup.object({
  email: yup.string()
    .required("Por favor, ingrese su email.").
    email("Respete el formato de email"),
  password: yup.string().
    required("Por favor, ingrese su contraseña").
    min(8, "Mínimo 8 caracteres"),
  rePassword: yup.string()
    .required("Por favor, repita su contraseña")
    .oneOf([yup.ref("password"), null], "Las contraseñas no coinciden")
})

const { handleSubmit } = useForm({
  validationSchema: schema,
  initialValues: {
    email: '',
    password: '',
    rePassword: ''
  }
})
const { value: email, errorMessage: emailError } = useField('email')
const { value: password, errorMessage: passwordError } = useField('password')
const { value: rePassword, errorMessage: rePasswordError } = useField('rePassword')



function togglePassword() {
  showPassword.value = !showPassword.value
}
function toggleRePassword() {
  showRePassword.value = !showRePassword.value
}
const onSubmit = handleSubmit(async (values) => {
  try {
    const payload = {
      email: values.email,
      password: values.password
    }
    await registerUser(payload)
    const token = await loginUser(payload)
    const userMetaData = await getCurrentUser(token)
    authStore.setToken(token)
    authStore.setUser(userMetaData)
    router.push('/home')
  } catch(error) {
    console.error(`Error: ${error}`)
  }
}) 
</script>