<template>
  <div class="analysis-container">
    <!-- 顶部文件上传区域 -->
    <el-card class="upload-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <span>脑电波数据分析</span>
            <el-tag type="info" v-if="currentFile" style="margin-left: 10px;">当前文件: {{ currentFile.name }}</el-tag>
          </div>
          <div class="header-right">
            <el-select v-model="selectPatientId" clearable placeholder="选择病人" style="margin-left: 20px; width: 240px;">
              <el-option v-for="item in patients" :key="item.name" :label="item.name" :value="item.id" />
            </el-select>
            <!-- 开始分析按钮 -->
            <el-button type="primary" @click="startAnalysis" :loading="analyzing">
              <el-icon class="el-icon--upload">
                <VideoPlay/>
              </el-icon>
              开始分析
            </el-button>
          </div>
        </div>
      </template>

      <div class="upload-area">
        <el-upload class="eeg-upload" drag action="#" :auto-upload="false" :on-change="handleFileChange"
                   :before-upload="beforeUpload" :limit="1">
          <el-icon class="el-icon--upload">
            <upload-filled/>
          </el-icon>
          <div class="el-upload__text">
            拖拽文件到此处或 <em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              支持 .edf, .csv 格式的脑电波数据文件，单个文件不超过50MB
            </div>
          </template>
        </el-upload>
        <div class="upload-actions" v-if="currentFile">
          <el-button type="primary" @click="uploadFile" :loading="uploading">上传文件</el-button>
          <el-button @click="clearFile" :disabled="uploading">清除文件</el-button>
        </div>
        <el-progress v-if="uploadProgress > 0 && uploadProgress < 100" :percentage="uploadProgress" :stroke-width="15"
                     status="success"></el-progress>
      </div>
    </el-card>
    
    <!-- 分析结果展示区域 -->
    <div v-if="fileProcessed" class="analysis-results">
      <!-- 分析方法选择 -->
      <el-card class="method-card">
        <div class="method-buttons">
          <el-radio-group v-model="currentAnalysisMethod" size="large">
            <el-radio-button label="zero_crossing">零交叉特征</el-radio-button>
            <el-radio-button label="stft">短时傅里叶变换</el-radio-button>
            <el-radio-button label="dwt">离散小波变换</el-radio-button>
          </el-radio-group>
        </div>
      </el-card>
      
      <!-- 过零点特征分析结果 -->
      <el-card v-if="currentAnalysisMethod === 'zero_crossing'" class="result-card">
        <template #header>
          <div class="card-header">
            <span>零交叉特征分析结果</span>
            <div>
              <el-button type="primary" size="small" @click="exportAnalysisResult">导出分析结果</el-button>
            </div>
          </div>
        </template>
        <div class="image-grid">
          <div v-for="(image, index) in analysisResult.features.zero_crossing.images" :key="index" class="image-item">
            <div class="image-title">{{ image.channel || `图像 ${index + 1}` }}</div>
            <el-image 
              :src="fixImageUrl(image.url)" 
              fit="contain"
              :preview-src-list="getPreviewList(analysisResult.features.zero_crossing.images)"
              :initial-index="index"
              class="analysis-image"
            >
              <template #error>
                <div class="image-error">
                  <el-icon><picture-filled /></el-icon>
                  <div>加载失败</div>
                </div>
              </template>
            </el-image>
          </div>
        </div>
      </el-card>
      
      <!-- 短时傅里叶变换分析结果 -->
      <el-card v-if="currentAnalysisMethod === 'stft'" class="result-card">
        <template #header>
          <div class="card-header">
            <span>短时傅里叶变换分析结果</span>
            <div>
              <el-button type="primary" size="small" @click="exportAnalysisResult">导出分析结果</el-button>
            </div>
          </div>
        </template>
        <div class="image-grid">
          <div v-for="(image, index) in analysisResult.features.stft.images" :key="index" class="image-item">
            <div class="image-title">{{ image.channel || `图像 ${index + 1}` }}</div>
            <el-image 
              :src="fixImageUrl(image.url)" 
              fit="contain"
              :preview-src-list="getPreviewList(analysisResult.features.stft.images)"
              :initial-index="index"
              class="analysis-image"
            >
              <template #error>
                <div class="image-error">
                  <el-icon><picture-filled /></el-icon>
                  <div>加载失败</div>
                </div>
              </template>
            </el-image>
          </div>
        </div>
      </el-card>
      
      <!-- 离散小波变换分析结果 -->
      <el-card v-if="currentAnalysisMethod === 'dwt'" class="result-card">
        <template #header>
          <div class="card-header">
            <span>离散小波变换分析结果</span>
            <div>
              <el-button type="primary" size="small" @click="exportAnalysisResult">导出分析结果</el-button>
            </div>
          </div>
        </template>
        <div class="image-grid">
          <div v-for="(image, index) in analysisResult.features.dwt.images" :key="index" class="image-item">
            <div class="image-title">{{ `小波变换图像 ${index + 1}` }}</div>
            <el-image 
              :src="fixImageUrl(image.url)" 
              fit="contain"
              :preview-src-list="getPreviewList(analysisResult.features.dwt.images)"
              :initial-index="index"
              class="analysis-image"
            >
              <template #error>
                <div class="image-error">
                  <el-icon><picture-filled /></el-icon>
                  <div>加载失败</div>
                </div>
              </template>
            </el-image>
          </div>
        </div>
      </el-card>
      
      <!-- 文件信息 -->
      <el-card v-if="analysisResult.file_name" class="file-info-card">
        <template #header>
          <div class="card-header">
            <span>文件信息</span>
          </div>
        </template>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="文件名">{{ analysisResult.file_name }}</el-descriptions-item>
          <el-descriptions-item label="文件大小">{{ formatFileSize(analysisResult.file_size) }}</el-descriptions-item>
          <el-descriptions-item label="患者ID">{{ selectPatientId }}</el-descriptions-item>
          <el-descriptions-item label="分析时间">{{ new Date().toLocaleString() }}</el-descriptions-item>
        </el-descriptions>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import {ref} from 'vue'
