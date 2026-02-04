<template>
  <div class="eeg-container">
    <!-- 文件上传区域 -->
    <div class="file-upload">
      <el-upload
        class="upload-demo"
        drag
        :action="uploadUrl"
        :on-success="handleUploadSuccess"
        :on-error="handleUploadError"
        :before-upload="beforeUpload"
        accept=".edf"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          拖拽EDF文件到此处或 <em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            请上传.edf格式文件
          </div>
        </template>
      </el-upload>
    </div>

    <!-- 状态提示 -->
    <div :class="['status', isLoading ? 'loading' : (isLoaded ? 'connected' : 'disconnected')]">
      {{ isLoading ? '加载中...' : (isLoaded ? '数据已加载' : '未加载数据') }}
    </div>

    <!-- 通道选择器 -->
    <div class="channel-selector">
      <button
        v-for="channel in availableChannels"
        :key="channel"
        :class="{ active: selectedChannels.includes(channel) }"
        @click="toggleChannel(channel)"
      >
        {{ channel }}
      </button>
    </div>

    <!-- 控制面板 -->
    <div class="control-panel">
      <el-slider
        v-model="timeRange"
        range
        :min="0"
        :max="maxTime"
        :step="1"
        @change="updateTimeRange"
      />
      <div class="time-labels">
        <span>{{ formatTime(timeRange[0]) }}</span>
        <span>{{ formatTime(timeRange[1]) }}</span>
      </div>
    </div>

    <!-- 图表容器 -->
    <div class="chart-container">
      <VChart
        class="chart"
        :option="chartOption"
        autoresize
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { use } from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, TitleComponent, ToolboxComponent, DataZoomComponent } from 'echarts/components'
import VChart from 'vue-echarts'
import { CanvasRenderer } from 'echarts/renderers'
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'
import axios from 'axios'

// 初始化ECharts模块
use([LineChart, GridComponent, TooltipComponent, TitleComponent, ToolboxComponent, DataZoomComponent, CanvasRenderer])

// 上传URL
const uploadUrl = '/api/eeg/upload-edf'

// 响应式数据
const isLoaded = ref(false)
const isLoading = ref(false)
const edfId = ref('')
const maxTime = ref(10) // 默认10秒
const timeRange = ref([0, 10])

// 可用通道列表
const availableChannels = ref([
  'FP1-F7', 'F7-T7', 'T7-P7', 'P7-O1',
  'FP1-F3', 'F3-C3', 'C3-P3', 'P3-O1',
  'FP2-F4', 'F4-C4', 'C4-P4', 'P4-O2',
  'FP2-F8', 'F8-T8', 'T8-P8', 'P8-O2',
  'FZ-CZ', 'CZ-PZ', 'P7-T7', 'T7-FT9',
  'FT9-FT10', 'FT10-T8', 'T8-P8'
])

// 默认选择所有通道
const selectedChannels = ref([...availableChannels.value])

// 图表配置
const chartOption = reactive({
  title: {
    text: 'EEG 数据',
    left: 'center',
    top: 10
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross',
      animation: false
    }
  },
  toolbox: {
    feature: {
      dataZoom: {
        yAxisIndex: 'none'
      },
      restore: {},
      saveAsImage: {}
    }
  },
  grid: {
    left: 100,
    right: 50,
    top: 50,
    bottom: 50
  },
  xAxis: {
    type: 'value',
    name: '时间 (s)',
    min: 0,
    max: 10,
    axisLabel: {
      formatter: (value) => value.toFixed(1)
    }
  },
  yAxis: {
    type: 'category',
    data: [],
    axisLine: { onZero: false },
    axisTick: { show: false },
    splitLine: { show: false },
    axisLabel: {
      inside: true,
      fontSize: 10
    },
    inverse: true
  },
  dataZoom: [
    {
      type: 'inside',
      xAxisIndex: 0,
      start: 0,
      end: 100
    },
    {
      type: 'slider',
      xAxisIndex: 0,
      start: 0,
      end: 100
    }
  ],
  series: []
})

// 格式化时间
function formatTime(seconds) {
  const min = Math.floor(seconds / 60)
  const sec = Math.floor(seconds % 60)
  return `${min}:${sec.toString().padStart(2, '0')}`
}

