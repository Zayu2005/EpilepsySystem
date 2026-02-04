<template>
  <div class="chat-page">
    <el-container>
      <!-- Patient Sidebar -->
      <el-aside width="300px">
        <div class="patient-select">
          <div class="back-button">
            <el-button link @click="goBack" class="back-btn">
              <el-icon><Back /></el-icon>
              返回首页
            </el-button>
          </div>
          <div class="select-header">
            <h3>选择患者</h3>
            <el-input
                v-model="searchText"
                placeholder="搜索患者"
                prefix-icon="Search"
                clearable
                size="small"
                class="search-input"
            />
          </div>
          <div class="patient-list">
            <div
                v-for="patient in filteredPatients"
                :key="patient.id"
                :class="['patient-item', { active: currentPatient?.id === patient.id }]"
                @click="selectPatient(patient)"
            >
              <el-avatar :size="40" :class="['patient-avatar', { 'pulse': currentPatient?.id === patient.id }]">
                {{ patient.name.slice(0, 1) }}
              </el-avatar>
              <div class="patient-info">
                <div class="patient-name">{{ patient.name }}</div>
                <div v-if="patient.diagnosis" class="patient-detail">{{ patient.diagnosis }}</div>
              </div>
            </div>
            <div v-if="filteredPatients.length === 0" class="no-patients">
              <el-empty description="未找到匹配的患者" :image-size="80" />
            </div>
          </div>
        </div>
      </el-aside>

      <!-- Main Chat Area -->
      <el-container>
        <el-header height="60px">
          <div class="chat-header">
            <div class="patient-brief" v-if="currentPatient">
              <span class="name">{{ currentPatient.name }}</span>
              <span class="info">{{ currentPatient.age }}岁 {{ currentPatient.male }}</span>
              <el-tag v-if="currentPatient.diagnosis" size="small" type="info" class="diagnosis-tag">
                {{ currentPatient.diagnosis }}
              </el-tag>
            </div>
            <div class="header-actions">
              <el-tooltip content="生成病例报告" placement="bottom" :enterable="false">
                <el-button type="primary" plain size="small" @click="exportPDF" class="action-btn">
                  <el-icon class="icon"><Document /></el-icon>
                  生成病例报告
                </el-button>
              </el-tooltip>
              <el-tooltip content="清空当前对话" placement="bottom" :enterable="false">
                <el-button type="primary" plain size="small" @click="clearChat" class="action-btn">
                  <el-icon class="icon"><Delete /></el-icon>
                  清空对话
                </el-button>
              </el-tooltip>
            </div>
          </div>
        </el-header>

        <el-main>
          <div class="chat-container" ref="chatContainer">
            <div class="chat-messages">
              <div
                  v-for="(message, index) in messages"
                  :key="index"
                  :class="['message', message.role, {'new-message': index === messages.length - 1}]"
              >
                <el-avatar :size="36" :class="message.role === 'assistant' ? 'assistant-avatar' : 'user-avatar'">
                  {{ message.role === 'assistant' ? 'AI' : '我' }}
                </el-avatar>
                <div class="message-content">
                  <MarkdownRenderer :content="message.content" />
                  <div class="message-actions">
                    <el-tooltip content="导出此消息" placement="top" :enterable="false">
                      <el-button
                          type="text"
                          size="small"
                          class="export-message-btn"
                          @click="exportSingleMessage(message, index)"
                      >
                        <el-icon><Download /></el-icon>
                      </el-button>
                    </el-tooltip>
                  </div>
                </div>
              </div>
              <div v-if="isTyping" class="typing-indicator">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
              </div>
            </div>
          </div>
        </el-main>

        <el-footer height="140px">
          <div class="chat-input">
            <el-input
                v-model="inputMessage"
                type="textarea"
                :rows="3"
                placeholder="输入您的问题..."
                @keyup.enter.ctrl="sendMessage"
                :disabled="!currentPatient"
                class="message-textarea"
            />
            <div class="input-actions">
              <span class="tip">Ctrl + Enter 发送</span>
              <el-button
                  type="primary"
                  @click="sendMessage"
                  :disabled="!currentPatient || !inputMessage.trim()"
                  class="send-button"
              >
                发送
              </el-button>
            </div>
          </div>
        </el-footer>
      </el-container>
    </el-container>

    <!-- Virtual Assistant -->
    <div class="virtual-assistant">
      <img src="@/assets/虚拟形象-min.gif" alt="AI助手" class="virtual-assistant-gif" @click="toggleAssistantInfo" />
      <div v-if="showAssistantInfo" class="assistant-info">
        <div class="assistant-info-content">
          <h4>AI医疗助手</h4>
          <p>我可以帮您分析病例、解答医学问题</p>
        </div>
      </div>
    </div>

    <!-- Export Format Dialog -->
    <el-dialog
        v-model="exportDialogVisible"
        title="选择导出格式"
        width="300px"
        :destroy-on-close="true"
        center
    >
      <div class="export-format-options">
        <el-button @click="confirmExport('txt')" class="format-btn">
          <el-icon><Document /></el-icon>
          文本文件 (.txt)
        </el-button>
        <el-button @click="confirmExport('md')" class="format-btn">
          <el-icon><Edit /></el-icon>
          Markdown (.md)
        </el-button>
        <el-button @click="confirmExport('pdf')" class="format-btn">
          <el-icon><Printer /></el-icon>
          PDF文档 (.pdf)
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Back, Document, Delete, Search, Download, Edit, Printer } from '@element-plus/icons-vue'
import MarkdownRenderer from '@/components/MarkdownRenderer.vue'
import { patientListAllService } from "@/api/patient.js"
import { ElMessage } from 'element-plus'
import html2pdf from 'html2pdf.js'
import { marked } from 'marked'
import hljs from 'highlight.js'

