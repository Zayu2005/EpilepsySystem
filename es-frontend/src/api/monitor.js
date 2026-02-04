import request from '@/utils/request.js'

/**
 * 获取监控数据
 * @param {Object} params - 查询参数
 * @returns {Promise} 返回监控数据
 */
export const getMonitorData = (params) => {
    // 模拟API调用，实际项目中应该连接到后端API
    return new Promise((resolve) => {
        setTimeout(() => {
            // 生成模拟数据
            const data = generateMockMonitorData(params)
            resolve({
                code: 0,
                data: data
            })
        }, 500) // 模拟网络延迟
    })
}

/**
 * 获取首页统计数据
 * @returns {Promise} 返回统计数据
 */
export const getHomeStats = () => {
    // 模拟API调用
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({
                code: 0,
                data: {
                    patientCount: 128,
                    todayAppointments: 24,
                    emergencyCount: 5,
                    abnormalCount: 8
                }
            })
        }, 300)
    })
}

/**
 * 生成模拟监控数据
 * @param {Object} params - 查询参数
 * @returns {Array} 返回模拟监控数据
 */
const generateMockMonitorData = (params) => {
    const rooms = [
        { roomNo: '301', patientName: '陈长' },
        { roomNo: '302', patientName: '孙洲男' },
        { roomNo: '303', patientName: '周立安' },
        { roomNo: '304', patientName: '陈静宜' },
        { roomNo: '305', patientName: '林宇轩' },
        { roomNo: '306', patientName: '张悦' },
        { roomNo: '307', patientName: '刘昊然' },
        { roomNo: '308', patientName: '王红阳' }
    ]

    // 生成当前时间
    const now = new Date()
    const timeString = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`
    const dateString = `${now.getFullYear()}-${(now.getMonth() + 1).toString().padStart(2, '0')}-${now.getDate().toString().padStart(2, '0')}`
    
    // 为每个房间生成脑电波数据
    const result = rooms.map(room => {
        // 随机生成脑电波值和状态
        const eegValue = generateEegValue(room.roomNo)
        const status = getStatusByEegValue(eegValue)
        
        return {
            ...room,
            eegValue: eegValue.toFixed(1),
            status: status,
            lastUpdate: `${dateString} ${timeString}`
        }
    })
    
    // 如果是异常监测模式，只返回异常数据
    if (params && params.type === 'warning') {
        return result.filter(item => item.status !== '正常')
    }
    
    return result
}

/**
 * 根据房间号生成模拟脑电波值
 * 不同房间有不同的基础值和波动范围，以模拟不同患者状态
 * @param {string} roomNo - 房间号
 * @returns {number} 返回模拟脑电波值
 */
const generateEegValue = (roomNo) => {
    // 为不同房间设置不同的基础值和波动范围
    const roomSettings = {
        '301': { base: 45, range: 10 },  // 正常范围
        '302': { base: 65, range: 15 },  // 轻度异常
        '303': { base: 40, range: 8 },   // 正常范围
        '304': { base: 85, range: 10 },  // 严重异常
        '305': { base: 50, range: 12 },  // 正常范围
        '306': { base: 75, range: 15 },  // 中度异常
        '307': { base: 55, range: 10 },  // 正常范围
        '308': { base: 90, range: 5 }    // 严重异常
    }
    
    // 获取房间设置，如果没有特定设置则使用默认值
    const setting = roomSettings[roomNo] || { base: 50, range: 10 }
    
    // 生成随机波动值
    const fluctuation = (Math.random() * 2 - 1) * setting.range
    
    // 返回基础值加波动值
    return Math.max(0, Math.min(100, setting.base + fluctuation))
}

/**
 * 根据脑电波值确定状态
 * @param {number} value - 脑电波值
 * @returns {string} 返回状态描述
 */
const getStatusByEegValue = (value) => {
    if (value > 80) return '异常'
    if (value > 60) return '警告'
    return '正常'
}