// 切换通道显示
function toggleChannel(channel) {
  const index = selectedChannels.value.indexOf(channel)
  if (index > -1) {
    selectedChannels.value.splice(index, 1)
  } else {
    selectedChannels.value.push(channel)
  }
  updateChart()
}

// 更新时间范围
function updateTimeRange() {
  fetchEdfData()
}

// 文件上传前检查
function beforeUpload(file) {
  const isEDF = file.name.toLowerCase().endsWith('.edf')
  if (!isEDF) {
    ElMessage.error('请上传EDF格式文件!')
    return false
  }
  
  const isLt100M = file.size / 1024 / 1024 < 100
  if (!isLt100M) {
    ElMessage.error('文件大小不能超过100MB!')
    return false
  }
  
  isLoading.value = true
  return true
}

// 处理上传成功
function handleUploadSuccess(response) {
  isLoading.value = false
  if (response.code === 0) {
    ElMessage.success('文件上传成功')
    edfId.value = response.data.id
    maxTime.value = response.data.duration || 10
    timeRange.value = [0, Math.min(10, maxTime.value)]
    availableChannels.value = response.data.channels || availableChannels.value
    selectedChannels.value = [...availableChannels.value]
    isLoaded.value = true
    fetchEdfData()
  } else {
    ElMessage.error(response.message || '上传失败')
  }
}

// 处理上传错误
function handleUploadError() {
  isLoading.value = false
  ElMessage.error('文件上传失败')
}

// 获取EDF数据
async function fetchEdfData() {
  if (!edfId.value) return
  
  isLoading.value = true
  try {
    const response = await axios.get('/api/eeg/edf-data', {
      params: {
        id: edfId.value,
        startTime: timeRange.value[0],
        endTime: timeRange.value[1],
        channels: selectedChannels.value.join(',')
      }
    })
    
    if (response.data.code === 0) {
      updateChartWithData(response.data.data)
      isLoaded.value = true
    } else {
      ElMessage.error(response.data.message || '获取数据失败')
    }
  } catch (error) {
    console.error('获取EDF数据失败:', error)
    ElMessage.error('获取数据失败: ' + error.message)
  } finally {
    isLoading.value = false
  }
}

// 更新图表数据
function updateChartWithData(data) {
  // 更新Y轴通道标签
  chartOption.yAxis.data = selectedChannels.value
  
  // 更新X轴范围
  chartOption.xAxis.min = timeRange.value[0]
  chartOption.xAxis.max = timeRange.value[1]
  
  // 更新系列数据
  chartOption.series = selectedChannels.value.map((channel, index) => {
    const channelData = data[channel] || []
    // 计算垂直偏移，使通道显示不重叠
    const offset = (selectedChannels.value.length - index - 1) * 2
    
    return {
      name: channel,
      type: 'line',
      showSymbol: false,
      data: channelData.map(point => [point[0], point[1] + offset]),
      smooth: true,
      lineStyle: {
        width: 1
      },
      emphasis: {
        lineStyle: {
          width: 2
        }
      }
    }
  })
}

// 更新图表
function updateChart() {
  if (isLoaded.value) {
    fetchEdfData()
  }
}

// 生命周期钩子
onMounted(() => {
  // 初始化
})

// 监听选中通道变化
watch(selectedChannels, () => {
  updateChart()
})
</script>

<style scoped>
.eeg-container {
  width: 100%;
  height: 800px;
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.file-upload {
  margin-bottom: 20px;
}

.chart-container {
  flex: 1;
  min-height: 600px;
}

.chart {
  width: 100%;
  height: 100%;
}

.status {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 5px 10px;
  border-radius: 4px;
  z-index: 100;
}

.connected {
  background: #67c23a;
  color: white;
}

.disconnected {
  background: #f56c6c;
  color: white;
}

.loading {
  background: #e6a23c;
  color: white;
}

.channel-selector {
  margin-bottom: 10px;
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}

.channel-selector button {
  padding: 5px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  background: white;
}

.channel-selector button.active {
  background: #409eff;
  color: white;
  border-color: #409eff;
}

.control-panel {
  margin: 10px 0 20px;
  padding: 10px;
  background: #f5f7fa;
  border-radius: 4px;
}

.time-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 5px;
  color: #606266;
}
</style>