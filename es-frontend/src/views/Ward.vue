<template>
  <div class="ward-container">
    <!-- 顶部控制栏 -->
    <el-card class="control-panel">
      <div class="panel-header">
        <div class="room-selector">
          <span class="label" style="width: 200px;">当前病房：</span>
          <el-select v-model="currentRoom" placeholder="选择病房" @change="handleRoomChange">
            <el-option v-for="room in rooms" :key="room.id" :label="room.name" :value="room.id" />
          </el-select>
        </div>
        <div class="status-indicator" :class="monitorStatus">
          <el-icon><VideoCamera /></el-icon>
          {{ monitorStatus === 'online' ? '监控正常' : '监控异常' }}
        </div>
      </div>
    </el-card>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 左侧：病房信息 -->
      <el-card class="side-card room-info" style="height: 449px;">
        <template #header>
          <div class="card-header">
            <span>病房信息</span>
            <el-tag :type="roomStatus.type">{{ roomStatus.text }}</el-tag>
          </div>
        </template>
        <div class="info-content">
          <div class="info-item">
            <span class="label">病房号：</span>
            <span>{{ wardInfo.roomNo }}</span>
          </div>
          <div class="info-item">
            <span class="label">床位数：</span>
            <span>{{ wardInfo.bedCount }}</span>
          </div>
          <div class="info-item">
            <span class="label">主治医生：</span>
            <span>{{ wardInfo.doctor }}</span>
          </div>
          <div class="info-item">
            <span class="label">值班护士：</span>
            <span>{{ wardInfo.nurse }}</span>
          </div>
        </div>
      </el-card>

      <!-- 中央：视频监控 -->
      <div class="monitor-container" style="height: 450px; width: auto">
        <el-card class="monitor-card">
          <template #header>
            <div class="card-header">
              <span>实时监控</span>
            </div>
          </template>
          <div class="video-wrapper">
            <div class="video-placeholder" v-if="!videoUrl">
              <el-icon><VideoCamera /></el-icon>
              <span>正在连接监控画面...</span>
            </div>
            <video 
              ref="videoElement" 
              v-else 
              :src="videoUrl" 
              autoplay 
              muted
              loop
              disablePictureInPicture
              controlsList="nodownload noplaybackrate"
            ></video>
          </div>
        </el-card>
      </div>

      <!-- 右侧：患者数据 -->
      <el-card class="side-card patient-data" style="height: 448px;">
        <template #header>
          <div class="card-header">
            <span>患者实时数据</span>
            <el-button type="primary" link @click="refreshData">
              <el-icon><Refresh /></el-icon>
            </el-button>
          </div>
        </template>
        <div class="vital-signs">
          <div class="vital-item">
            <div class="vital-label">心率</div>
            <div class="vital-value" :class="getVitalClass(vitals.heartRate, 60, 100)">
              {{ vitals.heartRate }} <span class="unit">bpm</span>
            </div>
          </div>
          <div class="vital-item">
            <div class="vital-label">血压</div>
            <div class="vital-value" :class="getVitalClass(vitals.bloodPressure, 90, 140)">
              {{ vitals.bloodPressure }} <span class="unit">mmHg</span>
            </div>
          </div>
          <div class="vital-item">
            <div class="vital-label">体温</div>
            <div class="vital-value" :class="getVitalClass(vitals.temperature, 36, 37.2)">
              {{ vitals.temperature }} <span class="unit">°C</span>
            </div>
          </div>
          <div class="vital-item">
            <div class="vital-label">血氧</div>
            <div class="vital-value" :class="getVitalClass(vitals.oxygen, 95, 100)">
              {{ vitals.oxygen }} <span class="unit">%</span>
            </div>
          </div>
        </div>
      </el-card>  
    </div>

    <!-- 脑电图区域 -->
    <el-card class="eeg-section" style="margin-top: -50px;">
      <EegData/>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { Download } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { 
  VideoCamera, 
  FullScreen, 
  VideoPlay, 
  Camera, 
  Refresh,
  Sunny,
  Lightning,
  Monitor,
  Notification
} from '@element-plus/icons-vue'
import EegData from '@/components/EegData.vue'


// 视频 URL - 修改为对象映射，根据病房ID显示不同视频
const videoUrls = ref({
  1: 'http://cloud.epilepsy-detect.xyz/video3.mp4',
  2: 'http://cloud.epilepsy-detect.xyz/video3.mp4',
  3: 'http://cloud.epilepsy-detect.xyz/video3.mp4'
})

// 当前视频URL
const videoUrl = ref(videoUrls.value[1])

// 病房列表 - 静态数据
const rooms = ref([
  { id: 1, name: '301室' },
  { id: 2, name: '302室' },
  { id: 3, name: '303室' }
])

// 当前选中的病房
const currentRoom = ref(1)

// 监控状态 - 模拟在线
const monitorStatus = ref('online')

// 病房信息数据 - 为每个病房添加不同的信息
const roomsInfo = {
  1: {
    roomNo: '301室',
    bedCount: 2,
    doctor: '张医生',
    nurse: '李护士'
  },
  2: {
    roomNo: '302室',
    bedCount: 4,
    doctor: '王医生',
    nurse: '赵护士'
  },
  3: {
    roomNo: '303室',
    bedCount: 3,
    doctor: '刘医生',
    nurse: '陈护士'
  }
}

// 病房信息 - 初始化为第一个病房的信息
const wardInfo = ref(roomsInfo[1])

// 病房状态
const roomStatus = ref({
  text: '正常',
  type: 'success'
})

// 生命体征数据 - 模拟实时数据
const vitals = ref({
  heartRate: 75,
  bloodPressure: '120/80',
  temperature: 36.5,
  oxygen: 98
})

// 模拟数据更新
const updateVitals = () => {
  // 随机波动数据
  vitals.value.heartRate = Math.floor(70 + Math.random() * 20)
  vitals.value.temperature = (36 + Math.random()).toFixed(1)
  vitals.value.oxygen = Math.floor(95 + Math.random() * 5)
}

// 行为记录 - 静态数据
const activities = ref([
  {
    content: '患者正常休息中',
    time: '10:00',
    type: 'success',
    color: '#67C23A'
  },
  {
    content: '护士查房',
    time: '09:30',
    type: 'primary',
    color: '#409EFF'
  },
  {
    content: '服用早间药物',
    time: '08:00',
    type: 'info',
    color: '#909399'
  }
])

// 环境监测数据 - 静态数据
const environment = ref([
  {
    label: '室温',
    value: '26',
    unit: '°C',
    icon: 'Sunny',
    status: 'normal'
  },
  {
    label: '湿度',
    value: '45',
    unit: '%',
    icon: 'Monitor',
    status: 'normal'
  },
  {
    label: '光照',
    value: '300',
    unit: 'lux',
    icon: 'Lightning',
    status: 'warning'
  },
  {
    label: '噪音',
    value: '35',
    unit: 'dB',
    icon: 'Notification',
    status: 'normal'
  }
])

// 视频流 - 模拟离线状态
const videoStream = ref(null)
const videoElement = ref(null)

// 处理病房切换 - 修改此函数以更新视频和病房信息
const handleRoomChange = (roomId) => {
  try {
    const room = rooms.value.find(r => r.id === roomId)
    if (room) {
      monitorStatus.value = 'offline'
      
      // 更新视频URL
      videoUrl.value = ''  // 先清空视频URL，显示加载状态
      
      setTimeout(() => {
        monitorStatus.value = 'online'
        // 设置新的视频URL
        videoUrl.value = videoUrls.value[roomId]
        
        // 更新病房信息
        wardInfo.value = roomsInfo[roomId]
      }, 1500)
    }
  } catch (error) {
    console.error('切换病房失败:', error)
    ElMessage.error('切换病房失败')
  }
}

// 切换全屏
const toggleFullscreen = () => {
  try {
    ElMessage({
      message: '全屏功能模拟',
      type: 'info'
    })
  } catch (error) {
    console.error('全屏操作失败:', error)
    ElMessage.error('操作失败')
  }
}

// 开始/停止录制
const toggleRecord = () => {
  try {
    ElMessage({
      message: '录制功能模拟',
      type: 'info'
    })
  } catch (error) {
    console.error('录制操作失败:', error)
    ElMessage.error('操作失败')
  }
}

// 截图
const captureSnapshot = () => {
  try {
    ElMessage({
      message: '截图功能模拟',
      type: 'info'
    })
  } catch (error) {
    console.error('截图操作失败:', error)
    ElMessage.error('操作失败')
  }
}

// 刷新数据
const refreshData = () => {
  try {
    updateVitals()
    ElMessage({
      message: '数据已更新',
      type: 'success'
    })
  } catch (error) {
    console.error('数据更新失败:', error)
    ElMessage.error('更新失败')
  }
}

// 获取生命体征显示类
const getVitalClass = (value, min, max) => {
  if (typeof value === 'string') return 'normal' // 处理血压字符串
  if (value < min) return 'warning'
  if (value > max) return 'danger'
  return 'normal'
}

let timer = null

// 组件挂载时初始化
onMounted(() => {
  try {
    timer = setInterval(() => {
      updateVitals()
    }, 3000)
  } catch (error) {
    console.error('初始化失败:', error)
    ElMessage.error('页面初始化失败')
  }
})

// 组件卸载时清理
onUnmounted(() => {
  try {
    if (timer) {
      clearInterval(timer)
      timer = null
    }
  } catch (error) {
    console.error('清理失败:', error)
  }
})

// 添加新的导入
const patientInfo = ref({
  name: '张三',
  age: 45,
  gender: '男',
  admissionDate: '2024-01-15'
})

// 脑电图相关
const eegChart = ref(null)
const eegInstance = ref(null)
let eegTimer = null

// 初始化脑电图
const initEEGChart = () => {
  if (!eegChart.value) return
  
  eegInstance.value = echarts.init(eegChart.value)
  const option = {
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'time',
      splitLine: {
        show: false
      }
    },
    yAxis: {
      type: 'value',
      splitLine: {
        show: true
      }
    },
    series: [
      {
        name: 'EEG',
        type: 'line',
        showSymbol: false,
        data: [],
        lineStyle: {
          width: 1
        }
      }
    ]
  }
  eegInstance.value.setOption(option)
}

// 更新脑电图数据
const updateEEGData = () => {
  const now = new Date()
  const value = Math.random() * 100
  const data = eegInstance.value.getOption().series[0].data
  data.push([now, value])
  
  if (data.length > 100) {
    data.shift()
  }
  
  eegInstance.value.setOption({
    series: [{
      data: data
    }]
  })
}

// 控制脑电图播放/暂停
const isEEGPlaying = ref(true)
const toggleEEGPlay = () => {
  isEEGPlaying.value = !isEEGPlaying.value
  if (isEEGPlaying.value) {
    startEEGUpdate()
  } else {
    stopEEGUpdate()
  }
}

// 开始更新脑电图
const startEEGUpdate = () => {
  eegTimer = setInterval(updateEEGData, 100)
}

// 停止更新脑电图
const stopEEGUpdate = () => {
  if (eegTimer) {
    clearInterval(eegTimer)
    eegTimer = null
  }
}

// 下载脑电图数据
const downloadEEGData = () => {
  try {
    const dataUrl = eegInstance.value.getDataURL()
    const link = document.createElement('a')
    link.download = `EEG数据_${new Date().toISOString().slice(0, 10)}.png`
    link.href = dataUrl
    link.click()
  } catch (error) {
    ElMessage.error('下载失败')
  }
}

// 修改原有的 onMounted
onMounted(async () => {
  try {
    // ... 原有初始化代码 ...
    
    await nextTick()
    initEEGChart()
    startEEGUpdate()
    
    window.addEventListener('resize', () => {
      eegInstance.value?.resize()
    })
  } catch (error) {
    console.error('初始化失败:', error)
    ElMessage.error('页面初始化失败')
  }
})

// 修改原有的 onUnmounted
onUnmounted(() => {
  // ... 原有清理代码 ...
  stopEEGUpdate()
  eegInstance.value?.dispose()
})
</script>

<style scoped>
.ward-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.control-panel {
  margin-bottom: 20px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.room-selector {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 5px;
}

.status-indicator.online {
  color: #67C23A;
}

.status-indicator.offline {
  color: #F56C6C;
}

.main-content {
  display: grid;
  grid-template-columns: 300px 1fr 300px;
  gap: 20px;
  margin-bottom: 20px;
  height: calc(100vh - 300px); /* 调整总高度 */
}

.video-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 16/9; /* 保持16:9比例 */
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden; /* 防止视频溢出 */
}

video {
  width: 100%;
  height: 100%;
  object-fit: contain; /* 保持视频比例 */
}

.monitor-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* 确保视频控制按钮不会遮挡视频内容 */
.monitor-controls {
  position: absolute;
  bottom: 20px;
  right: 20px;
  z-index: 10;
  background: rgba(0, 0, 0, 0.5);
  padding: 8px;
  border-radius: 4px;
}

.left-panel,
.right-panel,
.center-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.video-card {
  flex: 0 0 400px;
  margin-bottom: 20px;
}

.video-wrapper {
  width: 100%;
  height: 360px;
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.eeg-card {
  flex: 1;
  min-height: 300px;
}

.eeg-chart {
  width: 100%;
  height: 250px;
}

.monitor-container {
  flex: 1;
  min-width: 0; /* 防止溢出 */
}

.monitor-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.video-wrapper {
  flex: 1;
  position: relative;
  width: 100%;
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  border-radius: 4px;
}

video {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.video-placeholder {
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.video-placeholder .el-icon {
  font-size: 32px;
}

/* 删除不需要的样式 */
.monitor-controls {
  display: none;
}

.side-card {
  height: 100%;
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.info-item {
  display: flex;
  justify-content: space-between;
}

.vital-signs {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.vital-item {
  text-align: center;
  padding: 15px;
  border-radius: 8px;
  background: #f5f7fa;
}

.vital-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 5px;
}

.vital-value {
  font-size: 24px;
  font-weight: bold;
}

.vital-value.normal {
  color: #67C23A;
}

.vital-value.warning {
  color: #E6A23C;
}

.vital-value.danger {
  color: #F56C6C;
}

.unit {
  font-size: 12px;
  color: #909399;
}

.bottom-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.env-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.env-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px;
  border-radius: 8px;
  background: #f5f7fa;
}

.env-info {
  flex: 1;
}

.env-label {
  font-size: 14px;
  color: #909399;
}

.env-value {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.el-icon {
  font-size: 24px;
}

.el-icon.normal {
  color: #67C23A;
}

.el-icon.warning {
  color: #E6A23C;
}

.el-icon.danger {
  color: #F56C6C;
}

.eeg-section {
  margin-bottom: 20px;
}

.eeg-chart {
  width: 100%;
  height: 300px;
}

.eeg-controls {
  display: flex;
  gap: 10px;
}
</style>
