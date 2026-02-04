<template>
  <div class="eeg-data-container" v-if="value">
    
    <!-- 主要内容区域 -->
    <div class="flex-row">
      <!-- 左侧：实时数据流控制 -->
      <el-card class="control-card">
        <template #header>
          <div class="panel-header">
            <span>EEG数据控制</span>
            <div class="connection-status" :class="{ connected: isConnected }">
              {{ isConnected ? '已连接' : '未连接' }}
            </div>
          </div>
        </template>
        
        <div class="controls">
          <el-form :model="streamSettings" label-width="120px">
            <el-form-item label="窗口大小 (秒)">
              <el-slider v-model="streamSettings.windowSize" :min="0.5" :max="5" :step="0.1" />
            </el-form-item>
            <el-form-item label="步长 (秒)">
              <el-slider v-model="streamSettings.stepSize" :min="0.1" :max="2" :step="0.1" />
            </el-form-item>
          </el-form>
          <div class="stream-buttons">
            <el-button type="primary" @click="startStreaming" :disabled="isStreaming || !isConnected">
              <el-icon><VideoPlay /></el-icon> 开始
            </el-button>
            <el-button type="danger" @click="stopStreaming">
              <el-icon><VideoPause /></el-icon> 暂停
            </el-button>
            <el-button type="primary" @click="toggleConnection">
              {{ isConnected ? '断开连接' : '连接WebSocket' }}
            </el-button>
          </div>
        </div>
        
        <div class="status-panel" v-if="isConnected">
          <div class="status-item">当前时间: <span>{{ currentTimestamp.toFixed(2) }} 秒</span></div>
          <div class="status-item">接收数据包: <span>{{ packetCount }}</span></div>
          <div class="status-item">发作状态: <span :class="isSeizure ? 'error' : 'success'">{{ isSeizure ? '是' : '否' }}</span></div>
          <div class="seizure-alert" v-show="isSeizure">
            <strong>警告:</strong> 检测到发作活动！
          </div>
        </div>
      </el-card>
      
      <!-- 右侧：数据可视化 -->
      <el-card class="chart-card">
        <template #header>
          <div class="panel-header">
            <span>EEG数据可视化</span>
            <div class="seizure-indicator" v-if="isSeizure">
              <el-tag type="danger">发作状态</el-tag>
            </div>
          </div>
        </template>
        
        <div class="visualization-controls">
          <el-form :inline="true" :model="visualSettings">
            <el-form-item label="显示点数">
              <el-input-number v-model="visualSettings.displayPoints" :min="256" :max="5120" :step="128" />
            </el-form-item>
            <el-form-item label="Y轴缩放">
              <el-input-number v-model="visualSettings.yScale" :min="0.1" :max="10" :step="0.1" />
            </el-form-item>
            <el-form-item label="通道间距">
              <el-input-number v-model="visualSettings.channelOffset" :min="50" :max="500" :step="10" />
            </el-form-item>
          </el-form>
          <div class="chart-buttons">
            <el-button @click="clearChart">清除图表</el-button>
            <el-button @click="selectAllChannels">{{ allChannelsSelected ? '取消全选' : '全选' }}</el-button>
          </div>
        </div>
        
        <div class="channel-selector">
          <el-checkbox-group v-model="selectedChannels">
            <div v-for="(channel, index) in availableChannels" :key="channel" class="channel-checkbox">
              <div class="color-box" :style="{ backgroundColor: getChannelColor(index) }"></div>
              <el-checkbox :label="channel">{{ channel }}</el-checkbox>
            </div>
          </el-checkbox-group>
        </div>
        
        <div class="chart-container" ref="chartContainer">
          <div id="main-chart" class="main-chart"></div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { VideoPlay, VideoPause } from '@element-plus/icons-vue'
import axios from 'axios'
import * as echarts from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, ToolboxComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { io } from 'socket.io-client'

// 注册必要的 echarts 组件
echarts.use([LineChart, GridComponent, TooltipComponent, ToolboxComponent, LegendComponent, CanvasRenderer])

// 服务器配置
const SERVER_URL = 'http://localhost:5000'
const SOCKET_URL = 'http://localhost:5000'

