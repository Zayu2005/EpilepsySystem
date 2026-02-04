// import './assets/main.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { createPersistedState } from 'pinia-persistedstate-plugin'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
const app = createApp(App)
const pinia = createPinia() 
const persist = createPersistedState()  //Pinia持久化插件


pinia.use(persist)
app.use(pinia)
app.use(router)
app.use(ElementPlus,{
  locale: zhCn
})
app.mount('#app')
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }