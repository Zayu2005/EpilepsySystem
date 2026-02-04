<template>
  <div class="home-container">
    <!-- 顶部统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :md="6" v-for="(item, index) in statsCards" :key="item.label">
        <el-card shadow="hover" class="stats-card" :body-style="{ padding: '20px' }" 
                :style="{ animationDelay: index * 0.1 + 's' }">
          <div class="stats-item">
            <div class="stats-icon" :style="{ background: item.color }">
              <el-icon>
                <component :is="item.icon" />
              </el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-value">{{ stats[item.key] }}</div>
              <div class="stats-label">{{ item.label }}</div>
              <div class="stats-trend" v-if="item.trend">
                <span :class="['trend-value', item.trend > 0 ? 'up' : 'down']">
                  {{ Math.abs(item.trend) }}%
                  <el-icon>
                    <component :is="item.trend > 0 ? 'ArrowUp' : 'ArrowDown'" />
                  </el-icon>
                </span>
                <span class="trend-label">较上周</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 主要内容区域 -->
    <el-row :gutter="20" class="main-content">
      <!-- 左侧：实时监控 -->
      <el-col :span="16">
        <el-card class="monitor-card animate-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <span class="title">实时脑电波监测</span>
                <el-tag type="success" effect="dark" class="status-tag">
                  <el-icon>
                    <Loading />
                  </el-icon>
                  实时监测中
                </el-tag>
              </div>
              <div class="header-right">
                <el-radio-group v-model="monitorType" size="small">
                  <el-radio-button label="all" >全部病房</el-radio-button>
                  <el-radio-button label="warning">异常监测</el-radio-button>
                </el-radio-group>
                <el-button type="primary" plain size="small" @click="refreshMonitorData">
                  <el-icon>
                    <Refresh />
                  </el-icon>
                  刷新
                </el-button>
              </div>
            </div>
          </template>
          <div class="monitor-list" v-loading="monitorLoading">
            <el-table :data="monitorData" style="width: 100%;" :row-class-name="tableRowClassName" :row-style="{height:'100px'}">
              <el-table-column prop="roomNo" label="病房号" width="100" />
              <el-table-column prop="patientName" label="患者姓名" width="120" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="getStatusType(scope.row.status)" class="status-tag-animated">
                    {{ scope.row.status }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="lastUpdate" label="最后更新" width="180" />
              <el-table-column prop="eegValue" label="脑电波值" width="120">
                <template #default="scope">
                  <span :class="getEegValueClass(scope.row.eegValue)">
                    {{ scope.row.eegValue }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200">
                <template #default="scope">
                  <el-button link type="primary" @click="viewDetails(scope.row)" class="action-button">
                    查看详情
                  </el-button>
                  <el-button link type="warning" @click="handleAlert(scope.row)" v-if="scope.row.status !== '正常'" class="action-button">
                    处理预警
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧：待办事项和通知 -->
      <el-col :span="8">
        <!-- 右侧：待办事项和通知 -->
        <el-card class="todo-card animate-card" :style="{ animationDelay: '0.2s' }">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <span class="title">待办事项</span>
                <el-badge :value="todoList.length" class="todo-badge" type="danger" />
              </div>
              <div class="header-right">
                <el-select v-model="todoFilter" placeholder="筛选状态" size="small" class="filter-select">
                  <el-option label="全部" value="all" />
                  <el-option label="已完成" value="completed" />
                  <el-option label="未完成" value="uncompleted" />
                </el-select>
                <el-button type="primary" link @click="todoDialogVisible = true" class="add-button">
                  <el-icon>
                    <Plus />
                  </el-icon>
                  添加待办
                </el-button>
              </div>
            </div>
          </template>
          <div class="timeline-wrapper">
            <el-timeline>
              <el-timeline-item v-for="item in filteredTodoList" :key="item.id" :type="item.type" :timestamp="item.time"
                :color="getTimelineColor(item)" class="timeline-item-animated">
                <div class="todo-item">
                  <div class="todo-content">
                    <el-checkbox v-model="item.completed" @change="() => handleTodoComplete(item)" />
                    <span :class="{ 'todo-completed': item.completed }">
                      <div class="todo-title">{{ item.title }}</div>
                      <div class="todo-desc">{{ item.content }}</div>
                    </span>
                  </div>
                  <div class="todo-actions">
                    <el-button link type="danger" @click="deleteTodo(item)" class="delete-button">删除</el-button>
                  </div>
                </div>
              </el-timeline-item>
            </el-timeline>
          </div>

          <!-- 添加分页组件 -->
          <div class="pagination-container">
            <el-pagination v-model:current-page="pageNum" v-model:page-size="pageSize" :page-sizes="[5, 10, 20]"
              :small="true" layout="total, sizes, prev, pager, next" :total="todoList.length"
              @size-change="handleSizeChange" @current-change="handleCurrentChange" />
          </div>
        </el-card>

        <el-card class="notice-card animate-card" :style="{ animationDelay: '0.3s' }">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <span class="title">系统通知</span>
                <div class="pulse-dot" v-if="notices.length > 0"></div>
              </div>
              <div class="header-right">
                <el-tooltip placement="top" content="发布通知" v-if="userInfo.username === 'admin'">
                  <el-button class="add-notice-button" circle @click="notificationDialog = true">
                    <el-icon>
                      <Plus />
                    </el-icon>
                  </el-button>
                </el-tooltip>
                <el-button text @click="viewAllNotices" class="view-all-button">查看全部</el-button>
              </div>
            </div>
          </template>
          <div class="notice-list">
            <el-scrollbar height="300px">
              <div v-for="notice in notices" :key="notice.id" class="notice-item" @click="readNotice(notice)">
                <div class="notice-content">
                  <div class="notice-header">
                    <div class="notice-title">{{ notice.title }}</div>
                    <div class="notice-time">{{ notice.createTime }}</div>
                  </div>
                  <div class="notice-desc">{{ notice.content }}</div>
                </div>
                <el-badge is-dot :hidden="notice.read" class="notice-badge" />
              </div>
            </el-scrollbar>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 添加待办对话框 -->
    <el-dialog v-model="todoDialogVisible" title="添加待办事项" width="500px" class="custom-dialog">
      <el-form :model="newTodo" :rules="todoRules" ref="todoFormRef" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="newTodo.title" placeholder="请输入待办事项标题" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input v-model="newTodo.content" type="textarea" rows="3" placeholder="请输入待办事项详细内容" />
        </el-form-item>
        <el-form-item label="截止时间" prop="time">
          <el-date-picker v-model="newTodo.time" type="datetime" placeholder="选择截止时间" format="YYYY-MM-DD HH:mm"
            value-format="YYYY-MM-DD HH:mm" />
        </el-form-item>
        <el-form-item label="优先级" prop="type">
          <el-select v-model="newTodo.type" placeholder="选择优先级">
            <el-option label="低" value="低" />
            <el-option label="中" value="中" />
            <el-option label="高" value="高" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="todoDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitTodo">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 添加通知的弹出框 -->
     <el-dialog v-model="notificationDialog" title="发布通知" width="500px" class="custom-dialog">
      <el-form :model="newNotification" :rules="notificationRules" ref="notificationFormRef" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="newNotification.title" placeholder="请输入通知标题" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input v-model="newNotification.content" type="textarea" rows="3" placeholder="请输入通知内容" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="notificationDialog = false">取消</el-button>
          <el-button type="primary" @click="submitNotification()">确定</el-button>
        </span>
      </template>
     </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import {
  User, Bell, Warning, FirstAidKit, Loading, Refresh, Plus, ArrowUp, ArrowDown
} from '@element-plus/icons-vue'

import { getTodoListService, addTodoService, deleteTodoService, updateTodoStatusService } from '@/api/todo.js'
import { addNotificationService, getNotificationsService } from '@/api/notification.js'
import { userInfoService } from '@/api/user.js'
import { getMonitorData, getHomeStats } from '@/api/monitor.js'

import { ElMessage, ElMessageBox } from 'element-plus'

const notificationDialog = ref(false) // 通知的弹出框
const newNotification = ref({
  title: '',
  content: '',
})

// 通知规则
const notificationRules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入通知内容', trigger: 'blur' }],
}

const notices = ref([])
const userInfo = ref({
  id: '',
  username: '',
  name: '',
  email: '',
  createTime: '',
  updateTime: '',
})

userInfoService().then(res => {
  userInfo.value = res.data
})

// 统计卡片配置
const statsCards = [
  {
    key: 'patientCount',
    label: '累计患者',
    icon: 'User',
    color: 'linear-gradient(135deg, #4158D0, #C850C0)',
    trend: 5
  },
  {
    key: 'todayAppointments',
    label: '今日预约',
    icon: 'Bell',
    color: 'linear-gradient(135deg, #42E695, #3BB2B8)',
    trend: -2
  },
  {
    key: 'emergencyCount',
    label: '异常预警',
    icon: 'Lightning',
    color: 'linear-gradient(135deg, #FF6B6B, #FFE66D)',
    trend: -5
  },
  {
    key: 'emergencyCount',
    label: '急诊患者',
    icon: 'FirstAidKit',
    color: 'linear-gradient(135deg, #FF416C, #FF4B2B)',
    trend: -3
  }
]

// 数据状态
const pageNum = ref()
const pageSize = ref()
const stats = ref({})
const monitorData = ref([])
const todoList = ref([])

const monitorType = ref('all')
const monitorLoading = ref(false)
const todoDialogVisible = ref(false)
const refreshInterval = ref(null)

// 新待办表单
const newTodo = ref({
  title: '',
  content: '',
  time: '',
  type: '',
  completed: 0
})

// 待办表单校验规则
const todoRules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入待办内容', trigger: 'blur' }],
  time: [{ required: true, message: '请选择时间', trigger: 'change' }],
  type: [{ required: true, message: '请选择优先级', trigger: 'change' }]
}