// 状态变量
const isConnected = ref(false)
const isStreaming = ref(false)
const isSeizure = ref(false)
const socket = ref(null)
const mainChart = ref(null)
const currentTimestamp = ref(0)
const packetCount = ref(0)

// 通道相关
const availableChannels = ref([])
const selectedChannels = ref([])
const allChannelsSelected = computed(() => {
  return selectedChannels.value.length === availableChannels.value.length
})

// 数据预览
const dataPreview = ref('')
const streamPreview = ref('')
const value = ref(true)
// 数据获取设置
const dataFetchSettings = reactive({
  startTime: 0,
  windowSize: 1.0
})

// 数据流设置
const streamSettings = reactive({
  windowSize: 5.0,
  stepSize: 1.5
})

// 可视化设置
const visualSettings = reactive({
  displayPoints: 1024,
  yScale: 2,
  channelOffset: 200
})

// 数据缓存
const channelBuffers = reactive({})

// 通道颜色
const colorPalette = [
  'rgb(255, 99, 132)', 'rgb(54, 162, 235)', 'rgb(255, 206, 86)', 
  'rgb(75, 192, 192)', 'rgb(153, 102, 255)', 'rgb(255, 159, 64)',
  'rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)',
  'rgb(128, 0, 128)', 'rgb(0, 128, 128)', 'rgb(128, 128, 0)',
  'rgb(128, 0, 0)', 'rgb(0, 128, 0)', 'rgb(0, 0, 128)',
  'rgb(255, 0, 255)', 'rgb(0, 255, 255)', 'rgb(255, 255, 0)'
]

// 获取通道颜色
const getChannelColor = (index) => {
  return colorPalette[index % colorPalette.length]
}

// 切换WebSocket连接
const toggleConnection = () => {
  if (isConnected.value) {
    disconnectSocket()
  } else {
    connectSocket()
  }
}

// 连接 WebSocket
const connectSocket = () => {
  socket.value = io(SOCKET_URL)
  
  socket.value.on('connect', () => {
    isConnected.value = true
    ElMessage.success('已连接到 EEG 数据服务器')
  })
  
  socket.value.on('disconnect', () => {
    isConnected.value = false
    isStreaming.value = false
    ElMessage.warning('与 EEG 数据服务器的连接已断开')
  })
  
  socket.value.on('connection_response', (data) => {
    console.log('连接响应:', data)
  })
  
  socket.value.on('eeg_data', (data) => {
    processEegData(data)
  })
  
  socket.value.on('eeg_stream_end', () => {
    isStreaming.value = false
    ElMessage.info('EEG 数据流已结束')
  })
}

// 断开 WebSocket 连接
const disconnectSocket = () => {
  if (socket.value) {
    socket.value.disconnect()
    socket.value = null
    isConnected.value = false
  }
}

// 获取EEG信息
const getEegInfo = async () => {
  try {
    const response = await axios.get(`${SERVER_URL}/eeg/info`)
    if (response.data) {
      ElMessage.success('成功获取EEG信息')
      dataPreview.value = JSON.stringify(response.data, null, 2)
      
      // 如果有通道信息，更新可用通道列表
      if (response.data.channels) {
        availableChannels.value = response.data.channels
      }
    }
  } catch (error) {
    console.error('获取EEG信息错误:', error)
    ElMessage.error('获取EEG信息失败: ' + error.message)
  }
}

// 获取特定时间段的数据
const fetchData = async () => {
  try {
    const response = await axios.get(`${SERVER_URL}/eeg/data`, {
      params: {
        start_time: dataFetchSettings.startTime,
        window_size: dataFetchSettings.windowSize
      }
    })
    
    if (response.data) {
      ElMessage.success('成功获取数据')
      dataPreview.value = JSON.stringify(response.data, null, 2)
      
      // 如果有通道信息，更新可用通道列表
      if (response.data.channels && !availableChannels.value.length) {
        availableChannels.value = response.data.channels
      }
      
      // 更新图表
      if (response.data.data) {
        updateChart(response.data.data)
      }
    }
  } catch (error) {
    console.error('获取数据错误:', error)
    ElMessage.error('获取数据失败: ' + error.message)
  }
}

