import axios from 'axios'

const BASE_URL = import.meta.env.VITE_BASE_URL
const GET_ALL_FROM_USER = `${BASE_URL}/tasks/get-from-user/`
const CREATE_TASK = `${BASE_URL}/tasks/create/`
const UPDATE_TASK = `${BASE_URL}/tasks/update/`
const DELETE_TASK = `${BASE_URL}/tasks/delete/`
const DELETE_COMPLETED_TASKS = `${BASE_URL}/tasks/delete_completed`


/**
 * Fetch every task that belongs to the provided user.
 * @param {number} userID - Identifier of the task owner.
 * @param {string} token - Bearer token used to authorize the request.
 * @returns {Promise<Array<Record<string, unknown>> | undefined>} Collection of tasks when successful.
 */
export async function getAllTasksFromUser(userID, token){
  try {
    const response = await axios.get(`${GET_ALL_FROM_USER}${userID}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },}
    )
    return response.data
  } catch(error){
    console.error(`Error al traer tareas: ${error}`)
  }
}

/**
 * Create a new task for the authenticated user.
 * @param {{ title: string, description?: string, task_type: string, completed?: boolean }} taskData - Task payload.
 * @param {string} token - Bearer token used to authorize the request.
 * @returns {Promise<void>} Resolves when the request completes.
 */
export async function createTask(taskData, token) {
  try {
    const response = await axios.post(CREATE_TASK, taskData,{
      headers: {
      'Authorization': `Bearer ${token}` 
      }
    })
  } catch(error) {
    console.error(`Error: ${error}`)
  }
}

/**
 * Update an existing task with new information.
 * @param {number} taskID - Identifier of the task to update.
 * @param {Record<string, unknown>} task - Partial payload with the fields to update.
 * @param {string} token - Bearer token used to authorize the request.
 * @returns {Promise<Record<string, unknown> | undefined>} Updated task data returned by the backend.
 */
export async function updateTask(taskID, task, token){
  try {
    const response = await axios.put(`${UPDATE_TASK}${taskID}`, task, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    return response.data
  } catch(error) {
    console.error(`Error: ${error}`)
  }
}

/**
 * Delete a task owned by the authenticated user.
 * @param {number} taskID - Identifier of the task to remove.
 * @param {string} token - Bearer token used to authorize the request.
 * @returns {Promise<Record<string, unknown> | undefined>} Backend response confirming the deletion.
 */
export async function deleteTask(taskID, token){
  try {
    const response = await axios.delete(`${DELETE_TASK}${taskID}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    return response.data
  } catch(error) {
    console.error(`Error: ${error}`)
  }
}

/**
 * Delete every completed task associated with the authenticated user.
 * @param {string} token - Bearer token used to authorize the request.
 * @returns {Promise<Record<string, unknown> | undefined>} Backend response confirming the deletion.
 */
export async function deleteCompletedTasks(token) {
  try {
    const response = await axios.delete(DELETE_COMPLETED_TASKS, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    return response.data
  } catch(error) {
    console.error(`Error: ${error}`)
  }
}
