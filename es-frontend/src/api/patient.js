

import request from '@/utils/request'

//分页查询病人
export const patientListService = (params) =>{
    return request.get('/patient',{params: params})
}


//删除病人信息

export const deletePatientService = (id) =>{
    return request.delete('/patient',{params: {id: id}})
}

//更新病人信息
export const updatePatientService = (data) =>{
    return request.put('/patient',data)
}

//增加病人信息
export const addPatientService = (data) =>{
    return request.post('/patient',data)
}

//所有的病人列表
export const patientListAllService = () =>{
    return request.get('/patient/all')
}
//填写病人诊断信息
export const addDiagnosisService = (data) =>{
    return request.put('/patient/diagnosis',data)
}