// 开始数据流
const startStreaming = async () => {
  try {
    const response = await axios.post(`${SERVER_URL}/eeg/stream/start`, {
      window_size: streamSettings.windowSize,
      step_size: streamSettings.stepSize
    })
    
    if (response.data.status === 'success') {
      isStreaming.value = true
      ElMessage.success('EEG 数据流已启动')
      
      // 初始化数据缓冲区
      clearChart()
    } else {
      console.log(error)
      ElMessage.error(response.data.message || '启动数据流失败')
    }
  } catch (error) {
    console.error('启动数据流错误:', error)
    ElMessage.error('启动数据流失败: ' + error.message)
  }
}

// 停止数据流
const stopStreaming = async () => {
  try {
    const response = await axios.post(`${SERVER_URL}/eeg/stream/stop`)
    
    if (response.data.status === 'success') {
      isStreaming.value = false
      ElMessage.success('EEG 数据流已停止')
    } else {
      ElMessage.error(response.data.message || '停止数据流失败')
    }
  } catch (error) {
    console.error('停止数据流错误:', error)
    ElMessage.error('停止数据流失败: ' + error.message)
  }
}

// 处理 EEG 数据
const processEegData = (data) => {
  // 更新状态信息
  packetCount.value++
  currentTimestamp.value = data.timestamp || 0
  isSeizure.value = data.is_seizure || false
  
  // 更新实时数据预览
  const previewData = {
    timestamp: data.timestamp,
    is_seizure: data.is_seizure,
    channels: data.channels ? data.channels.length : 0,
    selected_channels: selectedChannels.value.length
  }
  streamPreview.value = JSON.stringify(previewData, null, 2)
  
  // 如果是第一次收到数据，更新可用通道列表
  if (availableChannels.value.length === 0 && data.channels) {
    availableChannels.value = data.channels
    selectedChannels.value = data.channels.slice(0, 23) // 默认选择前5个通道
  }
  
  // 更新图表数据
  if (data.data) {
    updateChart(data.data)
  }
}

// 初始化主图表
const initMainChart = () => {
  const chartDom = document.getElementById('main-chart')
  if (!chartDom) return
  
  mainChart.value = echarts.init(chartDom)
  
  const option = {
    grid: {
      left: 50,
      right: 20,
      top: 30,
      bottom: 30
    },
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const firstParam = params[0]
        return `时间: ${firstParam.value[0].toFixed(2)}s<br/>` + 
               params.map(param => `${param.seriesName}: ${param.value[1].toFixed(2)}`).join('<br/>')
      }
    },
    xAxis: {
      type: 'value',
      name: '时间 (秒)',
      axisLabel: {
        formatter: (value) => (value / 256).toFixed(1)
      }
    },
    yAxis: {
      type: 'value',
      name: '振幅',
      axisLabel: {
        show: false
      },
      splitLine: {
        show: true,
        lineStyle: {
          color: 'rgba(0, 0, 0, 0.1)',
          type: 'dashed'
        }
      }
    },
    series: [],
    animation: false,
    legend: {
      type: 'scroll',
      orient: 'vertical',
      right: 10,
      top: 20,
      bottom: 20,
      textStyle: {
        fontSize: 12
      }
    }
  }
  
  mainChart.value.setOption(option)
  
  // 响应窗口大小变化
  window.addEventListener('resize', () => {
    mainChart.value && mainChart.value.resize()
  })
}

