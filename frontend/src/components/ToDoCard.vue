<template>
  <div class="min-h-screen bg-gray-100 flex flex-col">
    <!-- Main content -->
    <main class="flex-1 p-6 max-w-3xl mx-auto w-full">
      <!-- Acciones -->
      <div class="flex justify-end mb-4 gap-2">
        <button
          type="button"
          @click="completeSelectedTasks"
          :disabled="!selectedTaskIds.length"
          class="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-md transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Completar
        </button>
        <button
          @click="handleDeleteCompletedTasks"
          class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-md transition disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="!areCompleted"
        >
        Eliminar completadas
        </button>
        <button
          type="button"
          class="flex items-center gap-2 px-4 py-2 border-2 border-dashed border-red-300 text-red-500 rounded-md transition hover:bg-red-50"
          :class="{ 'border-red-500 bg-red-100 text-red-600 shadow-inner scale-105': isTrashActive }"
          @dragenter.prevent="handleTrashDragOver"
          @dragover.prevent="handleTrashDragOver"
          @dragleave="handleTrashDragLeave"
          @drop.prevent="handleTrashDrop"
          aria-label="Soltar tareas aqui para eliminarlas"
        >
          <i class="fa-solid fa-trash"></i>
          Papelera
        </button>
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
          :class="[
            'p-4 rounded-lg shadow flex items-start justify-between gap-4 border transition-colors duration-200 cursor-grab select-none',
            task.completed ? 'bg-slate-50 border-green-200' : 'bg-white border-transparent',
            draggingTaskId === task.id ? 'opacity-60 cursor-grabbing' : '',
            dragOverTaskId === task.id && draggingTaskId !== task.id ? 'border-indigo-300 bg-indigo-50' : ''
          ]"
          draggable="true"
          @dragstart="handleDragStart(task.id, $event)"
          @dragenter="handleDragEnter(task.id)"
          @dragover.prevent
          @drop.prevent="handleDropOnTask(task.id)"
          @dragend="handleDragEnd"
        >
          <div class="flex items-start gap-3">
            <Checkbox
              v-model="selectedTaskIds"
              :value="task.id"
            />
            <div>
              <h2 :class="['text-lg font-semibold', task.completed ? 'text-gray-500 line-through' : 'text-gray-800']">{{ task.title }}</h2>
              <p :class="['text-sm', task.completed ? 'text-gray-400' : 'text-gray-600']">{{ task.description }}</p>
              <span
                :class="[
                  'inline-block mt-1 px-2 py-1 text-xs rounded-full transition-colors duration-200',
                  task.completed ? 'opacity-70 ring-1 ring-green-200' : '',
                  {
                    'bg-blue-100 text-blue-600': task.type === 'trabajo',
                    'bg-green-100 text-green-600': task.type === 'personal',
                    'bg-yellow-100 text-yellow-600': task.type === 'estudio'
                  }
                ]"
              >
                {{ task.type }}
              </span>
            </div>
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
              required="true"
              class="mt-1 w-full border rounded-md px-3 py-2 focus:ring-2 focus:ring-indigo-400"
            >
              <option disabled value="">Selecciona un tipo</option>
              <option value="trabajo">Trabajo</option>
              <option value="personal">Personal</option>
              <option value="estudio">Estudio</option>
            </select>
          </div>

          <p v-if="errors.type" class="text-red-500 text-xs mt-1"><strong>*{{ errors.type }}*</strong></p>

          <div class="flex justify-end gap-3">
            <button
              type="button"
              @click="closeModal"
              class="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-md text-sm transition-colors"
            >
              Cancelar
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-indigo-500 hover:bg-indigo-600 text-white rounded-md text-sm transition-colors"
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
      class="fixed inset-0 bg-black/50 flex items-center justify-center"
    >
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
import { computed, onMounted, ref } from "vue"
import { useToast } from "vue-toastification"
import * as yup from "yup"
import { useForm, useField } from "vee-validate"
import Checkbox from "./Checkbox.vue"
import { getAllTasksFromUser, createTask, updateTask, deleteTask, deleteCompletedTasks } from "../services/taskService"
import { useAuthStore } from "../stores/authStore"

