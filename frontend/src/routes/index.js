import Welcome from "../pages/Welcome.vue";
import Home from "../pages/Home.vue";
import Login from "../pages/Login.vue";
import Register from "../pages/Register.vue";
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from "../stores/authStore";


const routes = [
  {path: "/", component: Welcome},
  {path: "/home", component: Home, meta: {requiresAuth: true}},
  {path: "/login", component: Login},
  {path: "/register", component: Register}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return "/"
  }
  return true
})

export default router