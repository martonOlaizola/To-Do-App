import axios from 'axios'

const BASE_URL = import.meta.env.VITE_BASE_URL
const REGISTER_URL = `${BASE_URL}/auth/create`
const LOGIN_URL = `${BASE_URL}/auth/token`
const GET_CURRENT_USER_URL = `${BASE_URL}/auth/me`

/**
 * Register a new user in the backend.
 * @param {{ email: string, password: string }} payload - Credentials provided by the form.
 * @returns {Promise<import('axios').AxiosResponse | undefined>} Axios response when successful.
 */
export async function registerUser(payload){
  try {
    const response = await axios.post(REGISTER_URL, payload)
    return response
  } catch(error){
    console.error('Error en el login: ', error.response?.data || error.message)
  }
}

/**
 * Authenticate a user and retrieve the access token.
 * @param {{ email: string, password: string }} userData - Login credentials supplied by the user.
 * @returns {Promise<string | undefined>} Bearer token returned by the backend.
 */
export async function loginUser(userData){ 
  try {
    const params = new URLSearchParams();
    params.append('username', userData.email);
    params.append('password', userData.password);
    const response = await axios.post(LOGIN_URL, params, {
      withCredentials: true
    })

    const token = response.data.access_token
    return token
  }catch (error) {
    console.error('Error en el login: ', error.response?.data || error.message)
  }
}

/**
 * Retrieve the profile of the currently authenticated user.
 * @param {string} token - Bearer token returned by the login service.
 * @returns {Promise<{ id: number, email: string } | undefined>} User metadata when the request succeeds.
 */
export async function getCurrentUser(token) {
  try {
    const response = await axios.get(GET_CURRENT_USER_URL,{
      headers: {
      'Authorization': `Bearer ${token}`,
      }
    })
    return response.data
  } catch(error) {
    console.error(`Error al traer los datos: ${error}`)
  }
}