const authStore = useAuthStore()

const tasks = ref([])
const selectedTaskIds = ref([])
const selectedTaskID = ref(null)
const selectedTask = ref({})
const toast = useToast()
const showModal = ref(false)
const showDeleteModal = ref(false)
const editMode = ref(false)
const draggingTaskId = ref(null)
const dragOverTaskId = ref(null)
const isTrashActive = ref(false)
const taskOrder = ref([])

const schema = yup.object({
  title: yup.string().max(30, "Máximo 30 caracteres."),
  description: yup.string().max(50, "Máximo 50 caracteres."),
})

const { handleSubmit, errors, resetForm } = useForm({
  validationSchema: schema,
  validateOnInput: true
})

const { value: title } = useField("title")
const { value: description } = useField("description")
const { value: task_type } = useField("task_type")

/**
 * Determine if the environment exposes window.localStorage.
 * @returns {boolean} True when local storage APIs are available.
 */
function hasLocalStorageSupport() {
  return typeof window !== "undefined" && typeof window.localStorage !== "undefined"
}

/**
 * Build the storage key used to persist the user's task order.
 * @returns {string} Composite key combining the user id and the prefix.
 */
function getOrderStorageKey() {
  const userId = authStore.user?.id ?? "default"
  return `task-order-${userId}`
}

/**
 * Restore the task ordering persisted in local storage.
 * @returns {void}
 */
function loadTaskOrder() {
  if (!hasLocalStorageSupport()) {
    return
  }
  try {
    const raw = window.localStorage.getItem(getOrderStorageKey())
    if (!raw) {
      return
    }
    const parsed = JSON.parse(raw)
    if (Array.isArray(parsed)) {
      taskOrder.value = parsed
    }
  } catch (error) {
    console.error("Error cargando el orden de las tareas", error)
  }
}

/**
 * Persist the in-memory ordering of tasks to local storage.
 * @returns {void}
 */
function persistTaskOrder() {
  if (!hasLocalStorageSupport()) {
    return
  }
  try {
    window.localStorage.setItem(getOrderStorageKey(), JSON.stringify(taskOrder.value))
  } catch (error) {
    console.error("Error guardando el orden de las tareas", error)
  }
}

/**
 * Merge fetched tasks with the stored order preference.
 * @param {Array<{ id: number }>} fetchedTasks - Tasks retrieved from the backend.
 * @returns {void}
 */
function setTasksWithOrder(fetchedTasks = []) {
  const fetchedIds = fetchedTasks.map(task => task.id)
  const orderedIds = taskOrder.value.filter(id => fetchedIds.includes(id))
  const missingIds = fetchedIds.filter(id => !orderedIds.includes(id))
  taskOrder.value = [...orderedIds, ...missingIds]
  tasks.value = taskOrder.value
    .map(id => fetchedTasks.find(task => task.id === id))
    .filter(Boolean)
  selectedTaskIds.value = selectedTaskIds.value.filter(id => taskOrder.value.includes(id))
  persistTaskOrder()
}

/**
 * Fetch tasks for the current user and update the local state.
 * @param {{ showErrorToast?: boolean }} [options] - Control error feedback behaviour.
 * @returns {Promise<void>} Resolves when the tasks refresh completes.
 */
async function refreshTasks({ showErrorToast = false } = {}) {
  const token = authStore.token
  const user = authStore.user

  if (!user || typeof user.id === "undefined") {
    return
  }

  const fetchedTasks = await getAllTasksFromUser(user.id, token)

  if (!Array.isArray(fetchedTasks)) {
    if (showErrorToast) {
      toast.error("Error al traer las tareas")
    }
    return
  }

  setTasksWithOrder(fetchedTasks)
}

onMounted(async () => {
  loadTaskOrder()
  await refreshTasks({ showErrorToast: true })
})

