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
              @click="openEditTask(task.id)"
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
              v-model="form.title"
              type="text"
              class="mt-1 w-full border rounded-md px-3 py-2 focus:ring-2 focus:ring-indigo-400"
              required
            />
          </div>

          <p v-if="errors.title" class="text-red-500 text-xs mt-1"><strong>*{{ errors.title }}*</strong></p>

          <div>
            <label class="block text-sm font-medium text-gray-700">Descripción</label>
            <textarea
              v-model="form.description"
              class="mt-1 w-full border rounded-md px-3 py-2 focus:ring-2 focus:ring-indigo-400"
            ></textarea>
          </div>

          <p v-if="errors.description" class="text-red-500 text-xs mt-1"><strong>*{{ errors.description }}*</strong></p>

          <div>
            <label class="block text-sm font-medium text-gray-700">Tipo</label>
            <select
              v-model="form.task_type"
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
import { getAllTasksFromUser, createTask, updateTask, deleteTask } from "../services/taskService"
import { useToast } from "vue-toastification"

const tasks = ref([])
const selectedTaskID = ref(null)
const selectedTask = ref({})
const toast = useToast()
const showModal = ref(false)
const showDeleteModal = ref(false)
const editMode = ref(false)
const form = ref({ id: null, title: "", description: "", task_type: "" })
const errors = ref({title: '', description: '', type: ''})

onMounted( async () => {
  try {
    const userSTR = localStorage.getItem('user')
    const user = JSON.parse(userSTR)
    tasks.value = await getAllTasksFromUser(user.id)
  } catch(error) {
    toast.error('Error al traer las tareas')
    console.error(`Error: ${error}`)
  }
})

function openCreateModal() {
  editMode.value = false
  form.value = { id: null, title: "", description: "", type: "" }
  showModal.value = true
}

function openEditTask(taskId) {
  selectedTaskID.value = taskId
  editMode.value = true
  showModal.value = true
  selectedTask.value = form.value
}

function openDeleteModal(taskID) {
  selectedTaskID.value = taskID
  showDeleteModal.value = true
}

function closeDeleteModal(){
  showDeleteModal.value = false
}

function validateForm(){
  errors.value = {title: '', description: '', type: ''}
  if (form.value.title.length > 30) errors.value.title = 'Máximo 30 caracteres.'
  if (form.value.description.length > 50) errors.value.description = 'Máximo 50 caracteres'
  const stop = Object.keys(errors.value).length === 0 ? true : false
  return stop
}

async function handleCreateTask() {
  debugger
  if (!validateForm()) {
    return
  }
  selectedTask.value = form.value
  await createTask(selectedTask.value)
}

async function handleUpdateTask(taskId, task) {
  if (!validateForm()) return
  await updateTask(taskId, task)
  closeModal()
}

async function handleDeleteTask(taskId) {
  await deleteTask(taskId)
  window.location.reload()
}

function closeModal() {
  showModal.value = false
}
</script>