// 初始化数据
const initData = async () => {
  try {
    // 获取统计数据
    const statsRes = await getHomeStats()
    stats.value = statsRes.data

    // 获取监控数据
    await refreshMonitorData()
  } catch (error) {
    console.error('初始化数据失败:', error)
  }
}

//获得待办事项
const getTodoList = async () => {
  try {
    let params = {
      pageNum: pageNum.value || 1,
      pageSize: pageSize.value || 5
    }
    const result = await getTodoListService(params)
    todoList.value = result.data.items
  } catch (error) {
    console.error('获取待办事项失败:', error)
  }
}

// 刷新监控数据
const refreshMonitorData = async () => {
  monitorLoading.value = true
  try {
    const res = await getMonitorData({ type: monitorType.value })
    monitorData.value = res.data
  } catch (error) {
    console.error('获取监控数据失败:', error)
  } finally {
    monitorLoading.value = false
  }
}

// 表格行样式
const tableRowClassName = ({ row }) => {
  if (row.status === '异常') return 'warning-row'
  return ''
}

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    '正常': 'success',
    '警告': 'warning',
    '异常': 'danger'
  }
  return types[status] || 'info'
}

// 获取脑电波值样式
const getEegValueClass = (value) => {
  const numValue = parseFloat(value)
  if (numValue > 80) return 'eeg-danger'
  if (numValue > 60) return 'eeg-warning'
  return 'eeg-normal'
}