// 更新图表
const updateChart = (newData) => {
  if (!mainChart.value) return
  
  // 更新每个选中通道的数据
  selectedChannels.value.forEach((channel, index) => {
    if (!channelBuffers[channel]) {
      channelBuffers[channel] = []
    }
    
    // 添加新数据到缓冲区
    if (newData[channel]) {
      const channelData = newData[channel]
      
      // 为每个数据点添加索引作为X轴值
      const newPoints = Array.isArray(channelData) 
        ? channelData.map((val, i) => [i, val])
        : (channelData.data ? channelData.data.map((val, i) => [i, val]) : [])
      
      // 更新缓冲区
      channelBuffers[channel] = [...channelBuffers[channel], ...newPoints]
      
      // 限制缓冲区大小
      if (channelBuffers[channel].length > visualSettings.displayPoints) {
        channelBuffers[channel] = channelBuffers[channel].slice(-visualSettings.displayPoints)
      }
    }
  })
  
  // 准备图表数据
  const series = selectedChannels.value.map((channel, index) => {
    // 计算通道偏移量
    const offset = index * visualSettings.channelOffset
    
    return {
      name: channel,
      type: 'line',
      showSymbol: false,
      data: channelBuffers[channel] ? channelBuffers[channel].map(point => [
        point[0], 
        point[1] * visualSettings.yScale + offset
      ]) : [],
      lineStyle: {
        width: 1,
        color: getChannelColor(index)
      },
      emphasis: {
        lineStyle: {
          width: 2
        }
      }
    }
  })
  
  // 计算Y轴范围
  const totalChannels = selectedChannels.value.length
  const maxOffset = (totalChannels - 1) * visualSettings.channelOffset
  
  // 更新图表配置
  mainChart.value.setOption({
    yAxis: {
      min: -100,
      max: maxOffset + 100,
      axisLabel: {
        formatter: (value) => {
          const channelIndex = Math.floor(value / visualSettings.channelOffset)
          if (value % visualSettings.channelOffset === 0 && channelIndex < selectedChannels.value.length) {
            return selectedChannels.value[channelIndex]
          }
          return ''
        }
      }
    },
    series: series
  })
}

// 清除图表数据
const clearChart = () => {
  Object.keys(channelBuffers).forEach(key => {
    channelBuffers[key] = []
  })
  
  if (mainChart.value) {
    mainChart.value.setOption({
      series: selectedChannels.value.map(channel => ({
        name: channel,
        data: []
      }))
    })
  }
}

// 全选/取消全选通道
const selectAllChannels = () => {
  if (allChannelsSelected.value) {
    selectedChannels.value = []
  } else {
    selectedChannels.value = [...availableChannels.value]
  }
}

// 监听选中通道变化
watch(selectedChannels, () => {
  nextTick(() => {
    updateChart({}) // 传入空对象，只更新图表配置
  })
})

// 监听可视化设置变化
watch([() => visualSettings.yScale, () => visualSettings.channelOffset], () => {
  nextTick(() => {
    updateChart({}) // 传入空对象，只更新图表配置
  })
})

// 生命周期钩子
onMounted(() => {
  initMainChart()
  connectSocket()
})

onBeforeUnmount(() => {
  // 停止数据流
  if (isStreaming.value) {
    stopStreaming()
  }
  
  // 断开连接
  disconnectSocket()
  
  // 销毁图表实例
  if (mainChart.value) {
    mainChart.value.dispose()
  }
})
</script>

<style scoped>
.eeg-data-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.flex-row {
  display: flex;
  gap: 20px;
}

.control-card {
  width: 30%;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.chart-card {
  width: 70%;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

h1 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.section-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.connection-status {
  padding: 4px 8px;
  border-radius: 4px;
  background-color: #f56c6c;
  color: white;
}

.connection-status.connected {
  background-color: #67c23a;
}

.status-panel {
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.status-item {
  margin-bottom: 8px;
}

.success {
  color: #67c23a;
  font-weight: bold;
}

.error {
  color: #f56c6c;
  font-weight: bold;
}

.warning {
  color: #e6a23c;
  font-weight: bold;
}

.seizure-alert {
  background-color: #f56c6c;
  color: white;
  padding: 10px;
  border-radius: 4px;
  margin-top: 10px;
  animation: blink 1s infinite;
}

.control-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.flex-row {
  display: flex;
  gap: 20px;
}

.flex-column {
  flex: 1;
}

.controls {
  margin-bottom: 20px;
}

.stream-buttons {
  display: flex;
  gap: 10px;
}

.data-display {
  height: 200px;
  overflow-y: auto;
  border: 1px solid #ddd;
  padding: 10px;
  background-color: #fff;
  border-radius: 4px;
  font-family: monospace;
  white-space: pre-wrap;
}

.visualization-controls {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.chart-buttons {
  display: flex;
  gap: 10px;
}

.channel-selector {
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.channel-checkbox {
  display: inline-flex;
  align-items: center;
  margin-right: 15px;
  margin-bottom: 10px;
}

.color-box {
  display: inline-block;
  width: 12px;
  height: 12px;
  margin-right: 5px;
  border: 1px solid #ccc;
}

.main-chart {
  height: 600px;
  width: 100%;
}

.seizure-indicator {
  animation: blink 1s infinite;
}

@keyframes blink {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}
</style>