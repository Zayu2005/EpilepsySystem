import {createRouter, createWebHistory} from 'vue-router'

// 修改后
import { useTokenStore } from '../stores/token.js'
import { ElMessage } from 'element-plus'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/chat',
            name:'chat',
            component:() => import('../views/Chat.vue'),
            meta:{
                title:'AI辅助诊断'
            }
        },
        {
            path: '/test',
            name:'test',
            component:() => import('../views/test.vue'),
            meta:{
                title:'test'
            }
        },
        {
            path: '/account',
            name: 'account',
            component: () => import('../views/Account.vue'),
            meta: {
                title: '账号管理'
            }
        },
        {
            path: '/login',
            name: 'login',
            meta: {
                title: '登录',
            },
            component: () => import('../views/Login.vue'),
        },
        {
            path: '/',
            name: 'manager',
            meta: {
                title: '首页',
            },
            redirect: '/home',
            component: () => import('../views/Manager.vue'),
            children: [
                {
                    path: '/analysis',
                    name:'analysis',
                    component:() => import('../views/Analysis.vue'),
                    meta:{
                        title:'可视化分析'
                    }
                },
                {
                    path: '/home',
                    name: 'home',
                    meta: {
                        title: '首页',
                    },
                    component: () => import('../views/Home.vue'),
                },
                {
                    path: '/patient',
                    name: 'patient',
                    meta: {
                        title: '患者管理',
                    },
                    component: () => import('../views/Patient.vue'),
                },
                {
                    path: '/ward',
                    name: 'ward',
                    component: () => import('../views/Ward.vue'),
                    meta: {
                        title: '病房监控'
                    }
                },
                {
                    path: '/eeg',
                    name: 'eeg',
                    component: () => import('../views/Eeg.vue'),
                    meta: {
                        title: 'EEG分析'
                    }
                },
                {
                    path: '/mri',
                    name: 'mri',
                    component: () => import('../views/Mri.vue'),
                    meta: {
                        title: 'MRI分析'
                    }
                },
                {
                    path: '/edf',
                    name: 'edf',
                    component: () => import('../views/EdfView.vue'),
                    meta: {
                        title: 'EDF分析'
                    }
                },
                {
                    path: '/virtual-assistant',
                    name: 'VirtualAssistant',
                    component: () => import('@/views/VirtualAssistant.vue'),
                    meta: {
                        requiresAuth: true,
                        title: '智能医疗助手'
                    }
                },
                {
                    path: '/data',
                    name:'数据分析',
                    component:() => import('../views/DataView.vue'),
                    meta:{
                        title:'数据分析'
                    }
                }
            ]   
             
        }

    ],
})

router.beforeEach((to, from, next) => {
    // 设置页面标题
    if (to.meta.title) {
        document.title = to.meta.title
    }

    // 获取token
    const tokenStore = useTokenStore()
    const token = tokenStore.token

    // 白名单路由，不需要验证token
    const whiteList = ['/login','/data']

    if (whiteList.includes(to.path)) {
        // 如果是白名单页面，直接放行
        next()
    } else {
        if (!token) {
            // 如果没有token，重定向到登录页
            next('/login')
        } else {
            next()
        }
    }
})

// 路由切换后的处理
router.afterEach((to, from) => {
    // 如果路由确实发生了变化，且不是首次加载
    if (from.path !== '/' && from.path !== to.path) {
    }
})

// 路由错误处理
router.onError((error) => {
    console.log('路由错误:', error)
    // 可以添加错误提示
    ElMessage.error('页面加载失败，请重试')
})

export default router
