<template>
  <div class="analysis-container">
    <h1 class="page-title">医疗分析报告</h1>
    
    <el-row :gutter="20">
      <!-- 脑电波分析结果 -->
      <el-col :span="12">
        <el-card class="analysis-card">
          <template #header>
            <div class="card-header">
              <span>dwt</span>
              <el-tag type="success">已完成</el-tag>
            </div>
          </template>
          <div class="image-container">
            <el-image 
              :src="analysisData.eegImage" 
              fit="contain"
              :preview-src-list="[analysisData.eegImage]">
              <template #error>
                <div class="image-placeholder">
                  <el-icon><Picture /></el-icon>
                  <span>暂无图片</span>
                </div>
              </template>
            </el-image>
            <div class="analysis-info">
              <p>检测时间：{{ analysisData.eegTime }}</p>
              <p>分析结果：{{ analysisData.eegResult }}</p>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- MRI扫描结果 -->
      <el-col :span="12">
        <el-card class="analysis-card">
          <template #header>
            <div class="card-header">
              <span>mi</span>
              <el-tag type="success">已完成</el-tag>
            </div>
          </template>
          <div class="image-container">
            <el-image 
              :src="analysisData.mriImage" 
              fit="contain"
              :preview-src-list="[analysisData.mriImage]">
              <template #error>
                <div class="image-placeholder">
                  <el-icon><Picture /></el-icon>
                  <span>暂无图片</span>
                </div>
              </template>
            </el-image>
            <div class="analysis-info">
              <p>检测时间：{{ analysisData.mriTime }}</p>
              <p>分析结果：{{ analysisData.mriResult }}</p>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- CT检查结果 -->
      <el-col :span="12">
        <el-card class="analysis-card">
          <template #header>
            <div class="card-header">
              <span>avarage psd</span>
              <el-tag type="success">已完成</el-tag>
            </div>
          </template>
          <div class="image-container">
            <el-image 
              :src="analysisData.ctImage" 
              fit="contain"
              :preview-src-list="[analysisData.ctImage]">
              <template #error>
                <div class="image-placeholder">
                  <el-icon><Picture /></el-icon>
                  <span>暂无图片</span>
                </div>
              </template>
            </el-image>
            <div class="analysis-info">
              <p>检测时间：{{ analysisData.ctTime }}</p>
              <p>分析结果：{{ analysisData.ctResult }}</p>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 血液检测结果 -->
      <el-col :span="12">
        <el-card class="analysis-card">
          <template #header>
            <div class="card-header">
              <span>zero_crossings</span>
              <el-tag type="success">已完成</el-tag>
            </div>
          </template>
          <div class="image-container">
            <el-image 
              :src="analysisData.bloodImage" 
              fit="contain"
              :preview-src-list="[analysisData.bloodImage]">
              <template #error>
                <div class="image-placeholder">
                  <el-icon><Picture /></el-icon>
                  <span>暂无图片</span>
                </div>
              </template>
            </el-image>
            <div class="analysis-info">
              <p>检测时间：{{ analysisData.bloodTime }}</p>
              <p>分析结果：{{ analysisData.bloodResult }}</p>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 综合评估结果 -->
      <el-col :span="24">
        <el-card class="analysis-card">
          <template #header>
            <div class="card-header">
              <span>stff_featureextraction2</span>
              <el-tag type="warning">待确认</el-tag>
            </div>
          </template>
          <div class="image-container">
            <el-image 
              :src="analysisData.overallImage" 
              fit="contain"
              :preview-src-list="[analysisData.overallImage]">
              <template #error>
                <div class="image-placeholder">
                  <el-icon><Picture /></el-icon>
                  <span>暂无图片</span>
                </div>
              </template>
            </el-image>
            <div class="analysis-info">
              <p>评估时间：{{ analysisData.overallTime }}</p>
              <p>评估结果：{{ analysisData.overallResult }}</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Picture } from '@element-plus/icons-vue'

// 模拟分析数据
const analysisData = ref({
  eegImage: 'http://example.com/eeg.jpg',
  eegTime: '2024-01-20 10:30',
  eegResult: '脑电波活动正常，无异常波形',

  mriImage: 'http://example.com/mri.jpg',
  mriTime: '2024-01-20 11:00',
  mriResult: '大脑结构完整，未见异常',

  ctImage: 'http://example.com/ct.jpg',
  ctTime: '2024-01-20 11:30',
  ctResult: '颅内未见异常密度影',

  bloodImage: 'http://example.com/blood.jpg',
  bloodTime: '2024-01-20 12:00',
  bloodResult: '各项指标在正常范围内',

  overallImage: 'http://example.com/overall.jpg',
  overallTime: '2024-01-20 14:00',
  overallResult: '综合各项检查结果，建议进一步随访观察'
})
</script>

<style scoped>
.analysis-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.page-title {
  text-align: center;
  color: #303133;
  margin-bottom: 30px;
  font-size: 28px;
}

.analysis-card {
  margin-bottom: 20px;
  transition: all 0.3s;
}

.analysis-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.image-container {
  position: relative;
  min-height: 300px;
}

.el-image {
  width: 100%;
  height: 300px;
  border-radius: 4px;
}

.image-placeholder {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 300px;
  background-color: #f5f7fa;
  color: #909399;
}

.image-placeholder .el-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.analysis-info {
  margin-top: 15px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.analysis-info p {
  margin: 5px 0;
  color: #606266;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .el-col {
    width: 100% !important;
  }
  
  .image-container {
    min-height: 200px;
  }
  
  .el-image {
    height: 200px;
  }
}
</style>