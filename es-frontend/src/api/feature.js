import request from '@/utils/request'


/**
 * 上传EEG文件
 * @param {File} file - 要上传的EEG文件
 * @returns {Promise} 返回上传操作结果
 */

export const uploadEegService = (data) => {
    const formData = new FormData()
    formData.append('file', data.file)
    formData.append('patientId', data.patientId)
    formData.append('userId', data.userId)

    return request.post('/feature/upload', formData)
}

//获得Eeg可视化特征分析
export const getEegFeaturesService=(params)=>{
    return request.get('/feature/analysis',{params})
}
