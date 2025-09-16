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
              @click="editTask(task)"
              class="px-2 py-1 bg-yellow-400 hover:bg-yellow-500 text-white rounded-md text-sm"
            >
              Editar
            </button>
            <button
              @click="deleteTask(task.id)"
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

        <form @submit.prevent="saveTask" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Título</label>
            <input
              v-model="form.title"
              type="text"
              class="mt-1 w-full border rounded-md px-3 py-2 focus:ring-2 focus:ring-indigo-400"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Descripción</label>
            <textarea
              v-model="form.description"
              class="mt-1 w-full border rounded-md px-3 py-2 focus:ring-2 focus:ring-indigo-400"
              required
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Tipo</label>
            <select
              v-model="form.type"
              class="mt-1 w-full border rounded-md px-3 py-2 focus:ring-2 focus:ring-indigo-400"
              required
            >
              <option disabled value="">Selecciona un tipo</option>
              <option value="trabajo">Trabajo</option>
              <option value="personal">Personal</option>
              <option value="estudio">Estudio</option>
            </select>
          </div>

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
  </div>
</template>

<script setup>
import { ref } from "vue"

const tasks = ref([
  { id: 1, title: "Estudiar Vue 3", description: "Repasar Composition API", type: "estudio" },
  { id: 2, title: "Proyecto To-Do App", description: "Frontend con Vue", type: "trabajo" },
])

const showModal = ref(false)
const editMode = ref(false)
const form = ref({ id: null, title: "", description: "", type: "" })

function openCreateModal() {
  editMode.value = false
  form.value = { id: null, title: "", description: "", type: "" }
  showModal.value = true
}

function editTask(task) {
  editMode.value = true
  form.value = { ...task }
  showModal.value = true
}

function saveTask() {
  if (editMode.value) {
    const index = tasks.value.findIndex((t) => t.id === form.value.id)
    if (index !== -1) tasks.value[index] = { ...form.value }
  } else {
    tasks.value.push({
      ...form.value,
      id: Date.now(),
    })
  }
  closeModal()
}

function deleteTask(id) {
  tasks.value = tasks.value.filter((task) => task.id !== id)
}

function closeModal() {
  showModal.value = false
}
</script>
