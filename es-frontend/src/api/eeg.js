import request from '@/utils/request'

/**
 * 获取EEG记录列表
 * @param {Object} params - 查询参数
 * @returns {Promise} 返回EEG记录列表
 */
export const eegListService = (params) => {
    return request.get('/eeg', { params: params })
}

/**
 * 删除指定的EEG记录
 * @param {string|number} id - EEG记录ID
 * @returns {Promise} 返回删除操作结果
 */
export const deleteEegService = (id) => {
    return request.delete('/eeg', { params: { id: id } })
}

/**
 * 更新EEG记录信息
 * @param {Object} data - 更新的EEG记录数据
 * @returns {Promise} 返回更新操作结果
 */
export const updateEegService = (data) => {
    return request.put('/eeg', data)
}

/**
 * 添加新的EEG记录
 * @param {Object} data - 新EEG记录数据
 * @returns {Promise} 返回添加操作结果
 */
export const addEegService = (data) => {
    return request.post('/eeg', data)
}

/**
 * 获取指定EEG记录的数据
 * @param {string|number} id - EEG记录ID
 * @returns {Promise} 返回EEG数据
 */
export const getEegDataService = (id) => {
    return request.get('/eeg/data', { params: { id: id } })
}

/**
 * 上传EEG文件
 * @param {File} file - 要上传的EEG文件
 * @returns {Promise} 返回上传操作结果
 */
export const uploadEegService = (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return request.post('/eeg/upload', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}

/**
 * 获取指定EEG记录的分析结果
 * @param {string|number} id - EEG记录ID
 * @returns {Promise} 返回EEG分析结果
 */
export const getEegAnalysisService = (params) => {
    return request.get('/eeg/analysis', { params: params } )
}



//分页查询EEG的分析记录
export const getEegAnalysisListService = (params) => {
    return request.get('/eeg/analysisList', { params: params })
}