import {ElMessage, ElLoading} from 'element-plus'
import {UploadFilled, VideoPlay, PictureFilled} from '@element-plus/icons-vue'
import {getEegFeaturesService, uploadEegService} from '@/api/feature.js'
import {patientListAllService} from '@/api/patient.js'
import {userInfoService} from '@/api/user.js'
import {onMounted} from 'vue'
// 文件上传相关
const analyzing = ref(false)
const fileList = ref([])
const currentFile = ref(null)
const fileProcessed = ref(false)
const processing = ref(false)
const uploading = ref(false)
const uploadProgress = ref(0)
const temp =ref({
  "code": 200,
  "data": {
    "features": {
      "dwt": {
        "images": [
          {
            "url": "cloud.epilepsy-detect.xyz/28e7a11d-12b4-435c-93b8-050b8ee96a05.png"
          },
          {
            "url": "cloud.epilepsy-detect.xyz/8f565491-e0bb-4008-9857-30286e74a914.png"
          },
          {
            "url": "cloud.epilepsy-detect.xyz/18fc16c7-cc11-46ba-b73a-1a27e9163c6e.png"
          },
          {
            "url": "cloud.epilepsy-detect.xyz/a9554d8e-c88e-452c-b268-4e7dedfa786c.png"
          },
          {
            "url": "cloud.epilepsy-detect.xyz/313adbe8-2c4b-4574-8e4f-663dc3b8fd78.png"
          },
          {
            "url": "cloud.epilepsy-detect.xyz/fe158b70-78ce-413d-86e8-d622ab11b200.png"
          }
        ]
      },
      "stft": {
        "images": [
          {
            "channel": "FP1-F7",
            "url": "cloud.epilepsy-detect.xyz/5e31ca30-c1fa-4f5b-b99a-7375b81e506e.png"
          },
          {
            "channel": "F7-T7",
            "url": "cloud.epilepsy-detect.xyz/e4ed0763-6198-4995-92e0-184d14318882.png"
          },
          {
            "channel": "T7-P7",
            "url": "cloud.epilepsy-detect.xyz/3b8ce568-3373-4b39-9a33-7c2b147a2710.png"
          },
          {
            "channel": "P7-O1",
            "url": "cloud.epilepsy-detect.xyz/e1952b4d-95b2-442e-bfff-4104a0210c86.png"
          },
          {
            "channel": "FP1-F3",
            "url": "cloud.epilepsy-detect.xyz/363148d3-1f07-4a96-a47d-45159cc17cec.png"
          },
          {
            "channel": "汇总图",
            "url": "cloud.epilepsy-detect.xyz/e41672dd-4bfb-4893-b99c-fe6ab3f429e4.png"
          }
        ]
      },
      "zero_crossing": {
        "images": [
          {
            "channel": "FP1-F7",
            "url": "cloud.epilepsy-detect.xyz/1b07390a-9e31-4d9a-a6f8-234898ebc03a.png"
          },
          {
            "channel": "F7-T7",
            "url": "cloud.epilepsy-detect.xyz/313d3c26-6dc9-463e-b1c7-81ba59f9b5bf.png"
          },
          {
            "channel": "T7-P7",
            "url": "cloud.epilepsy-detect.xyz/4ab81076-9e4c-4cdc-81e9-20f010b10661.png"
          },
          {
            "channel": "P7-O1",
            "url": "cloud.epilepsy-detect.xyz/0e8e9416-54f6-4557-9b01-62e6336a7cf3.png"
          },
          {
            "channel": "FP1-F3",
            "url": "cloud.epilepsy-detect.xyz/5c25c635-612f-4ff1-a5f7-d8c5c4abaa4c.png"
          },
          {
            "channel": "汇总图",
            "url": "cloud.epilepsy-detect.xyz/e8045e1b-57f2-4b41-9291-a0e686ec5553.png"
          }
        ]
      }
    },
    "file_name": "ca2ce5fd-461d-472c-a55c-3d46b6ae5736.edf",
    "file_size": 42399744
  },
  "message": "特征提取成功"
})
//可视化分析结果
const analysisResult = ref({})
// 当前选择的分析方法
const currentAnalysisMethod = ref('zero_crossing') // 默认显示过零点特征
//患者列表
const patients = ref([])
const selectPatientId = ref('')
//用户信息
const userInfo = ref({})
onMounted(() => {
  //获取病人列表
  getPatients()
  //获取用户信息
  getUserInfo()
})