/**
 * Indicate whether there is at least one completed task.
 * @type {import('vue').ComputedRef<boolean>}
 */
const areCompleted = computed(() => tasks.value.some(task => task.completed))

/**
 * Prepare the form for creating a new task and display the modal.
 * @returns {void}
 */
function openCreateModal() {
  editMode.value = false
  resetForm()
  showModal.value = true
}

/**
 * Load an existing task into the form for editing.
 * @param { id: number } & Record<string, unknown>} task - Task selected by the user.
 * @returns {void}
 */
function openEditModal(task) {
  selectedTaskID.value = task.id
  selectedTask.value = task
  editMode.value = true
  resetForm({ values: task })
  showModal.value = true
}

/**
 * Hide the task modal without persisting changes.
 * @returns {void}
 */
function closeModal(){
  showModal.value = false
}

/**
 * Ask the user to confirm the deletion of the selected task.
 * @param {number} taskID - Identifier of the task to remove.
 * @returns {void}
 */
function openDeleteModal(taskID) {
  selectedTaskID.value = taskID
  showDeleteModal.value = true
}

/**
 * Dismiss the delete confirmation modal.
 * @returns {void}
 */
function closeDeleteModal(){
  showDeleteModal.value = false
}

/**
 * Mark the selected tasks as completed in bulk.
 * @returns {Promise<void>} Resolves after the backend update finishes.
 */
async function completeSelectedTasks(){
  if (!selectedTaskIds.value.length) {
    return
  }

  const pendingIds = selectedTaskIds.value.filter(id => {
    const task = tasks.value.find(taskItem => taskItem.id === id)
    return task && !task.completed
  })

  if (!pendingIds.length) {
    selectedTaskIds.value = []
    toast.info('Las tareas seleccionadas ya estaban completadas')
    return
  }

  try {
    const token = authStore.token

    await Promise.all(pendingIds.map(async id => {
      await updateTask(id, { completed: true }, token)
    }))

    toast.success('Tareas marcadas como completadas')
    selectedTaskIds.value = []
    await refreshTasks({ showErrorToast: true })
  } catch(error) {
    console.error(`Error: ${error}`)
    toast.error('Error al completar tareas')
  }
}

/**
 * Submit a new task once the creation form lints successfully.
 * @param { title?: string, description?: string, task_type: string, completed?: boolean } values - Validated form payload.
 * @returns {Promise<void>} Resolves after the task list is refreshed.
 */
const handleCreateTask = handleSubmit(async (values) => {
  try {
    const token = authStore.token

    await createTask(values, token)
    toast.success('Tarea creada con exito')
    closeModal()
    await refreshTasks({ showErrorToast: true })
  } catch(error) {
    console.error(`Error: ${error}`)
    toast.error('Error al crear tarea')
  }
})

/**
 * Persist edits made to the currently selected task.
 * @param { title?: string, description?: string, task_type?: string, completed?: boolean } values - Validated form payload.
 * @returns {Promise<void>} Resolves after the task list reflects the changes.
 */
const handleUpdateTask = handleSubmit(async (values) => {
  try {
    const token = authStore.token
    
    await updateTask(selectedTaskID.value, values, token)
    toast.success('Tarea editada con exito')
    closeModal()
    await refreshTasks({ showErrorToast: true })
  } catch(error) {
    console.error(`Error: ${error}`)
    toast.error('Error al editar tarea')
  }
})

/**
 * Permanently delete a single task after confirmation.
 * @param {number} taskId - Identifier of the task to remove.
 * @returns {Promise<void>} Resolves once the deletion request finishes.
 */
async function handleDeleteTask(taskId) {
  try {
    const token = authStore.token

    await deleteTask(taskId, token)
    toast.success('Tarea eliminada')
    closeDeleteModal()
    await refreshTasks({ showErrorToast: true })
  } catch(error){
    console.error(`Error: ${error}`)
    toast.error('Error eliminando la tarea')
  }
}