// 添加待办事项
const submitTodo = async () => {
  try {
    await addTodoService(newTodo.value)
    ElMessage.success('添加成功')
    todoDialogVisible.value = false
    // 重置表单
    newTodo.value = {
      title: '',
      content: '',
      time: '',
      type: '',
      completed: 0
    }
    // 刷新待办列表
    getTodoList()
  } catch (error) {
    ElMessage.error('添加失败')
  }
}

// 处理分页大小改变
const handleSizeChange = (val) => {
  pageSize.value = val
  getTodoList()
}

// 处理页码改变
const handleCurrentChange = (val) => {
  pageNum.value = val
  getTodoList()
}

// 查看全部通知
const viewAllNotices = () => {
  // 实现查看全部通知的逻辑
  ElMessage.info('查看全部通知功能待实现')
}

// 阅读通知
const readNotice = (notice) => {
  // 实现阅读通知的逻辑
  notice.read = true
  ElMessage.success('已标记为已读')
}

// 查看详情
const viewDetails = (row) => {
  // 实现查看详情的逻辑
  ElMessage.info(`查看患者 ${row.patientName} 的详情`)
}

// 处理预警
const handleAlert = (row) => {
  // 实现处理预警的逻辑
  ElMessage.success(`已处理 ${row.patientName} 的预警`)
}

