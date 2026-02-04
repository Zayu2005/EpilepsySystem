<template>
  <div class="eeg-container">
    <!-- 顶部操作区 -->
    <el-card class="upload-section">
      <template #header>
        <div class="section-header">
          <div class="header-left">
            <span>EEG数据分析</span>
            <el-select v-model="selectPatientId" clearable placeholder="选择病人" style="margin-left: 20px; width: 240px;">
              <el-option v-for="item in patients" :key="item.name" :label="item.name" :value="item.id" />
            </el-select>
          </div>
          <el-button type="primary" @click="startAnalysis" :loading="analyzing">
            <el-icon>
              <Connection />
            </el-icon>
            开始分析
          </el-button>
        </div>
      </template>

      <el-upload class="eeg-upload" drag :action="uploadUrl" :before-upload="beforeUpload" :auto-upload="true"
        :on-success="handleUploadSuccess" :on-error="handleUploadError" accept=".edf,.eeg" :data="{
              patientId: selectPatientId,
              userId: userInfo.id
            }">
        <el-icon class="el-icon--upload">
          <Upload />
        </el-icon>
        <div class="el-upload__text">
          拖拽EEG文件到此处或 <em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支持.edf/.eeg格式文件，单个文件不超过500MB
          </div>
        </template>
      </el-upload>
    </el-card>

    <!-- 分析结果展示区 -->
    <div class="analysis-section">
      <el-row :gutter="20">
        <!-- 左侧：分析历史 (原来是EEG波形图的位置) -->
        <el-col :span="16">
          <el-card class="history-section">
            <template #header>
              <div class="section-header">
                <span>分析历史</span>
                <el-input v-model="searchQuery" placeholder="搜索患者姓名" prefix-icon="Search" style="width: 200px" />
              </div>
            </template>
            <el-table :data="historyRecords" style="width: 100%">
              <el-table-column prop="createTime" label="检测日期" width="180" />
              <el-table-column prop="patientName" label="患者姓名" width="120" />
              <el-table-column prop="patientId" label="患者ID" width="120" />
              <el-table-column prop="riskLevel" label="风险等级" width="120">
                <template #default="scope">
                  <el-tag :type="getRiskType(scope.row.riskLevel)">
                    {{ getRiskLabel(scope.row.riskLevel) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="doctorName" label="分析医生" width="120" />
              <el-table-column label="操作">
                <template #default="scope">
                  <el-button link type="primary" @click="viewRecord(scope.row)">
                    查看
                  </el-button>
                  <el-button link type="primary" @click="exportRecord(scope.row)">
                    导出
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <div class="pagination">
              <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize"
                :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next" :total="total"
                @size-change="handleSizeChange" @current-change="handleCurrentChange" />
            </div>
          </el-card>
        </el-col>

        <!-- 右侧：分析结果 -->
        <el-col :span="8">
          <el-card class="result-card">
            <template #header>
              <div class="section-header">
                <span>分析结果</span>
              </div>
            </template>
            <div v-if="analyzing" class="analysis-loading">
              <el-icon class="loading-icon">
                <Loading />
              </el-icon>
              <p class="loading-text">正在分析...</p>
              <p class="loading-text">(因文件涉及上传下载，请耐心等待)</p>
            </div>
            <div class="analysis-results" v-else-if="analysisResults">
              <div class="result-item">
                <div class="result-label">癫痫发作风险评估</div>
                <el-progress :percentage="analysisResults.riskLevel" :color="getRiskColor" />
                </div>
              <div class="result-item">
                <div class="result-label">异常波形检测</div>
                <el-tag v-for="(anomaly, index) in analysisResults.anomalies" :key="index" :type="anomaly.severity"
                  class="anomaly-tag">
                  {{ anomaly.type }}
                </el-tag>
              </div>
              <div class="result-item">
                <div class="result-label">关键指标</div>
                <el-descriptions :column="1" border>
                  <el-descriptions-item label="脑电节律">
                    {{ analysisResults.rhythm }}
                  </el-descriptions-item>
                  <el-descriptions-item label="异常放电次数">
                    {{ analysisResults.dischargeCount }}
                  </el-descriptions-item>
                  <el-descriptions-item label="主要频段">
                    {{ analysisResults.frequency }}
                  </el-descriptions-item>
                </el-descriptions>
              </div>
              <!-- 添加文件信息部分 -->
              <div class="result-item" v-if="analysisResults.file_name">
                <div class="result-label">文件信息</div>
                <el-descriptions :column="1" border>
                  <el-descriptions-item label="文件名">
                    {{ analysisResults.file_name }}
                  </el-descriptions-item>
                  <el-descriptions-item label="文件大小">
                    {{ (analysisResults.file_size / 1024 / 1024).toFixed(2) }} MB
                  </el-descriptions-item>
                  <el-descriptions-item label="发作时间段"
                    v-if="analysisResults?.start_time !== 0 && analysisResults?.end_time !== 0">
                    {{ analysisResults.start_time }}s - {{ analysisResults.end_time }}s
                  </el-descriptions-item>
                </el-descriptions>
              </div>
            </div>
            <el-empty v-else description="请进行检测后查看报告" />
          </el-card>
        </el-col>
      </el-row>
    </div>


  </div>


  <!-- 添加查看记录的弹窗 -->
  <el-dialog v-model="dialogVisible" title="EEG分析详情" width="80%" :destroy-on-close="true">
    <div v-if="currentRecord" class="record-detail">
      <el-descriptions title="患者信息" :column="2" border>
        <el-descriptions-item label="患者姓名">{{ currentRecord.patientName }}</el-descriptions-item>
        <el-descriptions-item label="患者ID">{{ currentRecord.patientId }}</el-descriptions-item>
        <el-descriptions-item label="检测日期">{{ currentRecord.createTime }}</el-descriptions-item>
        <el-descriptions-item label="分析医生">{{ currentRecord.doctorName }}</el-descriptions-item>
      </el-descriptions>

      <div class="detail-section">
        <h3>风险评估</h3>
        <el-progress :percentage="currentRecord.riskLevel" :text-inside="true" :stroke-width="26":color="getRiskColor(currentRecord.riskLevel)" />
        
      </div>

      <div class="detail-section">
        <h3>异常波形检测</h3>
        <div class="anomaly-tags">
          <el-tag v-for="(anomaly, index) in currentRecord.anomalies" :key="index" :type="anomaly.severity"
            class="anomaly-tag">
            {{ anomaly.type }}
          </el-tag>
          <el-empty v-if="!currentRecord.anomalies || currentRecord.anomalies.length === 0" description="未检测到异常波形" />
        </div>
      </div>

      <el-descriptions title="关键指标" :column="2" border>
        <el-descriptions-item label="脑电节律">{{ currentRecord.rhythm || '未知' }}</el-descriptions-item>
        <el-descriptions-item label="异常放电次数">{{ currentRecord.dischargeCount || 0 }}</el-descriptions-item>
        <el-descriptions-item label="主要频段">{{ currentRecord.frequency || '未知' }}</el-descriptions-item>
      </el-descriptions>

      <el-descriptions v-if="currentRecord.fileName" title="文件信息" :column="2" border>
        <el-descriptions-item label="文件名">{{ currentRecord.fileName }}</el-descriptions-item>
        <el-descriptions-item label="文件大小">{{ currentRecord.fileSize ? (currentRecord.fileSize / 1024 / 1024).toFixed(2)
              +
              ' MB' : '未知' }}</el-descriptions-item>
        <el-descriptions-item v-if="currentRecord.startTime !== undefined && currentRecord.endTime !== undefined"
          label="发作时间段">
          {{ currentRecord.startTime }}s - {{ currentRecord.endTime }}s
        </el-descriptions-item>
      </el-descriptions>
    </div>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="exportRecord(currentRecord)">
          导出报告
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Upload,
  Connection,
  Document,
  ZoomIn,
  ZoomOut,
  Search,
  Loading
} from '@element-plus/icons-vue'
//获取用户信息
import { userInfoService } from '@/api/user';
// 获取所有的病人
import { patientListAllService } from '@/api/patient'
// 进行EEG分析的接口导入
import { getEegAnalysisService, getEegAnalysisListService } from '@/api/eeg'
// 导入html2pdf
import html2pdf from 'html2pdf.js'

import EegData from './EegData.vue'

// 上传相关
const uploadUrl = '/api/eeg/upload' // 实际开发时替换为真实的上传地址
const analyzing = ref(false)

// 查看记录弹窗相关
const dialogVisible = ref(false)
const currentRecord = ref(null)
const selectedChannel = ref('')

// 获取用户信息
const userInfo = ref({
  id: '',
  username: '',
  name: '',
  email: '',
  createTime: '',
  updateTime: '',
})
// 获取用户信息
const getUserInfo = async () => {
  try {
    const res = await userInfoService()
    userInfo.value = res.data
    console.log(userInfo.value.id)
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

const selectPatientId = ref('')
//获取病人信息
const getPatients = async () => {
  try {
    const res = await patientListAllService()
    patients.value = res.data  // 使用 .value 因为 patients 是一个 ref
  } catch (error) {
    console.error('获取患者失败:', error)
  }
}
// 病人数据
const patients = ref([

])

// 分析结果
const analysisResults = ref(null)

// 历史记录
const searchQuery = ref('')  //患者姓名
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
//历史分析记录
const historyRecords = ref([
])

// 文件上传处理
const beforeUpload = (file) => {
  // 检查文件扩展名而不是 MIME 类型
  const isValidFormat = file.name.toLowerCase().endsWith('.edf') || file.name.toLowerCase().endsWith('.eeg')
  const isLt500M = file.size / 1024 / 1024 < 500

  if (!isValidFormat) {
    ElMessage.error('请上传EDF或EEG格式的文件!')
    return false
  }
  if (!isLt500M) {
    ElMessage.error('文件大小不能超过 500MB!')
    return false
  }

  if (selectPatientId.value === '') {
    ElMessage.warning('请先选择病人')
    return false
  }

  return true
}

const handleUploadSuccess = (response) => {
  ElMessage.success('文件上传成功')
  // 处理上传成功后的逻辑
}

const handleUploadError = () => {
  ElMessage.error('文件上传失败')
}

// 开始分析
const startAnalysis = async () => {
  if (selectPatientId.value === '') {
    ElMessage.warning('请选择病人')
    return
  }
  analyzing.value = true
  analysisResults.value = null // 清空之前的分析结果

  try {
    let params = {
      patientId: selectPatientId.value,
      userId: userInfo.value.id
    }
    let res = await getEegAnalysisService(params)
    analysisResults.value = res.data.data
    ElMessage.success('分析完成')
    getHistoryRecords()
  } catch (error) {
    ElMessage.error('分析失败：' + error.message)
  } finally {
    analyzing.value = false
  }
}

// 风险等级颜色
const getRiskColor = (percentage) => {
  if (percentage > 70) return '#F56C6C'
  if (percentage > 30) return '#E6A23C'
  return '#67C23A'
}

// 补充缺失的方法定义
const getRiskType = (level) => {
  // 处理数值类型的风险等级
  if (typeof level === 'number') {
    if (level > 70) return 'danger'
    if (level > 30) return 'warning'
    return 'success'
  }
  // 处理字符串类型的风险等级
  if (level === 'high') return 'danger'
  if (level === 'medium') return 'warning'
  return 'success'
}

const getRiskLabel = (level) => {
  // 处理数值类型的风险等级
  if (typeof level === 'number') {
    if (level > 70) return '高风险'
    if (level > 30) return '中等风险'
    return '低风险'
  }
  // 处理字符串类型的风险等级
  const labels = {
    high: '高风险',
    medium: '中等风险',
    low: '低风险'
  }
  return labels[level] || '未知'
}

// 补充缺失的缩放方法
const zoomIn = () => {
  // TODO: 实现波形图放大功能
  ElMessage.info('放大功能开发中...')
}

const zoomOut = () => {
  // TODO: 实现波形图缩小功能
  ElMessage.info('缩小功能开发中...')
}

// 优化导出报告功能
const exportReport = () => {
  if (!analysisResults.value) {
    ElMessage.warning('暂无可导出的分析结果')
    return
  }

  const currentDate = new Date().toLocaleDateString('zh-CN')
  const reportData = {
    date: currentDate,
    patientInfo: '患者信息', // TODO: 添加实际的患者信息
    results: analysisResults.value,
    doctor: '主治医生' // TODO: 添加实际的医生信息
  }

  // TODO: 实现实际的导出逻辑
  console.log('导出报告数据:', reportData)
  ElMessage.success('报告导出中...')
}

// 优化历史记录导出功能 - 改为导出PDF
const exportRecord = (record) => {
  if (!record) {
    ElMessage.warning('记录数据不完整')
    return
  }

  try {
    // 创建一个临时的div元素作为PDF内容容器
    const element = document.createElement('div')
    element.className = 'pdf-container'

    // 设置PDF内容的样式
    element.style.padding = '20px'
    element.style.fontFamily = 'Arial, sans-serif'

    // 构建PDF内容
    element.innerHTML = `
      <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #409EFF;">${record.patientName}的EEG分析报告</h1>
        <p>检测日期: ${record.createTime}</p>
      </div>
      
      <div style="margin-bottom: 20px;">
        <h2>患者信息</h2>
        <table style="width: 100%; border-collapse: collapse;">
          <tr>
            <td style="border: 1px solid #ddd; padding: 8px; width: 30%;">患者姓名</td>
            <td style="border: 1px solid #ddd; padding: 8px;">${record.patientName}</td>
          </tr>
          <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">患者ID</td>
            <td style="border: 1px solid #ddd; padding: 8px;">${record.patientId}</td>
          </tr>
        </table>
      </div>
      
      <div style="margin-bottom: 20px;">
        <h2>分析结果</h2>
        <table style="width: 100%; border-collapse: collapse;">
          <tr>
            <td style="border: 1px solid #ddd; padding: 8px; width: 30%;">风险等级</td>
            <td style="border: 1px solid #ddd; padding: 8px;">${getRiskLabel(record.riskLevel)} (${record.riskLevel}%)</td>
          </tr>
          <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">脑电节律</td>
            <td style="border: 1px solid #ddd; padding: 8px;">${record.rhythm || '未知'}</td>
          </tr>
          <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">异常放电次数</td>
            <td style="border: 1px solid #ddd; padding: 8px;">${record.dischargeCount || 0}</td>
          </tr>
          <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">主要频段</td>
            <td style="border: 1px solid #ddd; padding: 8px;">${record.frequency || '未知'}</td>
          </tr>
        </table>
      </div>
      
      <div style="margin-bottom: 20px;">
        <h2>异常波形</h2>
        <ul>
          ${record.anomalies && record.anomalies.length > 0
        ? record.anomalies.map(a => `<li>${a.type} (${a.severity === 'warning' ? '警告' : a.severity === 'danger' ? '危险' : '信息'})</li>`).join('')
        : '<li>未检测到异常波形</li>'}
        </ul>
      </div>
      
      <div style="margin-bottom: 20px;">
        <h2>文件信息</h2>
        <table style="width: 100%; border-collapse: collapse;">
          <tr>
            <td style="border: 1px solid #ddd; padding: 8px; width: 30%;">文件名</td>
            <td style="border: 1px solid #ddd; padding: 8px;">${record.fileName || '未知'}</td>
          </tr>
          <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">文件大小</td>
            <td style="border: 1px solid #ddd; padding: 8px;">${record.fileSize ? (record.fileSize / 1024 / 1024).toFixed(2) + ' MB' : '未知'}</td>
          </tr>
          ${record.startTime !== undefined && record.endTime !== undefined ? `
          <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">发作时间段</td>
            <td style="border: 1px solid #ddd; padding: 8px;">${record.startTime}s - ${record.endTime}s</td>
          </tr>` : ''}
        </table>
      </div>
      
      <div style="margin-top: 40px; text-align: right;">
        <p>分析医生: ${record.doctorName || '未知'}</p>
        <p>生成日期: ${new Date().toLocaleDateString('zh-CN')}</p>
      </div>
    `

    // 将元素添加到文档中
    document.body.appendChild(element)

    // 配置PDF选项
    const options = {
      margin: 10,
      filename: `${record.patientName}EEG分析报告_${record.createTime.split(' ')[0].replace(/-/g, '')}.pdf`,
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { scale: 2, useCORS: true },
      jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
    }

    // 生成PDF
    html2pdf().from(element).set(options).save().then(() => {
      // 移除临时元素
      document.body.removeChild(element)
      ElMessage.success(`已导出 ${record.patientName} 的检查记录`)
    }).catch(error => {
      console.error('PDF导出失败:', error)
      ElMessage.error('PDF导出失败: ' + error.message)
      // 确保临时元素被移除
      if (document.body.contains(element)) {
        document.body.removeChild(element)
      }
    })
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败: ' + error.message)
  }
}

// 优化查看记录功能 - 改为弹窗显示
const viewRecord = (record) => {
  if (!record) {
    ElMessage.warning('记录数据不完整')
    return
  }

  try {
    // 设置当前查看的记录
    currentRecord.value = record
    // 显示弹窗
    dialogVisible.value = true
  } catch (error) {
    console.error('查看记录失败:', error)
    ElMessage.error('查看记录失败: ' + error.message)
  }
}

// 补充完整的 EEG 通道列表
const channels = ref([
  { label: 'FP1-F7', value: 'FP1-F7' },
  { label: 'F7-T3', value: 'F7-T3' },
  { label: 'T3-T5', value: 'T3-T5' },
  { label: 'T5-O1', value: 'T5-O1' },
  { label: 'FP2-F8', value: 'FP2-F8' },
  { label: 'F8-T4', value: 'F8-T4' },
  { label: 'T4-T6', value: 'T4-T6' },
  { label: 'T6-O2', value: 'T6-O2' },
  { label: 'FP1-F3', value: 'FP1-F3' },
  { label: 'F3-C3', value: 'F3-C3' },
  { label: 'C3-P3', value: 'C3-P3' },
  { label: 'P3-O1', value: 'P3-O1' }
])

// 分页处理
const handleSizeChange = (val) => {
  pageSize.value = val
  // 获取数据
  getHistoryRecords()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  // 获取数据
  getHistoryRecords()
}


//分页查询历史分析记录
const getHistoryRecords = async () => {
  try {
    const params = {
      pageNum: currentPage.value,
      pageSize: pageSize.value,
      searchQuery: searchQuery.value,
      patientId: selectPatientId.value,
      userId: userInfo.value.id
    }
    const res = await getEegAnalysisListService(params)
    console.log(res)
    historyRecords.value = res.data.items
    console.log(historyRecords.value)
    total.value = res.data.total
  } catch (error) {
    ElMessage.error("查询失败:" + error.message)
  }
}



onMounted(() => {
  getPatients()
  getUserInfo()
  getHistoryRecords()
})
</script>




<style scoped>
.eeg-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.upload-section {
  margin-bottom: 20px;
}

.eeg-upload {
  width: 100%;
}

.wave-card {
  height: auto;
  width: auto;
  margin-top: 20px;
}

.wave-container {
  height: 100%;
  background: #f8f9fa;
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}

.result-card {
  height: 500px;
  overflow-y: auto;
}

.history-section {
  height: 500px;
  overflow-y: auto;
}

.analysis-results {
  padding: 10px;
}

.anomaly-tag {
  margin-right: 8px;
  margin-bottom: 8px;
  cursor: default;
}

.el-descriptions {
  margin-top: 10px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.analysis-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
}

.loading-icon {
  font-size: 48px;
  color: #409EFF;
  animation: rotate 2s linear infinite;
}

.loading-text {
  margin-top: 20px;
  font-size: 16px;
  color: #606266;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}
</style>






<style scoped>
.record-detail {
  padding: 20px;
}

.detail-section {
  margin: 20px 0;
}

.anomaly-tags {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