/**
 * Remove every task marked as completed for the current user.
 * @returns {Promise<void>} Resolves after the tasks are deleted and refreshed.
 */
async function handleDeleteCompletedTasks() {
  try {
    const token = authStore.token

    await deleteCompletedTasks(token)
    toast.success('Tareas eliminadas')
    await refreshTasks({ showErrorToast: true })
  } catch(error) {
    console.error(`Error: ${error}`)
    toast.error('Error eliminando las tareas')
  }
}

/**
 * Begin dragging a task card and prepare drag metadata.
 * @param {number} taskId - Identifier of the dragged task.
 * @param {DragEvent} event - Native drag event fired by the browser.
 * @returns {void}
 */
function handleDragStart(taskId, event) {
  draggingTaskId.value = taskId
  dragOverTaskId.value = null
  if (event?.dataTransfer) {
    event.dataTransfer.effectAllowed = 'move'
    event.dataTransfer.setData('text/plain', String(taskId))
  }
}

/**
 * Highlight the drop target when another task is dragged over it.
 * @param {number} taskId - Identifier of the task currently under the cursor.
 * @returns {void}
 */
function handleDragEnter(taskId) {
  if (draggingTaskId.value === null || taskId === draggingTaskId.value) {
    return
  }
  dragOverTaskId.value = taskId
}

/**
 * Reorder the task list when a card is dropped on another card.
 * @param {number} targetId - Identifier of the task that received the drop.
 * @returns {void}
 */
function handleDropOnTask(targetId) {
  if (draggingTaskId.value === null || targetId === draggingTaskId.value) {
    handleDragEnd()
    return
  }

  const currentTasks = [...tasks.value]
  const fromIndex = currentTasks.findIndex(task => task.id === draggingTaskId.value)
  const toIndex = currentTasks.findIndex(task => task.id === targetId)

  if (fromIndex === -1 || toIndex === -1) {
    handleDragEnd()
    return
  }

  const [movedTask] = currentTasks.splice(fromIndex, 1)
  currentTasks.splice(toIndex, 0, movedTask)

  tasks.value = currentTasks
  taskOrder.value = currentTasks.map(task => task.id)
  persistTaskOrder()
  handleDragEnd()
}

/**
 * Clear drag state once the drag-and-drop interaction finishes.
 * @returns {void}
 */
function handleDragEnd() {
  draggingTaskId.value = null
  dragOverTaskId.value = null
  isTrashActive.value = false
}

/**
 * Activate the trash drop zone while a task is dragged over it.
 * @param {DragEvent} event - Native drag event containing data transfer info.
 * @returns {void}
 */
function handleTrashDragOver(event) {
  if (draggingTaskId.value === null) {
    return
  }
  if (event?.dataTransfer) {
    event.dataTransfer.dropEffect = 'move'
  }
  isTrashActive.value = true
}

/**
 * Reset the trash drop zone when the pointer leaves the area.
 * @returns {void}
 */
function handleTrashDragLeave() {
  isTrashActive.value = false
}

/**
 * Permanently delete the currently dragged task using the trash zone.
 * @returns {Promise<void>} Resolves after the deletion and refresh complete.
 */
async function handleTrashDrop() {
  if (draggingTaskId.value === null) {
    handleDragEnd()
    return
  }

  const taskId = draggingTaskId.value
  const token = authStore.token

  taskOrder.value = taskOrder.value.filter(id => id !== taskId)
  tasks.value = tasks.value.filter(task => task.id !== taskId)
  selectedTaskIds.value = selectedTaskIds.value.filter(id => id !== taskId)
  persistTaskOrder()
  handleDragEnd()

  try {
    await deleteTask(taskId, token)
    toast.success('Tarea eliminada')
    await refreshTasks({ showErrorToast: true })
  } catch(error) {
    console.error(`Error: ${error}`)
    toast.error('Error eliminando la tarea')
    await refreshTasks({ showErrorToast: true })
  }
}
</script>