onMounted(() => {
  getTodoList()
  initData()
  // 设置定时刷新监控数据
  getNotifications()
  refreshInterval.value = setInterval(refreshMonitorData, 30000)
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
})

// 添加待办筛选状态
const todoFilter = ref('all')

// 筛选待办列表
const filteredTodoList = computed(() => {
  if (todoFilter.value === 'all') return todoList.value
  return todoList.value.filter(item =>
    todoFilter.value === 'completed' ? item.completed : !item.completed
  )
})

// 获取时间线颜色
const getTimelineColor = (todo) => {
  if (todo.completed) return '#67C23A'
  const priorityColors = {
    '高': '#F56C6C',
    '中': '#E6A23C',
    '低': '#409EFF'
  }
  return priorityColors[todo.type] || '#409EFF'
}

// 处理待办完成状态
const handleTodoComplete = async (todo) => {
  try {
    await ElMessageBox.confirm('确认更改该待办事项的状态', '提示', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'info'
    })

    const params = { id: todo.id }
    const result = await updateTodoStatusService(params)

    if (result.code === 0) {
      ElMessage.success('更改成功')
      // 更新本地待办事项状态
      todo.completed = !todo.completed
      // 重新获取待办列表
      await getTodoList()
    } else {
      ElMessage.warning('更改失败')
      // 恢复checkbox状态
      todo.completed = !todo.completed
    }
  } catch (error) {
    console.error('更改失败:', error)
    ElMessage.error('更改失败')
    // 恢复checkbox状态
    todo.completed = !todo.completed
  }
}

// 删除待办
const deleteTodo = (todo) => {
  ElMessageBox.confirm('确认删除该待办事项吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    todoList.value = todoList.value.filter(item => item.id !== todo.id)
    deleteTodoService(todo.id)
    ElMessage.success('删除成功')
  }).catch(() => {
  })
}

//获得所有通知
const getNotifications = async() => {
  try {
    const res = await getNotificationsService()
    notices.value = res.data
  } catch (error) {
    console.error('获取通知失败:', error)
  }
}

// 新建通知
const submitNotification = async () => {
  try {
    await ElMessageBox.confirm('确认发布该通知吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await addNotificationService(newNotification.value)
    ElMessage.success('发布成功')
    notificationDialog.value = false
    // 重置表单
    newNotification.value = {
      title: '',
      content: ''
    }
    // 刷新通知列表
    await getNotifications()
  } catch (error) {
    ElMessage.error('发布失败')
  }
}
</script>

<style scoped>
.home-container {
  padding: 20px;
  overflow-x: hidden;
  background-color: #f5f7fa;
  min-height: 100vh;
}

/* 统计卡片样式优化 */
.stats-card {
  margin-bottom: 20px;
  animation: slideInUp 0.5s ease forwards;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.3s ease;
  overflow: hidden;
  border-radius: 12px;
  border: none;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.stats-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
}

.stats-card:hover .stats-icon {
  transform: scale(1.1) rotate(5deg);
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-card {
  animation: fadeIn 0.6s ease forwards;
  opacity: 0;
  border-radius: 12px;
  border: none;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.stats-row {
  margin-bottom: 20px;
}

.stats-item {
  display: flex;
  align-items: center;
  gap: 15px;
}

.stats-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.stats-icon::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
}

.stats-icon::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: rgba(255, 255, 255, 0.2);
  transform: rotate(45deg);
  animation: shimmer 3s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%) rotate(45deg);
  }
  100% {
    transform: translateX(100%) rotate(45deg);
  }
}

.stats-icon .el-icon {
  font-size: 28px;
  z-index: 1;
  filter: drop-shadow(0 2px 5px rgba(0, 0, 0, 0.3));
}

.stats-info {
  flex: 1;
}

