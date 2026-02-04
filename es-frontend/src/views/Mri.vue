<template>
  <div class="mri-container">
    <!-- 顶部操作区 -->
    <el-card class="upload-section">
      <template #header>
        <div class="section-header">
          <span class="title">MRI 影像分析</span>
          <div class="action-buttons">
            <el-button type="primary" @click="startAnalysis" :loading="analyzing">
              <el-icon><Connection /></el-icon>
              开始分析
            </el-button>
            <el-button type="success" @click="view3D" :disabled="!hasData">
              <el-icon><View /></el-icon>
              3D视图
            </el-button>
          </div>
        </div>
      </template>

      <!-- 文件上传区 -->
      <el-upload
        class="mri-upload"
        drag
        :action="uploadUrl"
        :before-upload="beforeUpload"
        :on-success="handleUploadSuccess"
        :on-error="handleUploadError"
        accept=".dcm,.nii,.nii.gz"
        multiple
      >
        <el-icon class="el-icon--upload"><Upload /></el-icon>
        <div class="el-upload__text">
          拖拽MRI文件到此处或 <em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支持DICOM(.dcm)和NIfTI(.nii/.nii.gz)格式，可多选上传
          </div>
        </template>
      </el-upload>
    </el-card>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <el-row :gutter="20">
        <!-- 左侧：图像显示区 -->
        <el-col :span="16">
          <el-card class="viewer-card">
            <template #header>
              <div class="section-header">
                <span>影像查看器</span>
                <div class="viewer-controls">
                  <el-select v-model="currentView" placeholder="选择视图" size="small">
                    <el-option label="轴向" value="axial" />
                    <el-option label="冠状" value="coronal" />
                    <el-option label="矢状" value="sagittal" />
                  </el-select>
                  <el-button-group>
                    <el-button size="small" @click="adjustContrast">
                      <el-icon><Sunny /></el-icon>
                    </el-button>
                    <el-button size="small" @click="zoomIn">
                      <el-icon><ZoomIn /></el-icon>
                    </el-button>
                    <el-button size="small" @click="zoomOut">
                      <el-icon><ZoomOut /></el-icon>
                    </el-button>
                  </el-button-group>
                </div>
              </div>
            </template>
            <div class="viewer-container" ref="viewerContainer">
              <!-- MRI图像将在这里渲染 -->
              <div v-if="!hasData" class="empty-viewer">
                <el-empty description="请上传MRI数据" />
              </div>
            </div>
            <div class="slice-control" v-if="hasData">
              <el-slider v-model="currentSlice" :max="maxSlice" @input="updateSlice" />
            </div>
          </el-card>
        </el-col>

        <!-- 右侧：分析结果 -->
        <el-col :span="8">
          <el-card class="analysis-card">
            <template #header>
              <div class="section-header">
                <span>AI 分析结果</span>
                <el-button type="primary" link @click="exportReport">
                  <el-icon><Document /></el-icon>
                  导出报告
                </el-button>
              </div>
            </template>
            <div v-if="analysisResults" class="analysis-results">
              <!-- 病变检测结果 -->
              <div class="result-section">
                <h4>病变检测</h4>
                <el-descriptions :column="1" border>
                  <el-descriptions-item label="病变类型">
                    {{ analysisResults.lesionType }}
                  </el-descriptions-item>
                  <el-descriptions-item label="位置">
                    {{ analysisResults.location }}
                  </el-descriptions-item>
                  <el-descriptions-item label="大小">
                    {{ analysisResults.size }}
                  </el-descriptions-item>
                </el-descriptions>
              </div>

              <!-- 风险评估 -->
              <div class="result-section">
                <h4>风险评估</h4>
                <el-progress 
                  :percentage="analysisResults.riskLevel"
                  :color="getRiskColor"
                  :format="format"
                />
              </div>

              <!-- 关键发现 -->
              <div class="result-section">
                <h4>关键发现</h4>
                <el-timeline>
                  <el-timeline-item
                    v-for="(finding, index) in analysisResults.findings"
                    :key="index"
                    :type="finding.severity"
                    :color="finding.color"
                  >
                    {{ finding.description }}
                  </el-timeline-item>
                </el-timeline>
              </div>

              <!-- AI建议 -->
              <div class="result-section">
                <h4>AI建议</h4>
                <el-alert
                  v-for="(suggestion, index) in analysisResults.suggestions"
                  :key="index"
                  :title="suggestion.title"
                  :type="suggestion.type"
                  :description="suggestion.content"
                  show-icon
                />
              </div>
            </div>
            <el-empty v-else description="暂无分析结果" />
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 历史记录表格 -->
    <el-card class="history-section">
      <template #header>
        <div class="section-header">
          <span>检查历史</span>
          <el-input
            v-model="searchQuery"
            placeholder="搜索患者信息"
            prefix-icon="Search"
            style="width: 200px"
          />
        </div>
      </template>
      <el-table :data="historyRecords" style="width: 100%">
        <el-table-column prop="date" label="检查日期" width="180" />
        <el-table-column prop="patientName" label="患者姓名" width="120" />
        <el-table-column prop="patientId" label="患者ID" width="120" />
        <el-table-column prop="scanType" label="扫描类型" width="120" />
        <el-table-column prop="result" label="分析结果" width="120">
          <template #default="scope">
            <el-tag :type="getResultType(scope.row.result)">
              {{ scope.row.result }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="doctor" label="审核医生" width="120" />
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
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 3D视图对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="3D立体重建"
      width="80%"
      :before-close="handleClose"
    >
      <div class="three-d-viewer" ref="threeDViewer">
        <!-- 3D渲染将在这里展示 -->
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">关闭</el-button>
          <el-button type="primary" @click="save3DView">
            保存视图
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Upload,
  Connection,
  Document,
  View,
  ZoomIn,
  ZoomOut,
  Sunny,
  Search
} from '@element-plus/icons-vue'

