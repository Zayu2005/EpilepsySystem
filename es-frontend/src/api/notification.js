import request from '@/utils/request'


//新建通知
export const addNotificationService = (data) => {
    return request.post('/notification', data)
}

export const getNotificationsService=() => {
    return request.get('/notification/list')
}