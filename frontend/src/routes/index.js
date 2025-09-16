import Welcome from "../pages/Welcome.vue";
import Home from "../pages/Home.vue";
import Login from "../pages/Login.vue";
import Register from "../pages/Register.vue";
import { createRouter, createWebHistory } from 'vue-router'


const routes = [
  {path: "/", component: Welcome},
  {path: "/home", component: Home},
  {path: "/login", component: Login},
  {path: "/register", component: Register}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router