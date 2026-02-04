import { defineStore } from 'pinia'
import {ref} from 'vue'

export const useTokenStore = defineStore('token', () => {
    const token = ref('')

    //设置token的值
    const setToken = (newToken) => {
        token.value = newToken
    }

    //删除token的值
    const removeToken = () => {
        token.value = ''
    }

    return {token, setToken, removeToken}
},
{
    persist:true
    }
)