.stats-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  animation: countUp 1.5s ease-out forwards;
  background: linear-gradient(45deg, #333, #666);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

@keyframes countUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.stats-label {
  font-size: 14px;
  color: #606266;
  margin-top: 6px;
  position: relative;
  display: inline-block;
  font-weight: 500;
}

.stats-label::after {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #409EFF, transparent);
  transition: width 0.5s ease;
}

.stats-card:hover .stats-label::after {
  width: 100%;
}

.trend-value {
  display: flex;
  align-items: center;
  font-size: 13px;
  font-weight: 600;
  margin-top: 8px;
}

.trend-value.up {
  color: #67C23A;
}

.trend-value.down {
  color: #F56C6C;
}

.trend-value .el-icon {
  margin-left: 4px;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-5px);
  }
  60% {
    transform: translateY(-2px);
  }
}

.trend-label {
  font-size: 12px;
  color: #909399;
  margin-left: 5px;
}

/* 卡片头部样式优化 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  position: relative;
  padding-left: 12px;
}

.title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 18px;
  background: linear-gradient(to bottom, #409EFF, #53a8ff);
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.5);
}

.monitor-card, .todo-card, .notice-card {
  margin-bottom: 20px;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  overflow: hidden;
}

.monitor-card:hover, .todo-card:hover, .notice-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
}

.status-tag {
  display: flex;
  align-items: center;
  gap: 5px;
  height: 24px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.status-tag {
  display: flex;
  align-items: center;
  gap: 5px;
  height: 24px;
  border-radius: 12px;
  padding: 0 10px;
  font-weight: 500;
}

.status-tag-animated {
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.status-tag-animated::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: shine 2s infinite;
}

@keyframes shine {
  100% {
    left: 100%;
  }
}

.status-tag .el-icon {
  animation: rotate 2s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.monitor-list {
  margin-top: 10px;
}

/* 表格行动画增强 */
.el-table .el-table__row {
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.el-table .el-table__row::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #409EFF, transparent);
  transition: width 0.5s ease;
}

.el-table .el-table__row:hover {
  background-color: #f0f9ff !important;
  transform: translateY(-2px) scale(1.01);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  z-index: 1;
}

.el-table .el-table__row:hover::after {
  width: 100%;
}

.el-table .warning-row {
  background-color: rgba(253, 246, 236, 0.8);
  position: relative;
  overflow: hidden;
  animation: pulse 3s infinite;
}

.el-table .warning-row::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: repeating-linear-gradient(
    45deg,
    rgba(230, 162, 60, 0.05),
    rgba(230, 162, 60, 0.05) 10px,
    rgba(230, 162, 60, 0.08) 10px,
    rgba(230, 162, 60, 0.08) 20px
  );
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(230, 162, 60, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(230, 162, 60, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(230, 162, 60, 0);
  }
}

/* 待办事项样式增强 */
.timeline-wrapper {
  position: relative;
  overflow: hidden;
}

.timeline-wrapper::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at top right, rgba(64, 158, 255, 0.05), transparent 70%);
  pointer-events: none;
}

.timeline-item-animated {
  transform: translateX(0);
  opacity: 1;
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.timeline-item-animated:hover {
  transform: translateX(8px);
}

.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 12px;
  border-radius: 10px;
  transition: all 0.3s ease;
  background-color: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(235, 238, 245, 0.8);
}

.todo-item:hover {
  background-color: rgba(255, 255, 255, 0.9);
  transform: translateX(5px) scale(1.02);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.05);
}

