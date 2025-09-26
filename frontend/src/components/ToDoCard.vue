<template>
  <div class="min-h-screen bg-gray-100 flex flex-col">
    <!-- Main content -->
    <main class="flex-1 p-6 max-w-3xl mx-auto w-full">
      <!-- Botón crear -->
      <div class="flex justify-end mb-4">
        <button
          @click="openCreateModal"
          class="px-4 py-2 bg-indigo-500 hover:bg-indigo-600 text-white rounded-md transition"
        >
          + Nueva tarea
        </button>
      </div>

      <!-- Lista de tareas -->
      <div class="space-y-4">
        <div
          v-for="task in tasks"
          :key="task.id"
          class="bg-white p-4 rounded-lg shadow flex justify-between items-center"
        >
          <div>
            <h2 class="text-lg font-semibold text-gray-800">{{ task.title }}</h2>
            <p class="text-gray-600 text-sm">{{ task.description }}</p>
            <span
              class="inline-block mt-1 px-2 py-1 text-xs rounded-full"
              :class="{
                'bg-blue-100 text-blue-600': task.type === 'trabajo',
                'bg-green-100 text-green-600': task.type === 'personal',
                'bg-yellow-100 text-yellow-600': task.type === 'estudio'
              }"
            >
              {{ task.type }}
            </span>
          </div>

          <div class="flex gap-2">
            <button
              @click="openEditModal(task)"
              class="px-2 py-1 bg-yellow-400 hover:bg-yellow-500 text-white rounded-md text-sm"
            >
              Editar
            </button>
            <button
              @click="openDeleteModal(task.id)"
              class="px-2 py-1 bg-red-500 hover:bg-red-600 text-white rounded-md text-sm"
            >
              Eliminar
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal crear/editar -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/50 flex items-center justify-center"
    >
      <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">
          {{ editMode ? 'Editar Tarea' : 'Nueva Tarea' }}
        </h2>

        <form @submit.prevent="editMode ? handleUpdateTask(selectedTaskID, selectedTask) : handleCreateTask()" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Título</label>
            <input
              v-model="title"
              type="text"
              class="mt-1 w-full border rounded-md px-3 py-2 focus:ring-2 focus:ring-indigo-400"
              :required="editMode ? false : true"
            />
          </div>


          <p v-if="errors.title" class="text-red-500 text-xs mt-1"><strong>*{{ errors.title }}*</strong></p>

          <div>
            <label class="block text-sm font-medium text-gray-700">Descripción</label>
            <textarea
              v-model="description"
              class="mt-1 w-full border rounded-md px-3 py-2 focus:ring-2 focus:ring-indigo-400"
            ></textarea>
          </div>

          <p v-if="errors.description" class="text-red-500 text-xs mt-1"><strong>*{{ errors.description }}*</strong></p>

          <div>
            <label class="block text-sm font-medium text-gray-700">Tipo</label>
            <select
              v-model="task_type"
              class="mt-1 w-full border rounded-md px-3 py-2 focus:ring-2 focus:ring-indigo-400"
            >
              <option disabled value="">Selecciona un tipo</option>
              <option value="trabajo">Trabajo</option>
              <option value="personal">Personal</option>
              <option value="estudio">Estudio</option>
            </select>
          </div>

          <p v-if="errors.type" class="text-red-500 text-xs mt-1"><strong>*{{ errors.type }}*</strong></p>

          <div class="flex justify-end gap-2">
            <button
              type="button"
              @click="closeModal"
              class="px-4 py-2 bg-gray-300 hover:bg-gray-400 rounded-md"
            >
              Cancelar
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-indigo-500 hover:bg-indigo-600 text-white rounded-md"
            >
              Guardar
            </button>
          </div>
        </form>
      </div>
    </div>
      <!-- Modal eliminar -->
        <div
        v-if="showDeleteModal"
        class="fixed inset-0 bg-black/50 flex items-center justify-center">
        <div class="bg-white rounded-lg shadow-lg p-6 w-[400px]">
          <h2 class="text-lg font-semibold text-gray-800 mb-4">
            ¿Estás seguro de eliminar esta tarea?
          </h2>
          <p class="text-gray-600 text-sm mb-6">
            Esta acción no se puede deshacer.
          </p>
          <div class="flex justify-end gap-3">
            <button
            @click="closeDeleteModal"
              class="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-md text-sm transition-colors"
            >
              Cancelar
            </button>
            <button
            type="submit"
              @click="handleDeleteTask(selectedTaskID)"
              class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-md text-sm transition-colors"
            >
              Eliminar
            </button>
          </div>
        </div>
      </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue"
import { useToast } from "vue-toastification"
import * as yup from "yup"
import { useForm, useField } from "vee-validate"
import { getAllTasksFromUser, createTask, updateTask, deleteTask } from "../services/taskService"


const tasks = ref([])
const selectedTaskID = ref(null)
const selectedTask = ref({})
const toast = useToast()
const showModal = ref(false)
const showDeleteModal = ref(false)
const editMode = ref(false)
const schema = yup.object({
  title: yup.string().max(30, "Máximo 30 caracteres."),
  description: yup.string().max(50, "Máxmimo 50 caracteres."),
})
const { handleSubmit, errors, resetForm } = useForm({
  validationSchema: schema,
  validateOnInput: true
})
const { value: title } = useField('title')
const { value: description } = useField('description')
const { value: task_type } = useField('task_type')
onMounted( async () => {
  try {
    const token = localStorage.getItem('jwt')
    const userSTR = localStorage.getItem('user')
    const user = JSON.parse(userSTR)
    tasks.value = await getAllTasksFromUser(user.id, token)
  } catch(error) {
    toast.error('Error al traer las tareas')
    console.error(`Error: ${error}`)
  }
})

function openCreateModal() {
  editMode.value = false
  resetForm()
  showModal.value = true
}

function openEditModal(task) {
  selectedTaskID.value = task.id
  selectedTask.value = task
  editMode.value = true
  resetForm({ values: task })
  showModal.value = true
}

function closeModal(){
  showModal.value = false
}

function openDeleteModal(taskID) {
  selectedTaskID.value = taskID
  showDeleteModal.value = true
}

function closeDeleteModal(){
  showDeleteModal.value = false
}


const handleCreateTask = handleSubmit(async (values) => {
  try {
    await createTask(values, token)
    toast.success('Tarea creada con exito')
    tasks.value = await getAllTasksFromUser(user.id, token)
    closeModal()
  } catch(error) {
    console.error(`Error: ${error}`)
    toast.error('Error al crear tarea')
  }
})

const handleUpdateTask = handleSubmit(async (values) => {
  try {
    await updateTask(selectedTaskID.value, values, token)
    toast.success('Tarea editada con exito')
    tasks.value = await getAllTasksFromUser(user.id, token)
    closeModal()
  } catch(error) {
    console.error(`Error: ${error}`)
    toast.error('Error al editar tarea')
  }
})

async function handleDeleteTask(taskId) {
  try {
    await deleteTask(taskId)
    toast.success('Tarea eliminada')
    tasks.value = await getAllTasksFromUser(user.id, token)
    closeDeleteModal()
  } catch(error){
    console.error(`Error: ${error}`)
    toast.error('Error eliminando la tarea')
  }
}
</script>
