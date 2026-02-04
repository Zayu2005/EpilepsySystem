import request from '@/utils/request.js'


//ToDo待办接口

// 获取待办事项列表
export const getTodoListService = (params) => {
    return request.get('/todo/list',{ params: params})
}

// 添加待办事项
export const addTodoService = (data) => {
    return request.post('/todo/add', data)
}

// 更新待办事项状态
export const updateTodoStatusService = (params) => {
    return request.put('/todo/status', null, { params })  // 修正
}

// 删除待办事项
export const deleteTodoService = (id) => {
    return request.delete(`/todo/delete/${id}`)  // 使用反引号
}
