import { createApp } from 'vue'
import App from './App.vue'
import Toast from 'vue-toastification'
import "vue-toastification/dist/index.css"
import './style.css'
import router from './routes'


const app = createApp(App)

app.use(router)
app.use(Toast, {
  transition: "Vue-Toastification__bounce",
  maxToasts: 20,
  newestOnTop: true,
  position: "bottom-right",
  timeout: 2989,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: false,
  draggablePercent: 0.1,
  showCloseButtonOnHover: false,
  hideProgressBar: true,
  closeButton: "button",
  icon: true,
  rtl: false
})
app.mount('#app')