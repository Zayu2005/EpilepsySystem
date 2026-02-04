


import request from '@/utils/request.js'

//提供调用登录接口的函数
export const userLoginService = (loginData) =>{
    const params = new URLSearchParams();
    for(let key in loginData){
        params.append(key,loginData[key])
    }

    return request.post('/user/login', params)
}
// 提供测试接口的函数
export const testService = () =>{
    return request.get('/user/test')
}

// 提供获取用户信息的函数
export const userInfoService = () =>{
    return request.get('/user/info')
}

// 提供获取患者数量的函数
export const userCountService = () =>{
    return request.get('/user/count')
}

// 提供获取用户列表的函数
export const userListService = (params) =>{
    return request.get('/user/list',{params: params})
}

// 提供添加用户的函数
export const addUserService = (data) =>{
    return request.post('/user/register',data)
}

// 提供修改用户状态的函数
export const userStatusChangeService = (params) =>{
    return request.post('/user/status',params)
}

// 提供修改用户信息的函数
export const updateUserService = (data) =>{
    return request.post('/user/update',data)
}


