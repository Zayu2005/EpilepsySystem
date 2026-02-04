
import axios from 'axios';
//定义一个变量,记录公共的前缀  ,  baseURL
const baseURL = '/api';
const instance = axios.create({baseURL})
import { ElMessage } from 'element-plus';
import { useTokenStore } from '@/stores/token.js';
import router from '@/router';

//添加请求拦截器
instance.interceptors.request.use(
    config=>{
        // 获取token的值
        const tokenStore = useTokenStore()
        const token = tokenStore.token
        if(token){
            config.headers.Authorization = token
        }
        return config;
    },
    err=>{
        return Promise.reject(err);
    }
)
//添加响应拦截器
instance.interceptors.response.use(
    result=>{

        //判断业务状态码
        if(result.data.code === 0){
            return result.data;
        }
        //操作失败

        //异步操作的状态转换为失败
        return Promise.reject(result.data);

    },
    err=>{
        if(err.response.status === 401){
            const tokenStore = useTokenStore()
            tokenStore.removeToken()
            ElMessage.error('未登录或登录状态已过期，请重新登录');
            router.push('/login')
        }else{
            ElMessage.error('服务异常');
        }
        return Promise.reject(err);//异步的状态转化成失败的状态
    }
)

export default instance;