const startAnalysis = async () => {
  // 移除这行，它过早地设置了处理完成状态
  // fileProcessed.value = true
  
  // 判断文件和患者是否选择
  if (!currentFile.value || !selectPatientId.value) {
    ElMessage.error('请上传文件同时选择患者')
    return
  }
  
  //开始分析
  analyzing.value = true
  //清空分析结果
  analysisResult.value = null
  
  try {
    let params = {
      patientId: selectPatientId.value,
      userId: userInfo.value.id
    }
    // let res = await getEegFeaturesService(params)
    // 处理返回的数据结构
    // analysisResult.value = res.data.data;
    analysisResult.value = temp.value.data;
    // 在成功获取数据后再设置处理完成状态
    fileProcessed.value = true
    console.log('分析结果:', analysisResult.value)
    ElMessage.success('分析完成')
  }catch (error) {
    ElMessage.error('分析失败：' + error.message)
  }finally {
    //关闭分析加载动画
    analyzing.value = false
  }
}
//获得用户信息
const getUserInfo = async () => {
  try {
    const res = await userInfoService()
    userInfo.value = res.data
    console.log('用户信息:', userInfo.value.id)
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}
// 获取患者列表
const getPatients = async () => {
  try {
    const res = await patientListAllService()
    patients.value = res.data  // 使用 .value 因为 patients 是一个 ref
  } catch (error) {
    console.error('获取患者失败:', error)
  }
}
// 上传前验证
const beforeUpload = (file) => {
  // 检查文件类型
  const validTypes = ['.edf', '.csv']
  const extension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase()
  const isValidType = validTypes.includes(extension)

  if (!isValidType) {
    ElMessage.error('只能上传.edf或.csv格式的脑电波数据文件!')
    return false
  }

  // 检查文件大小
  const isLt50M = file.size / 1024 / 1024 < 50
  if (!isLt50M) {
    ElMessage.error('文件大小不能超过50MB!')
    return false
  }

  return true
}

// 文件变更处理
const handleFileChange = (file) => {
  currentFile.value = file.raw
  fileList.value = [file]
}

// 清除文件
const clearFile = () => {
  currentFile.value = null
  fileList.value = []
  fileProcessed.value = false
  uploadProgress.value = 0
}

// 上传文件到服务器

const uploadFile = async () => {
  // 检查必要参数是否有效
  if (!currentFile.value || !selectPatientId.value || !userInfo.value.id) {
    ElMessage.error('请确保文件、患者ID和用户信息均有效');
    return;
  }

  const uploadParams = {
    file: currentFile.value,
    patientId: selectPatientId.value,
    userId: userInfo.value.id
  };

  try {
    uploading.value = true;
    uploadProgress.value = 0;

    const res = await uploadEegService(uploadParams);

    if (res.code === 0) {
      ElMessage.success('文件上传成功');
      resetUploadState();
    } else {
      ElMessage.error(`文件上传失败，服务器返回：${res.message || '未知错误'}`);
      resetUploadState();
    }
  } catch (error) {
    console.error('文件上传失败:', error);
    ElMessage.error(`文件上传失败：${error.message || '未知错误'}`);
    resetUploadState();
  }
};

// 提取状态重置逻辑，减少冗余代码
const resetUploadState = () => {
  uploading.value = false;
  uploadProgress.value = 0;
};

// 获取图片预览列表
const getPreviewList = (images) => {
  if (!images || !Array.isArray(images)) return [];
  return images.map(img => fixImageUrl(img.url));
};

// 修复图片URL（添加缺少的//）
const fixImageUrl = (url) => {
  if (url && url.startsWith('http:')) {
    return url.replace('http:', 'http://');
  }
  return url;
};

// 格式化文件大小
const formatFileSize = (bytes) => {
  if (!bytes) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

// 导出分析结果
const exportAnalysisResult = async () => {
  try {
    // 显示加载提示
    const loadingInstance = ElLoading.service({
      text: '正在生成分析报告...',
      background: 'rgba(0, 0, 0, 0.7)'
    });
    
    // 导入所需库
    const html2canvas = (await import('html2canvas')).default;
    const jsPDF = (await import('jspdf')).default;
    
    // 获取当前选中的患者信息
    const selectedPatient = patients.value.find(p => p.id === selectPatientId.value) || {};
    
    // 创建一个临时的报告容器
    const reportContainer = document.createElement('div');
    reportContainer.style.width = '800px';
    reportContainer.style.padding = '20px';
    reportContainer.style.position = 'absolute';
    reportContainer.style.left = '-9999px';
    reportContainer.innerHTML = `
      <h1 style="text-align: center; margin-bottom: 20px;">脑电波数据分析报告</h1>
      <div style="margin-bottom: 20px;">
        <p><strong>患者姓名:</strong> ${selectedPatient.name || '未知'}</p>
        <p><strong>患者ID:</strong> ${selectPatientId.value || '未知'}</p>
        <p><strong>分析时间:</strong> ${new Date().toLocaleString()}</p>
        <p><strong>文件名:</strong> ${analysisResult.value.file_name || '未知'}</p>
        <p><strong>文件大小:</strong> ${formatFileSize(analysisResult.value.file_size) || '未知'}</p>
        <p><strong>分析方法:</strong> ${getAnalysisMethodName(currentAnalysisMethod.value)}</p>
      </div>
    `;
    
    // 添加图片
    const images = analysisResult.value.features[currentAnalysisMethod.value].images;
    for (let i = 0; i < images.length; i++) {
      const image = images[i];
      const title = image.channel ? `通道: ${image.channel}` : `图像 ${i + 1}`;
      
      const imgContainer = document.createElement('div');
      imgContainer.style.marginBottom = '20px';
      imgContainer.innerHTML = `
        <h3>${title}</h3>
        <img src="${fixImageUrl(image.url)}" style="max-width: 100%; border: 1px solid #ddd;" />
      `;
      
      reportContainer.appendChild(imgContainer);
    }
    
    document.body.appendChild(reportContainer);
    
    // 使用html2canvas将报告转换为图片
    const canvas = await html2canvas(reportContainer, {
      scale: 2, // 提高清晰度
      useCORS: true, // 允许加载跨域图片
      logging: false
    });
    
    document.body.removeChild(reportContainer);
    
    // 创建PDF
    const imgData = canvas.toDataURL('image/jpeg', 0.8);
    const pdf = new jsPDF('p', 'mm', 'a4');
    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();
    
    // 计算图片在PDF中的尺寸
    const imgWidth = pageWidth;
    const imgHeight = (canvas.height * imgWidth) / canvas.width;
    
    // 分页处理
    let heightLeft = imgHeight;
    let position = 0;
    let page = 1;
    
    pdf.addImage(imgData, 'JPEG', 0, position, imgWidth, imgHeight);
    heightLeft -= pageHeight;
    
    // 如果内容超过一页，添加新页
    while (heightLeft > 0) {
      position = heightLeft - imgHeight;
      pdf.addPage();
      pdf.addImage(imgData, 'JPEG', 0, position, imgWidth, imgHeight);
      heightLeft -= pageHeight;
      page++;
    }
    
    // 生成文件名
    const fileName = `脑电波分析报告_${selectedPatient.name || '未知'}_${new Date().toISOString().slice(0, 10)}.pdf`;
    
    // 保存PDF
    pdf.save(fileName);
    
    // 关闭加载提示
    loadingInstance.close();
    
    ElMessage.success('分析报告已成功导出');
  } catch (error) {
    console.error('导出分析失败:', error);
    ElMessage.error(`导出失败: ${error.message}`);
  }
};

// 获取分析方法的中文名称
const getAnalysisMethodName = (method) => {
  const methodNames = {
    'zero_crossing': '零交叉特征分析',
    'stft': '短时傅里叶变换分析',
    'dwt': '离散小波变换分析'
  };
  return methodNames[method] || method;
};

</script>

<style scoped>
.analysis-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.upload-card {
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.upload-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.eeg-upload {
  width: 100%;
}

.upload-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.analysis-content {
  margin-top: 20px;
  min-height: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* 分析结果样式 */
.analysis-results {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.method-card {
  width: 100%;
}

.method-buttons {
  display: flex;
  justify-content: center;
  padding: 10px 0;
}

.result-card {
  width: 100%;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 10px;
}

.image-item {
  display: flex;
  flex-direction: column;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  overflow: hidden;
}

.image-title {
  padding: 8px;
  background-color: #f5f7fa;
  font-weight: bold;
  text-align: center;
}

.analysis-image {
  height: 250px;
  width: 100%;
  background-color: #f5f7fa;
}

.image-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;
}

.file-info-card {
  width: 100%;
}

.header-left {
  display: flex;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>