// Router setup
const router = useRouter()
const goBack = () => router.push('/home')

// State management
const searchText = ref('')
const inputMessage = ref('')
const currentPatient = ref(null)
const chatContainer = ref(null)
const patients = ref([])
const messages = ref([
  {
    role: 'assistant',
    content: '您好，我是您的AI医疗助手。请问有什么可以帮您分析的？'
  }
])
const isTyping = ref(false)
const showAssistantInfo = ref(false)

// Export dialog state
const exportDialogVisible = ref(false)
const currentExportMessage = ref(null)
const currentExportIndex = ref(null)

// Computed properties
const filteredPatients = computed(() => {
  if (!searchText.value) return patients.value

  const query = searchText.value.toLowerCase()
  return patients.value.filter(patient =>
      patient.name.toLowerCase().includes(query) ||
      (patient.diagnosis && patient.diagnosis.toLowerCase().includes(query))
  )
})

// Methods
const toggleAssistantInfo = () => {
  showAssistantInfo.value = !showAssistantInfo.value
  setTimeout(() => {
    showAssistantInfo.value = false
  }, 3000)
}

const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

const getPatients = async() => {
  try {
    const res = await patientListAllService()
    patients.value = res.data
  } catch (error) {
    console.error('获取患者失败:', error)
    ElMessage.error('获取患者列表失败，请稍后重试')
  }
}