.todo-content {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.todo-title {
  font-weight: bold;
  margin-bottom: 5px;
  transition: all 0.3s ease;
  color: #303133;
}

.todo-item:hover .todo-title {
  color: #409EFF;
}

.todo-desc {
  color: #606266;
  font-size: 13px;
  transition: all 0.3s ease;
  line-height: 1.5;
}

.todo-completed {
  color: #909399;
  text-decoration: line-through;
}

.todo-actions {
  opacity: 0;
  transform: translateX(10px);
  transition: all 0.3s ease;
}

.todo-item:hover .todo-actions {
  opacity: 1;
  transform: translateX(0);
}

.delete-button {
  transition: all 0.3s ease;
  position: relative;
}

.delete-button:hover {
  color: #f56c6c;
  transform: scale(1.1);
}

/* 通知项增强 */
.notice-item {
  padding: 15px;
  border-bottom: 1px solid rgba(235, 238, 245, 0.7);
  cursor: pointer;
  transition: all 0.4s ease;
  margin-bottom: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  position: relative;
  overflow: hidden;
  border-radius: 8px;
}

.notice-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 0;
  background: linear-gradient(to bottom, #409EFF, #53a8ff);
  transition: height 0.3s ease;
}

.notice-item:hover {
  background-color: rgba(245, 247, 250, 0.8);
  transform: translateX(5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.notice-item:hover::before {
  height: 100%;
}

.notice-badge {
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.notice-item:hover .notice-badge {
  transform: scale(1.2) rotate(10deg);
}

.notice-content {
  width: 100%;
}

.notice-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.notice-title {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
  flex: 1;
  margin-right: 12px;
  transition: all 0.3s ease;
  position: relative;
  padding-bottom: 5px;
}

.notice-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background: linear-gradient(90deg, #409EFF, transparent);
  transition: width 0.3s ease;
}

.notice-item:hover .notice-title {
  color: #409EFF;
}

.notice-item:hover .notice-title::after {
  width: 100%;
}

.notice-time {
  font-size: 12px;
  color: #909399;
  white-space: nowrap;
}

.notice-desc {
  font-size: 13px;
  color: #606266;
  line-height: 1.6;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #F56C6C;
  position: relative;
}

.pulse-dot::before {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background-color: rgba(245, 108, 108, 0.6);
  animation: pulse-animation 2s infinite;
}

@keyframes pulse-animation {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(3);
    opacity: 0;
  }
}

/* 操作按钮增强 */
.action-button {
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  padding: 3px 0;
}

.action-button::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background-color: currentColor;
  transition: width 0.3s ease;
}

.action-button:hover {
  transform: translateY(-2px);
}

.action-button:hover::after {
  width: 100%;
}

/* 添加按钮增强 */
.add-button, .view-all-button {
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.add-button:hover, .view-all-button:hover {
  transform: translateY(-2px);
  text-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.add-notice-button {
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #409EFF, #53a8ff);
  color: white;
  border: none;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.add-notice-button:hover {
  transform: rotate(90deg) scale(1.1);
  background: linear-gradient(135deg, #53a8ff, #409EFF);
  box-shadow: 0 8px 20px rgba(64, 158, 255, 0.4);
}

.filter-select {
  transition: all 0.3s ease;
}

.filter-select:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

/* 对话框增强 */
.custom-dialog {
  border-radius: 12px;
  overflow: hidden;
}

.custom-dialog :deep(.el-dialog__header) {
  background: linear-gradient(135deg, #f5f7fa, #e4e7ed);
  padding: 15px 20px;
}

.custom-dialog :deep(.el-dialog__title) {
  font-weight: 600;
  color: #303133;
}

.custom-dialog :deep(.el-dialog__body) {
  padding: 30px 20px;
}

.custom-dialog :deep(.el-dialog__footer) {
  padding: 15px 20px;
  border-top: 1px solid #f0f2f5;
}

/* 分页组件美化 */
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  transition: all 0.3s ease;
  padding: 10px;
  background-color: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(5px);
  border-radius: 8px;
}

.pagination-container:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

/* 脑电波值样式增强 */
.eeg-normal {
  color: #67C23A;
  font-weight: 600;
  display: inline-block;
  position: relative;
}

.eeg-normal::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #67C23A;
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.eeg-normal:hover::after {
  transform: scaleX(1);
}

.eeg-warning {
  color: #E6A23C;
  font-weight: 600;
  display: inline-block;
  position: relative;
}

.eeg-warning::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #E6A23C;
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.eeg-warning:hover::after {
  transform: scaleX(1);
}

.eeg-danger {
  color: #F56C6C;
  font-weight: 600;
  display: inline-block;
  position: relative;
  animation: blink 1.5s infinite;
}

@keyframes blink {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.eeg-danger::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #F56C6C;
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.eeg-danger:hover::after {
  transform: scaleX(1);
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .main-content>.el-col {
    width: 100%;
  }

  .stats-row .el-col {
    margin-bottom: 20px;
  }
}

@media (max-width: 768px) {
  .home-container {
    padding: 15px;
  }
  
  .title {
    font-size: 16px;
  }
  
  .stats-value {
    font-size: 24px;
  }
  
  .stats-icon {
    width: 48px;
    height: 48px;
  }
  
  .stats-icon .el-icon {
    font-size: 24px;
  }
}
</style>