// 基础状态
const uploadUrl = '/api/mri/upload'
const analyzing = ref(false)
const hasData = ref(false)
const dialogVisible = ref(false)

// 视图控制
const currentView = ref('axial')
const currentSlice = ref(0)
const maxSlice = ref(100)
const viewerContainer = ref(null)
const threeDViewer = ref(null)

// 分析结果
const analysisResults = ref(null)

// 搜索和分页
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 历史记录
const historyRecords = ref([
  {
    date: '2024-01-20',
    patientName: '张三',
    patientId: 'P001',
    scanType: 'T1加权',
    result: '异常',
    doctor: '李医生'
  }
  // ... 其他记录
])

// 文件上传处理
const beforeUpload = (file) => {
  const validTypes = ['.dcm', '.nii', '.nii.gz']
  const isValidType = validTypes.some(type => file.name.toLowerCase().endsWith(type))
  const isLt2G = file.size / 1024 / 1024 / 1024 < 2

  if (!isValidType) {
    ElMessage.error('请上传正确格式的MRI文件!')
    return false
  }
  if (!isLt2G) {
    ElMessage.error('文件大小不能超过 2GB!')
    return false
  }
  return true
}

const handleUploadSuccess = (response) => {
  ElMessage.success('文件上传成功')
  hasData.value = true
  // 处理上传成功后的逻辑
}

const handleUploadError = () => {
  ElMessage.error('文件上传失败')
}

// 分析控制
const startAnalysis = async () => {
  if (!hasData.value) {
    ElMessage.warning('请先上传MRI数据')
    return
  }

  analyzing.value = true
  try {
    // 模拟分析过程
    await new Promise(resolve => setTimeout(resolve, 2000))
    analysisResults.value = {
      lesionType: '海马体硬化',
      location: '左侧颞叶',
      size: '2.5 x 1.8 x 1.6 cm',
      riskLevel: 85,
      findings: [
        {
          description: '发现海马体体积减小',
          severity: 'warning',
          color: '#E6A23C'
        },
        {
          description: '信号异常增强',
          severity: 'danger',
          color: '#F56C6C'
        }
      ],
      suggestions: [
        {
          title: '建议进行详细评估',
          type: 'warning',
          content: '建议进行神经心理学评估和脑电图检查'
        }
      ]
    }
    ElMessage.success('分析完成')
  } catch (error) {
    ElMessage.error('分析失败')
  } finally {
    analyzing.value = false
  }
}

// 视图控制
const updateSlice = (value) => {
  // 更新切片显示
  console.log('更新切片:', value)
}

const adjustContrast = () => {
  // 调整对比度
}

const zoomIn = () => {
  // 放大视图
}

const zoomOut = () => {
  // 缩小视图
}

// 3D视图控制
const view3D = () => {
  dialogVisible.value = true
  // 初始化3D视图
}

const save3DView = () => {
  ElMessage.success('3D视图已保存')
  dialogVisible.value = false
}

const handleClose = (done) => {
  done()
}

// 风险等级颜色
const getRiskColor = (percentage) => {
  if (percentage > 70) return '#F56C6C'
  if (percentage > 30) return '#E6A23C'
  return '#67C23A'
}

const format = (percentage) => {
  return percentage === 100 ? '满' : `${percentage}%`
}

// 结果类型样式
const getResultType = (result) => {
  const types = {
    '正常': 'success',
    '异常': 'danger',
    '待复查': 'warning'
  }
  return types[result] || 'info'
}

// 导出功能
const exportReport = () => {
  ElMessage.success('报告导出中...')
}

const exportRecord = (record) => {
  console.log('导出记录:', record)
}

// 查看记录
const viewRecord = (record) => {
  console.log('查看记录:', record)
}

// 分页处理
const handleSizeChange = (val) => {
  pageSize.value = val
  // 获取数据
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  // 获取数据
}

onMounted(() => {
  // 初始化操作
})
</script>

<style scoped>
.mri-container {
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

.title {
  font-size: 18px;
  font-weight: bold;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.viewer-card {
  height: 600px;
}

.viewer-container {
  height: calc(100% - 60px);
  background: #000;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-viewer {
  color: #fff;
}

.viewer-controls {
  display: flex;
  gap: 10px;
  align-items: center;
}

.slice-control {
  margin-top: 10px;
}

.analysis-card {
  height: 600px;
  overflow-y: auto;
}

.result-section {
  margin-bottom: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 4px;
}

.result-section h4 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #303133;
}

.three-d-viewer {
  height: 600px;
  background: #000;
  border-radius: 4px;
}

.history-section {
  margin-top: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.el-alert {
  margin-bottom: 10px;
}
</style>