const selectPatient = (patient) => {
  currentPatient.value = patient
  messages.value = [
    {
      role: 'assistant',
      content: '正在加载病人信息，AI助手小智正在分析...'
    }
  ]
  isTyping.value = true

  // 构建病人信息
  const patientInfo = `患者姓名：${patient.name}，年龄：${patient.age}岁，性别：${patient.male}${patient.diagnosis ? `，诊断：${patient.diagnosis}` : ''}${patient.text ? `，病情描述：${patient.text}` : ''}`

  // 自动发送病人信息
  const params = new URLSearchParams({
    prompt: patientInfo,
    sessionId: `patient_${patient.id}`
  })

  const eventSource = new EventSource(`/api/chat/patient?${params.toString()}`)

  let assistantMessage = {
    role: 'assistant',
    content: ''
  }
  messages.value.push(assistantMessage)

  eventSource.onmessage = (event) => {
    // 移除所有的 # 标题符号
    const formattedData = event.data.replace(/^#{1,6}\s*/gm, '')
    assistantMessage.content += formattedData
    messages.value = [...messages.value]
    scrollToBottom()
  }

  eventSource.onerror = (error) => {
    console.error('SSE Error:', error)
    if (!assistantMessage.content) {
      assistantMessage.content = '抱歉，服务出现错误，请稍后重试。'
    }
    messages.value[0].content = `您好，我是您的AI医疗助手小智。我已经了解了${patient.name}的基本情况。${patient.text ? `\n\n主要情况：${patient.text}` : ''}\n\n请问您想了解哪些具体问题？`
    eventSource.close()
    isTyping.value = false
  }

  eventSource.onopen = () => {
    console.log('SSE connection opened')
    messages.value[0].content = `正在分析${patient.name}的病历信息，请稍候...`
  }
}

const sendMessage = () => {
  if (!inputMessage.value.trim() || !currentPatient.value) return

  const userMessage = inputMessage.value
  messages.value.push({
    role: 'user',
    content: userMessage
  })

  // 清空输入
  inputMessage.value = ''
  scrollToBottom()
  isTyping.value = true

  // 构建请求URL，添加sessionId参数
  const params = new URLSearchParams({
    prompt: userMessage,
    sessionId: `patient_${currentPatient.value.id}`
  })

  // 调用后端接口
  const eventSource = new EventSource(`/api/chat/patient?${params.toString()}`)

  let assistantMessage = {
    role: 'assistant',
    content: ''
  }
  messages.value.push(assistantMessage)

  eventSource.onmessage = (event) => {
    // 移除所有的 # 标题符号
    const formattedData = event.data.replace(/^#{1,6}\s*/gm, '')
    assistantMessage.content += formattedData
    messages.value = [...messages.value]
    scrollToBottom()
  }

  eventSource.onerror = (error) => {
    console.error('SSE Error:', error)
    if (!assistantMessage.content) {
      assistantMessage.content = '抱歉，服务出现错误，请稍后重试。'
    }
    eventSource.close()
    isTyping.value = false
  }

  eventSource.onopen = () => {
    console.log('SSE connection opened')
  }
}

const clearChat = () => {
  ElMessage({
    message: '对话已清空',
    type: 'success',
    duration: 2000
  })

  messages.value = [
    {
      role: 'assistant',
      content: '对话已清空，请问有什么可以帮您分析的？'
    }
  ]
}

// 导出单条消息
const exportSingleMessage = (message, index) => {
  currentExportMessage.value = message
  currentExportIndex.value = index
  exportDialogVisible.value = true
}

// 确认导出格式并执行导出
const confirmExport = (format) => {
  if (!currentExportMessage.value) return

  const message = currentExportMessage.value
  const index = currentExportIndex.value
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
  const role = message.role === 'assistant' ? 'AI回复' : '我的提问'
  const fileName = `${currentPatient.value ? currentPatient.value.name + '_' : ''}${role}_${index + 1}_${timestamp}`

  switch (format) {
    case 'txt':
      exportAsText(message.content, fileName)
      break
    case 'md':
      exportAsMarkdown(message.content, fileName)
      break
    case 'pdf':
      exportAsPDF(message, fileName)
      break
  }

  exportDialogVisible.value = false
}

// 导出为纯文本
const exportAsText = (content, fileName) => {
  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' })
  saveFile(blob, `${fileName}.txt`)
  ElMessage.success('文本文件导出成功')
}

// 导出为Markdown
const exportAsMarkdown = (content, fileName) => {
  // 确保Markdown格式正确
  const formattedContent = content
      // 将没有空格的标题格式 (#标题) 替换为正确的格式 (# 标题)
      .replace(/^(#{1,6})([^\s])/gm, '$1 $2')
      // 确保标题前后有换行符以便正确渲染
      .replace(/^(#{1,6}\s.+)$/gm, '\n$1\n')

  const blob = new Blob([formattedContent], { type: 'text/markdown;charset=utf-8' })
  saveFile(blob, `${fileName}.md`)
  ElMessage.success('Markdown文件导出成功')
}

// 导出为PDF
const exportAsPDF = (message, fileName) => {
  // 配置 marked 选项
  marked.setOptions({
    headerIds: true,
    mangle: false,
    headerPrefix: 'heading-',
    highlight: function(code, lang) {
      if (lang && hljs.getLanguage(lang)) {
        return hljs.highlight(code, { language: lang }).value
      }
      return hljs.highlightAuto(code).value
    },
    breaks: true,
    gfm: true
  })

  const currentDate = new Date().toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })

  // 处理 Markdown 内容
  const processedContent = message.content
      // 将没有空格的标题格式 (#标题) 替换为正确的格式 (# 标题)
      .replace(/^(#{1,6})([^\s])/gm, '$1 $2')
      // 确保标题前后有换行符以便正确渲染
      .replace(/^(#{1,6}\s.+)$/gm, '\n$1\n')

  const element = document.createElement('div')

  element.innerHTML = `
    <div style="padding: 20px; font-family: SimSun, serif;">
      <h1 style="text-align: center; margin-bottom: 30px; font-size: 24px; color: #333;">
        ${message.role === 'assistant' ? 'AI医疗助手回复' : '医生提问'}
      </h1>

      ${currentPatient.value ? `
      <div style="margin-bottom: 30px; padding: 15px; background-color: #f8f9fa; border-radius: 8px; border: 1px solid #e6e6e6;">
        <p><strong>患者：</strong>${currentPatient.value.name} | ${currentPatient.value.age}岁 | ${currentPatient.value.male}</p>
        ${currentPatient.value.diagnosis ? `<p><strong>诊断：</strong>${currentPatient.value.diagnosis}</p>` : ''}
      </div>
      ` : ''}

      <div style="padding: 15px; background-color: ${message.role === 'assistant' ? '#f5f7fa' : '#f0f9eb'};
                  border-radius: 8px; border: 1px solid ${message.role === 'assistant' ? '#e6e6e6' : '#e1f3d8'};
                  line-height: 1.6; font-size: 14px; margin-bottom: 20px;">
        ${marked.parse(processedContent)}
      </div>

      <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #EBEEF5; text-align: center;">
        <p style="color: #909399; font-size: 12px;">导出时间：${currentDate}</p>
      </div>
    </div>
  `

  // 添加样式以支持代码高亮和Markdown样式
  const style = document.createElement('style')
  style.textContent = `
    h1, h2, h3, h4, h5, h6 {
      margin-top: 24px;
      margin-bottom: 16px;
      font-weight: 600;
      line-height: 1.25;
    }
    h1 {
      font-size: 2em;
      border-bottom: 1px solid #eaecef;
      padding-bottom: 0.3em;
    }
    h2 {
      font-size: 1.5em;
      border-bottom: 1px solid #eaecef;
      padding-bottom: 0.3em;
    }
    h3 {
      font-size: 1.25em;
    }
    h4 {
      font-size: 1em;
    }
    h5 {
      font-size: 0.875em;
    }
    h6 {
      font-size: 0.85em;
      color: #6a737d;
    }
    pre {
      background-color: #f6f8fa;
      border-radius: 6px;
      padding: 16px;
      overflow: auto;
    }
    code {
      font-family: Consolas, Monaco, 'Andale Mono', monospace;
      font-size: 14px;
    }
    table {
      border-collapse: collapse;
      width: 100%;
      margin: 16px 0;
    }
    th, td {
      border: 1px solid #dfe2e5;
      padding: 8px 12px;
    }
    th {
      background-color: #f6f8fa;
    }
    blockquote {
      border-left: 4px solid #dfe2e5;
      padding-left: 16px;
      margin-left: 0;
      color: #6a737d;
    }
    img {
      max-width: 100%;
    }
    ul, ol {
      padding-left: 20px;
    }
    p {
      margin-top: 0;
      margin-bottom: 16px;
    }
  `
  element.appendChild(style)

  const opt = {
    margin: [0.5, 0.5],
    filename: `${fileName}.pdf`,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: {
      scale: 2,
      useCORS: true,
      logging: false
    },
    jsPDF: {
      unit: 'in',
      format: 'a4',
      orientation: 'portrait'
    }
  }

  ElMessage.success('正在生成PDF，请稍候...')
  html2pdf().from(element).set(opt).save().then(() => {
    ElMessage.success('PDF导出成功')
  }).catch(err => {
    console.error('PDF导出失败:', err)
    ElMessage.error('PDF导出失败，请重试')
  })
}

// 通用文件保存函数
const saveFile = (blob, fileName) => {
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = fileName
  link.click()
  URL.revokeObjectURL(link.href)
}

const exportPDF = () => {
  if (!currentPatient.value || messages.value.length <= 1) {
    ElMessage.warning('没有可导出的对话内容')
    return
  }

  // 配置 marked 选项
  marked.setOptions({
    headerIds: true,
    mangle: false,
    headerPrefix: 'heading-',
    highlight: function(code, lang) {
      if (lang && hljs.getLanguage(lang)) {
        return hljs.highlight(code, { language: lang }).value
      }
      return hljs.highlightAuto(code).value
    },
    breaks: true,
    gfm: true
  })

  const currentDate = new Date().toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })

  const element = document.createElement('div')

  // 处理 Markdown 内容，确保标题正确渲染
  const processedMessages = messages.value.map(msg => {
    return {
      ...msg,
      // 修复标题语法：确保#后有空格，同时处理多级标题(#, ##, ###等)
      content: msg.content
          // 将没有空格的标题格式 (#标题) 替换为正确的格式 (# 标题)
          .replace(/^(#{1,6})([^\s])/gm, '$1 $2')
          // 确保标题前后有换行符以便正确渲染
          .replace(/^(#{1,6}\s.+)$/gm, '\n$1\n')
    }
  })

  element.innerHTML = `
    <div style="padding: 20px; font-family: SimSun, serif;">
      <h1 style="text-align: center; margin-bottom: 30px; font-size: 24px; color: #333;">患者病例报告</h1>

      <div style="margin-bottom: 30px; padding: 20px; background-color: #f8f9fa; border-radius: 8px; border: 1px solid #e6e6e6;">
        <table style="width: 100%; border-collapse: collapse;">
          <tr>
            <td style="padding: 8px; width: 25%;"><strong>患者姓名：</strong>${currentPatient.value.name}</td>
            <td style="padding: 8px; width: 25%;"><strong>年龄：</strong>${currentPatient.value.age}岁</td>
            <td style="padding: 8px; width: 25%;"><strong>性别：</strong>${currentPatient.value.male}</td>
            <td style="padding: 8px; width: 25%;"><strong>记录时间：</strong>${currentDate}</td>
          </tr>
          ${currentPatient.value.diagnosis ? `
          <tr>
            <td colspan="4" style="padding: 8px;"><strong>诊断：</strong>${currentPatient.value.diagnosis}</td>
          </tr>
          ` : ''}
        </table>
      </div>

      <div style="margin-top: 20px;">
        ${processedMessages.map((msg, index) => `
          <div style="margin-bottom: 20px; page-break-inside: avoid;">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
              <span style="font-weight: bold; color: ${msg.role === 'assistant' ? '#409EFF' : '#67C23A'}; padding: 4px 8px; background-color: ${msg.role === 'assistant' ? '#ecf5ff' : '#f0f9eb'}; border-radius: 4px;">
                ${msg.role === 'assistant' ? 'AI医生' : '医生'}
              </span>
              <span style="margin-left: 10px; color: #909399; font-size: 14px;">
                #${index + 1}
              </span>
            </div>
            <div style="padding: 15px; background-color: ${msg.role === 'assistant' ? '#f5f7fa' : '#f0f9eb'};
                        border-radius: 8px; border: 1px solid ${msg.role === 'assistant' ? '#e6e6e6' : '#e1f3d8'}; line-height: 1.6; font-size: 14px;">
                          ${marked.parse(msg.content)}
                        </div>
          </div>
        `).join('')}
      </div>

      <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #EBEEF5; text-align: center;">
        <p style="color: #909399; font-size: 12px;">本报告由AI医疗助手自动生成，仅供医学参考</p>
        <p style="color: #909399; font-size: 12px;">导出时间：${currentDate}</p>
      </div>
    </div>
  `

  // 添加样式以支持代码高亮和Markdown样式
  const style = document.createElement('style')
  style.textContent = `
    h1, h2, h3, h4, h5, h6 {
      margin-top: 24px;
      margin-bottom: 16px;
      font-weight: 600;
      line-height: 1.25;
    }
    h1 {
      font-size: 2em;
      border-bottom: 1px solid #eaecef;
      padding-bottom: 0.3em;
    }
    h2 {
      font-size: 1.5em;
      border-bottom: 1px solid #eaecef;
      padding-bottom: 0.3em;
    }
    h3 {
      font-size: 1.25em;
    }
    h4 {
      font-size: 1em;
    }
    h5 {
      font-size: 0.875em;
    }
    h6 {
      font-size: 0.85em;
      color: #6a737d;
    }
    pre {
      background-color: #f6f8fa;
      border-radius: 6px;
      padding: 16px;
      overflow: auto;
    }
    code {
      font-family: Consolas, Monaco, 'Andale Mono', monospace;
      font-size: 14px;
    }
    table {
      border-collapse: collapse;
      width: 100%;
      margin: 16px 0;
    }
    th, td {
      border: 1px solid #dfe2e5;
      padding: 8px 12px;
    }
    th {
      background-color: #f6f8fa;
    }
    blockquote {
      border-left: 4px solid #dfe2e5;
      padding-left: 16px;
      margin-left: 0;
      color: #6a737d;
    }
    img {
      max-width: 100%;
    }
    ul, ol {
      padding-left: 20px;
    }
    p {
      margin-top: 0;
      margin-bottom: 16px;
    }
  `
  element.appendChild(style)

  const opt = {
    margin: [0.5, 0.5],
    filename: `${currentPatient.value.name}_诊疗对话记录_${new Date().toISOString().split('T')[0]}.pdf`,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: {
      scale: 2,
      useCORS: true,
      logging: false
    },
    jsPDF: {
      unit: 'in',
      format: 'a4',
      orientation: 'portrait',
      putTotalPages: true
    }
  }

  ElMessage.success('正在生成PDF，请稍候...')
  html2pdf().from(element).set(opt).save().then(() => {
    ElMessage.success('PDF导出成功')
  }).catch(err => {
    console.error('PDF导出失败:', err)
    ElMessage.error('PDF导出失败，请重试')
  })
}

// Watchers
watch(messages, () => {
  scrollToBottom()
}, { deep: true })

// Lifecycle hooks
onMounted(() => {
  getPatients()
  scrollToBottom()
})
</script>

<style scoped>
.chat-page {
  height: 100vh;
  background: #f5f7fa;
  overflow: hidden;
}

/* Sidebar Styles */
.el-aside {
  background: white;
  border-right: 1px solid #e6e6e6;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.patient-select {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.back-button {
  padding: 12px 20px;
  border-bottom: 1px solid #e6e6e6;
}

.back-btn {
  font-size: 14px;
  transition: all 0.3s ease;
}

.back-btn:hover {
  transform: translateX(-5px);
  color: #409EFF;
}

.select-header {
  padding: 20px;
  border-bottom: 1px solid #e6e6e6;
}

.select-header h3 {
  margin: 0 0 15px 0;
  color: #2c3e50;
  font-size: 18px;
  position: relative;
  display: inline-block;
}

.select-header h3::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 40px;
  height: 3px;
  background: linear-gradient(90deg, #409EFF, #79bbff);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.select-header h3:hover::after {
  width: 100%;
}

.search-input {
  transition: all 0.3s ease;
}

.search-input:focus {
  transform: scale(1.02);
}

.patient-list {
  flex: 1;
  overflow-y: auto;
  scroll-behavior: smooth;
  padding: 10px 0;
}

.patient-item {
  padding: 15px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
  position: relative;
  overflow: hidden;
}

.patient-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, rgba(64, 158, 255, 0.1), transparent);
  transform: translateX(-100%);
  transition: transform 0.3s ease;
}

.patient-item:hover {
  background: #f5f7fa;
  transform: translateX(5px);
}

.patient-item:hover::before {
  transform: translateX(0);
}

.patient-item.active {
  background: #ecf5ff;
  border-left: 3px solid #409EFF;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.patient-avatar {
  transition: all 0.3s ease;
  border: 2px solid transparent;
  background: linear-gradient(135deg, #409EFF, #79bbff);
}

.patient-avatar.pulse {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(64, 158, 255, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(64, 158, 255, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(64, 158, 255, 0);
  }
}

.patient-info {
  flex: 1;
}

.patient-name {
  font-weight: 500;
  margin-bottom: 4px;
  transition: color 0.3s ease;
}

.patient-item:hover .patient-name {
  color: #409EFF;
}

.patient-detail {
  font-size: 12px;
  color: #909399;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 180px;
}

.no-patients {
  padding: 20px;
  text-align: center;
  color: #909399;
}

/* Header Styles */
.chat-header {
  height: 60px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  border-bottom: 1px solid #e6e6e6;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.patient-brief {
  display: flex;
  align-items: center;
  gap: 12px;
  animation: fadeIn 0.5s ease;
}

.patient-brief .name {
  font-weight: 500;
  color: #2c3e50;
}

.patient-brief .info {
  color: #606266;
}

.diagnosis-tag {
  transition: all 0.3s ease;
}

.diagnosis-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 5px;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
}

.icon {
  margin-right: 4px;
}

/* Chat Container Styles */
.chat-container {
  height: calc(100vh - 200px);
  overflow-y: auto;
  padding: 20px;
  scroll-behavior: smooth;
  background: linear-gradient(rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.85)),
  url('http://cloud.epilepsy-detect.xyz/%E8%83%8C%E6%99%AF.png') center/cover no-repeat fixed;
  position: relative;
}

.chat-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.4));
  backdrop-filter: blur(1px);
  z-index: -1;
  animation: backgroundPulse 15s ease-in-out infinite;
}

@keyframes backgroundPulse {
  0%, 100% {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7));
  }
  50% {
    background: linear-gradient(135deg, rgba(240, 248, 255, 0.85), rgba(240, 248, 255, 0.65));
  }
}

.chat-container::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
      radial-gradient(circle at 25% 25%, rgba(64, 158, 255, 0.05) 1%, transparent 5%),
      radial-gradient(circle at 75% 75%, rgba(64, 158, 255, 0.05) 1%, transparent 5%);
  background-size: 60px 60px;
  opacity: 0.5;
  z-index: -1;
  pointer-events: none;
}

/* Message Styles */
.message {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  animation: messageSlideIn 0.5s ease;
  position: relative;
}

.message.new-message {
  animation: newMessagePop 0.5s ease;
}

@keyframes newMessagePop {
  0% {
    opacity: 0;
    transform: scale(0.8) translateY(20px);
  }
  50% {
    opacity: 1;
    transform: scale(1.05) translateY(-5px);
  }
  100% {
    transform: scale(1) translateY(0);
  }
}

@keyframes messageSlideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.assistant {
  flex-direction: row;
}

.message.user {
  flex-direction: row-reverse;
}

.assistant-avatar {
  background: linear-gradient(135deg, #409EFF, #79bbff);
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.user-avatar {
  background: linear-gradient(135deg, #67C23A, #95d475);
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.message:hover .assistant-avatar {
  transform: scale(1.1) rotate(5deg);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
  border-color: #409EFF;
}

.message:hover .user-avatar {
  transform: scale(1.1) rotate(-5deg);
  box-shadow: 0 4px 12px rgba(103, 194, 58, 0.3);
  border-color: #67C23A;
}

.message-content {
  max-width: 80%;
  padding: 12px 16px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.message.assistant .message-content {
  border-top-left-radius: 0;
  background: white;
}

.message.user .message-content {
  background: #ecf5ff;
  border-top-right-radius: 0;
}

.message-content:hover {
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

/* Message Actions */
.message-actions {
  position: absolute;
  top: 8px;
  right: 8px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.message-content:hover .message-actions {
  opacity: 1;
}

.export-message-btn {
  padding: 4px;
  color: #909399;
  transition: all 0.3s ease;
}

.export-message-btn:hover {
  color: #409EFF;
  transform: scale(1.2);
}

/* Export Format Dialog */
.export-format-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.format-btn {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 10px;
  padding: 12px;
  transition: all 0.3s ease;
}

.format-btn:hover {
  background-color: #ecf5ff;
  transform: translateY(-2px);
}

/* Typing indicator */
.typing-indicator {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 10px 16px;
  background: white;
  border-radius: 18px;
  width: fit-content;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.typing-indicator .dot {
  width: 8px;
  height: 8px;
  background: #409EFF;
  border-radius: 50%;
  animation: typingBounce 1.5s infinite ease-in-out;
}

.typing-indicator .dot:nth-child(1) {
  animation-delay: 0s;
}

.typing-indicator .dot:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator .dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typingBounce {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-8px);
  }
}

/* Input Area Styles */
.chat-input {
  padding: 20px;
  background: white;
  border-top: 1px solid #e6e6e6;
  height: 100%;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.chat-input:focus-within {
  box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.1);
}

.message-textarea {
  transition: all 0.3s ease;
}

.message-textarea:focus {
  transform: translateY(-2px);
}

.input-actions {
  margin-top: 12px;
  padding-bottom: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tip {
  color: #909399;
  font-size: 12px;
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

.chat-input:focus-within .tip {
  opacity: 1;
}

.send-button {
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.send-button::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 5px;
  height: 5px;
  background: rgba(255, 255, 255, 0.7);
  opacity: 0;
  border-radius: 100%;
  transform: scale(1, 1) translate(-50%, -50%);
  transform-origin: 50% 50%;
}

.send-button:hover::after {
  animation: ripple-button 0.6s ease-out;
}

@keyframes ripple-button {
  0% {
    transform: scale(0, 0);
    opacity: 0.5;
  }
  20% {
    transform: scale(25, 25);
    opacity: 0.5;
  }
  100% {
    opacity: 0;
    transform: scale(40, 40);
  }
}

/* Virtual Assistant Styles */
.virtual-assistant {
  position: fixed;
  right: 30px;
  bottom: 30px;
  z-index: 1000;
  filter: drop-shadow(0 8px 20px rgba(0, 0, 0, 0.3));
  animation: floatAnimation 3s ease-in-out infinite;
  transition: transform 0.3s ease;
}

.virtual-assistant-gif {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid rgba(255, 255, 255, 0.9);
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(5px);
  cursor: pointer;
  transition: all 0.3s ease;
}

.virtual-assistant:hover {
  transform: scale(1.08);
}

.virtual-assistant-gif:hover {
  border-color: #409EFF;
  box-shadow: 0 0 20px rgba(64, 158, 255, 0.5);
}

.assistant-info {
  position: absolute;
  top: -80px;
  right: 0;
  background: white;
  padding: 10px 15px;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  width: 200px;
  animation: fadeInUp 0.3s ease;
}

.assistant-info::after {
  content: '';
  position: absolute;
  bottom: -8px;
  right: 30px;
  width: 16px;
  height: 16px;
  background: white;
  transform: rotate(45deg);
  box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.1);
}

.assistant-info-content {
  position: relative;
  z-index: 1;
}

.assistant-info h4 {
  margin: 0 0 5px 0;
  color: #409EFF;
}

.assistant-info p {
  margin: 0;
  font-size: 12px;
  color: #606266;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes floatAnimation {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-15px);
  }
}

/* Scrollbar Styles */
.patient-list::-webkit-scrollbar,
.chat-container::-webkit-scrollbar {
  width: 6px;
}

.patient-list::-webkit-scrollbar-thumb,
.chat-container::-webkit-scrollbar-thumb {
  background-color: #dcdfe6;
  border-radius: 3px;
}

.patient-list::-webkit-scrollbar-track,
.chat-container::-webkit-scrollbar-track {
  background-color: transparent;
}

/* Responsive Styles */
@media (max-width: 768px) {
  .el-aside {
    width: 100% !important;
    position: fixed;
    z-index: 10;
    height: 100vh;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }

  .el-aside.show {
    transform: translateX(0);
  }

  .virtual-assistant {
    right: 20px;
    bottom: 20px;
  }

  .virtual-assistant-gif {
    width: 120px;
    height: 120px;
  }
}
</style>