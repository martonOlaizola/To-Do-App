import axios from 'axios'

const BASE_URL = import.meta.env.VITE_BASE_URL
const GET_ALL_FROM_USER = `${BASE_URL}/tasks/get-from-user/`
const CREATE_TASK = `${BASE_URL}/tasks/create/`
const UPDATE_TASK = `${BASE_URL}/tasks/update/`
const DELETE_TASK = `${BASE_URL}/tasks/delete/`
const DELETE_COMPLETED_TASKS = `${BASE_URL}/tasks/delete_completed`


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