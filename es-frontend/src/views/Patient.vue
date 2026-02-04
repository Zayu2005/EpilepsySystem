<template>
  <!-- 添加统计图表卡片 -->
  <el-row :gutter="20" class="statistics-cards">
    <el-col :span="8">
      <el-card class="chart-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span><el-icon><PieChart /></el-icon> 性别分布</span>
          </div>
        </template>
        <div class="chart-container">
          <div ref="genderChartRef" style="height: 300px"></div>
        </div>
      </el-card>
    </el-col>
    <el-col :span="8">
      <el-card class="chart-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span><el-icon><Histogram /></el-icon> 年龄分布</span>
          </div>
        </template>
        <div class="chart-container">
          <div ref="ageChartRef" style="height: 300px"></div>
        </div>
      </el-card>
    </el-col>
    <el-col :span="8">
      <el-card class="chart-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span><el-icon><DataAnalysis /></el-icon> 科室分布</span>
          </div>
        </template>
        <div class="chart-container">
          <div ref="departmentChartRef" style="height: 300px"></div>
        </div>
      </el-card>
    </el-col>
  </el-row>

  <el-card>
    <div>
      <el-button type="primary" style="margin-left: 10px;width: 100px; " @click="addPatientButton">
        <el-icon style="margin-right: 5px;">
          <Plus/>
        </el-icon>
        新增患者
      </el-button>
      <el-input v-model="name" style="width: 200px;margin-left: 1100px;" placeholder="请输入患者姓名" clearable
                @clear="getPatientList" @keyup.enter="getPatientList"/>
      <el-button type="primary" style="margin-left: 10px;" @click="getPatientList">
        <el-icon style="margin-right: 5px;">
          <Search/>
        </el-icon>
        搜索
      </el-button>
      <!-- 添加隐私模式切换 -->
      <el-switch
        v-model="privacyMode"
        class="ml-2"
        style="margin-left: 20px;"
        inline-prompt
        active-text="隐私模式"
        inactive-text="正常模式"
        @change="togglePrivacyMode"
      />
    </div>
  </el-card>
  <el-card style="margin-top: 20px;">
    <el-table :data="displayData" style="width: 100%" border stripe>
      <el-table-column type="index" label="序号" width="100" :index="indexMethod"/>
      <!-- <el-table-column prop="id" label="序号" width="150" /> -->
      <el-table-column prop="name" label="姓名" width="150">
        <template #default="scope">
          {{ maskData(scope.row.name, 'name') }}
        </template>
      </el-table-column>
      <el-table-column prop="age" label="年龄" width="150">
        <template #default="scope">
          {{ maskData(scope.row.age, 'age') }}
        </template>
      </el-table-column>
      <el-table-column prop="male" label="性别" width="150"/>
      <el-table-column prop="phone" label="联系方式" width="150">
        <template #default="scope">
          {{ maskData(scope.row.phone, 'phone') }}
        </template>
      </el-table-column>
      <el-table-column prop="address" label="住址">
        <template #default="scope">
          {{ maskData(scope.row.address, 'address') }}
        </template>
      </el-table-column>
      <!-- <el-table-column prop="doctorId" label="主治医生"/>
      <el-table-column prop="departmentId" label="病房号"/> -->
      <el-table-column prop="createTime" label="入院时间"/>
      <el-table-column fixed="right" label="操作  " min-width="120">
        <template #default="{ row }">
          <el-button type="primary" size="default" style="margin-left: 10px;" @click="editButton(row)">
            <el-icon>
              <EditPen/>
            </el-icon>
            修改患者信息
          </el-button>
          <el-button type="danger" size="default" style="margin-left: 10px;" @click="deleteButton(row)">
            <el-icon>
              <Delete/>
            </el-icon>
            删除
          </el-button>
          <el-button type="success" size="default" style="margin-left: 10px;" @click="diagnosisButton(row)">
            <el-icon>
              <CopyDocument/>
            </el-icon>
            病情诊断
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination background layout="total, prev, pager, next, sizes, jumper" :total="total"
                   :page-sizes="pageSizes" :current-page="currentPage" :page-size="pageSize"
                   @current-change="handleCurrentChange"
                   @size-change="handleSizeChange">
    </el-pagination>
  </el-card>
  <!-- 修改患者信息 -->
  <el-dialog v-model="dialogFormVisible" title="修改患者信息" width="500">
    <el-form :model="editForm" label-width="120px">
      <el-form-item label="患者ID">
        <el-input v-model="editForm.id" disabled/>
      </el-form-item>
      <el-form-item label="姓名">
        <el-input v-model="editForm.name"/>
      </el-form-item>
      <el-form-item label="年龄">
        <el-input v-model="editForm.age"/>
      </el-form-item>
      <el-form-item label="性别">
        <el-radio-group v-model="editForm.male">
          <el-radio value="男">男</el-radio>
          <el-radio value="女">女</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="联系方式">
        <el-input v-model="editForm.phone"/>
      </el-form-item>
      <el-form-item label="住址">
        <el-input v-model="editForm.address"/>
      </el-form-item>
      <!-- <el-form-item label="主治医生">
        <el-input v-model="editForm.doctorId"/>
      </el-form-item> -->
      <!--
            <el-select
            v-model="value"
            placeholder="请选择主治医生"
            size="large"
          >
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select> -->
      <!-- <el-form-item label="病房号">
        <el-input v-model="editForm.departmentId"/>
      </el-form-item> -->
    </el-form>
    <template #footer>
            <span class="dialog-footer">
                <el-button @click="closeEditForm">取消</el-button>
                <el-button type="primary" @click="submitEditForm">确定</el-button>
            </span>
    </template>
  </el-dialog>
  <!-- 新增患者信息 -->
  <el-dialog v-model="addDialogFormVisible" title="新增患者信息" width="500">
    <el-form :model="addForm" label-width="120px">
      <el-form-item label="姓名">
        <el-input v-model="addForm.name"/>
      </el-form-item>
      <el-form-item label="年龄">
        <el-input v-model="addForm.age"/>
      </el-form-item>
      <el-form-item label="性别">
        <el-radio-group v-model="addForm.male">
          <el-radio value="男">男</el-radio>
          <el-radio value="女">女</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="联系方式">
        <el-input v-model="addForm.phone"/>
      </el-form-item>
      <el-form-item label="住址">
        <el-input v-model="addForm.address"/>
      </el-form-item>
      <!-- <el-form-item label="主治医生">
        <el-input v-model="addForm.doctorId"/>
      </el-form-item>
      <el-form-item label="病房号">
        <el-input v-model="addForm.departmentId"/>
      </el-form-item> -->
    </el-form>
    <template #footer>
            <span class="dialog-footer">
                <el-button @click="closeAddForm">取消</el-button>
                <el-button type="primary" @click="submitAddForm">确定</el-button>
            </span>
    </template>
  </el-dialog>
  <!--病情诊断窗口  -->
  <el-dialog v-model="diagnosisFormVisible" title="病情诊断" width="1000px">
    <el-form :model="diagnosisFrom" label-width="120px">
      <el-form-item label="患者ID">
        <el-input v-model="diagnosisFrom.id" disabled/>
      </el-form-item>
      <el-form-item label="患者姓名">
        <el-input v-model="diagnosisFrom.name" disabled/>
      </el-form-item>
      <el-form-item label="病情诊断">
        <el-input v-model="diagnosisFrom.diagnosis" />
      </el-form-item>
      <el-form-item label="详细病情">
        <!-- 替换文本框为富文本编辑器 -->
        <div class="quill-editor">
          <QuillEditor
            v-model:content="diagnosisFrom.text"
            contentType="html"
            theme="snow"
            :toolbar="[
              ['bold', 'italic', 'underline'],
              [{ 'list': 'ordered' }, { 'list': 'bullet' }],
              [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
              [{ 'color': [] }, { 'background': [] }],
              ['image', 'link'],
              ['clean']
            ]"
          />
        </div>
      </el-form-item>
    </el-form>
    <template #footer>
            <span class="dialog-footer">
                <el-button @click="closeDiagnosisForm">取消</el-button>
                <el-button type="primary" @click="submitDiagnosisFrom">确定</el-button>
            </span>
    </template>
  </el-dialog>
  <Loading :visible="isLoading" :text="LoadingText"/>
</template>


<script setup>
import {onMounted, ref, watch, onUnmounted, computed} from 'vue';
import * as echarts from 'echarts';
import Loading from '@/components/Loading.vue'
import {
  patientListService,
  deletePatientService,
  updatePatientService,
  addPatientService,
  patientListAllService, addDiagnosisService
} from '@/api/patient'
import {ElMessageBox, ElMessage} from 'element-plus'
// 导入富文本编辑器
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

const userListInfo = ref([
  {}
])
const LoadingText = ref('')
const isLoading = ref(false)
const pageSizes = [5, 10, 20, 50]
const currentPage = ref(1)
const pageNum = ref(1)
const pageSize = ref(10)
const total = ref(0)
//修改患者信息
const dialogFormVisible = ref(false)
const addDialogFormVisible = ref(false)
const diagnosisFormVisible = ref(false)
const name = ref('')
const editForm = ref({})
const addForm = ref({})
const diagnosisFrom = ref({})

// 添加隐私模式状态
const privacyMode = ref(true)
const userRole = ref('doctor') // 可以根据实际登录用户角色设置

// 根据隐私模式处理显示数据
const displayData = computed(() => {
  return patientData.value
})

// 切换隐私模式
const togglePrivacyMode = () => {
  ElMessage({
    type: 'info',
    message: privacyMode.value ? '已开启隐私模式，敏感信息将被隐藏' : '已关闭隐私模式，显示完整信息',
  })
}

// 数据脱敏函数
const maskData = (value, type) => {
  if (!value || !privacyMode.value) return value
  
  // 根据不同类型的数据进行不同的脱敏处理
  switch (type) {
    case 'name':
      // 姓名保留首字，其余用*代替
      if (value.length <= 1) return value
      return value.substring(0, 1) + '*'.repeat(value.length - 1)
    
    case 'phone':
      // 手机号码保留前三位和后四位，中间用*代替
      if (value.length <= 7) return '*'.repeat(value.length)
      return value.substring(0, 3) + '****' + value.substring(value.length - 4)
    
    case 'address':
      // 地址保留前六个字符，其余用*代替
      if (value.length <= 6) return value
      return value.substring(0, 6) + '****'
    
    case 'age':
      // 年龄显示为年龄段
      const age = parseInt(value)
      if (isNaN(age)) return value
      
      if (age < 18) return '未成年'
      else if (age < 30) return '18-30岁'
      else if (age < 45) return '30-45岁'
      else if (age < 60) return '45-60岁'
      else return '60岁以上'
      
    default:
      return value
  }
}

// 检查用户权限
const checkPermission = (requiredRole) => {
  // 这里可以根据实际的权限系统进行判断
  // 简单示例：医生可以查看所有信息，护士只能查看部分信息
  return userRole.value === requiredRole || userRole.value === 'admin'
}

const startLoading = () => {
  console.log('开始加载')
  isLoading.value = true
  LoadingText.value = '正在加载数据，请稍等...'
  setTimeout(() => {
    isLoading.value = false
    ElMessage.success('加载成功...')
  }, 1500)
}
//提交病情诊断窗口
// const submitDiagnosisForm
//关闭病情诊断窗口
const stopLoading = () => {
  isLoading.value = false
}
const closeDiagnosisForm = () => {
  diagnosisFormVisible.value = false
  diagnosisFrom.value = ref({})
}
const submitDiagnosisFrom = async () => {
  let result = await addDiagnosisService(diagnosisFrom.value)
  if (result.code == 0) {
    ElMessage({
      type: 'success',
      message: '新增成功',
    })
    closeDiagnosisForm()
  } else {
    ElMessage({
          type: 'error',
          message: '新增失败',
        }
    )
    closeDiagnosisForm()
  }
}
//新增患者信息
const addPatientButton = () => {
  addDialogFormVisible.value = true
  diagnosisFrom.value = ref({})
}
const submitAddForm = async () => {
  let result = await addPatientService(addForm.value)
  if (result.code == 0) {
    ElMessage({
      type: 'success',
      message: '新增成功',

    })
    addDialogFormVisible.value = false
    getPatientList()
  } else {
    ElMessage({
          type: 'error',
          message: '新增失败',
        }
    )
  }

}
//修改患者信息表单数据

const handleCurrentChange = (page) => {
  currentPage.value = page
  pageNum.value = page
  getPatientList()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  pageNum.value = 1
  currentPage.value = 1
  getPatientList()
}

const indexMethod = (index) => {
  return (currentPage.value - 1) * pageSize.value + index + 1
}

// 图表引用
const genderChartRef = ref(null)
const ageChartRef = ref(null)
const departmentChartRef = ref(null)

// 图表实例
let genderChart = null
let ageChart = null
let departmentChart = null

// 初始化图表
const initCharts = () => {
  // 性别分布图表
  genderChart = echarts.init(genderChartRef.value)
  // 年龄分布图表
  ageChart = echarts.init(ageChartRef.value)
  // 科室分布图表
  departmentChart = echarts.init(departmentChartRef.value)
}

// 更新图表数据
const updateCharts = (data) => {
  // 处理性别分布数据
  const genderData = data.reduce((acc, curr) => {
    acc[curr.male] = (acc[curr.male] || 0) + 1
    return acc
  }, {})

  // 处理年龄分布数据
  const ageGroups = {
    '0-18': 0,
    '19-30': 0,
    '31-45': 0,
    '46-60': 0,
    '60+': 0
  }
  data.forEach(patient => {
    const age = parseInt(patient.age)
    if (age <= 18) ageGroups['0-18']++
    else if (age <= 30) ageGroups['19-30']++
    else if (age <= 45) ageGroups['31-45']++
    else if (age <= 60) ageGroups['46-60']++
    else ageGroups['60+']++
  })

  // 处理科室分布数据
  const departmentData = data.reduce((acc, curr) => {
    acc[curr.departmentId] = (acc[curr.departmentId] || 0) + 1
    return acc
  }, {})

  // 设置性别分布图表
  genderChart.setOption({
    title: {
      text: '患者性别分布',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'normal',
        color: '#2c3e50'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}人 ({d}%)',
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      borderColor: '#eee',
      borderWidth: 1,
      textStyle: {
        color: '#333'
      },
      extraCssText: 'box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      top: 'center',
      itemGap: 12,
      textStyle: {
        fontSize: 12
      }
    },
    color: ['#4fc3f7', '#ff8a65', '#9575cd', '#4db6ac', '#f06292'],
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['60%', '50%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 8,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 14,
            fontWeight: 'bold'
          },
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        labelLine: {
          show: false
        },
        data: Object.entries(genderData).map(([name, value]) => ({
          name,
          value
        }))
      }
    ],
    animation: true,
    animationDuration: 1000,
    animationEasing: 'cubicOut'
  })

  // 设置年龄分布图表
  ageChart.setOption({
    title: {
      text: '患者年龄分布',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'normal',
        color: '#2c3e50'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      borderColor: '#eee',
      borderWidth: 1,
      textStyle: {
        color: '#333'
      },
      formatter: '{b}: {c}人',
      extraCssText: 'box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: Object.keys(ageGroups),
      axisLine: {
        lineStyle: {
          color: '#ddd'
        }
      },
      axisLabel: {
        color: '#666',
        fontSize: 12
      }
    },
    yAxis: {
      type: 'value',
      name: '人数',
      nameTextStyle: {
        color: '#666',
        fontSize: 12
      },
      axisLine: {
        show: false
      },
      axisTick: {
        show: false
      },
      splitLine: {
        lineStyle: {
          color: '#eee'
        }
      }
    },
    series: [
      {
        data: Object.values(ageGroups),
        type: 'bar',
        barWidth: '50%',
        showBackground: true,
        backgroundStyle: {
          color: 'rgba(220, 220, 220, 0.2)'
        },
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#83bff6' },
            { offset: 0.5, color: '#64a5f6' },
            { offset: 1, color: '#2196f3' }
          ]),
          borderRadius: [4, 4, 0, 0]
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#5e9cf7' },
              { offset: 0.7, color: '#3f87f5' },
              { offset: 1, color: '#1565c0' }
            ])
          }
        },
        animationDelay: function (idx) {
          return idx * 100;
        }
      }
    ],
    animationEasing: 'elasticOut',
    animationDelayUpdate: function (idx) {
      return idx * 5;
    }
  })

  // 设置科室分布图表
  departmentChart.setOption({
    title: {
      text: '患者科室分布',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'normal',
        color: '#2c3e50'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}人 ({d}%)',
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      borderColor: '#eee',
      borderWidth: 1,
      textStyle: {
        color: '#333'
      },
      extraCssText: 'box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);'
    },
    legend: {
      type: 'scroll',
      orient: 'horizontal',
      bottom: 0,
      data: Object.keys(departmentData),
      textStyle: {
        fontSize: 12
      }
    },
    color: ['#26c6da', '#29b6f6', '#66bb6a', '#ffa726', '#ef5350', '#ab47bc', '#ec407a', '#7e57c2'],
    series: [
      {
        type: 'pie',
        radius: '55%',
        center: ['50%', '45%'],
        roseType: 'radius',
        itemStyle: {
          borderRadius: 5,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          formatter: '{b}: {c}人'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 14,
            fontWeight: 'bold'
          },
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        data: Object.entries(departmentData).map(([name, value]) => ({
          name: name || '未分配',
          value
        }))
      }
    ],
    animationDuration: 1500,
    animationEasing: 'cubicInOut'
  })
}

// 监听窗口大小变化
const handleResize = () => {
  genderChart?.resize()
  ageChart?.resize()
  departmentChart?.resize()
}

// 修改获取患者列表函数
const getPatientList = async () => {
  try {
    let params = {
      pageNum: pageNum.value,
      pageSize: pageSize.value,
      name: name.value || null
    }
    const result = await patientListService(params)
    if (result.code === 0) {
      patientData.value = result.data.items
      total.value = result.data.total
    } else {
      ElMessage.error('获取数据失败')
    }
  } catch (error) {
    console.error('获取患者列表失败:', error)
    ElMessage.error('获取数据失败')
  }
}

//病情诊断
const diagnosisButton = async (row) => {
  diagnosisFormVisible.value = true
  diagnosisFrom.value = row
}
//删除患者
const deleteButton = async (row) => {
  let name = row.name
  let id = row.id
  ElMessageBox.confirm(
      `是否确定删除患者 ${privacyMode.value ? maskData(name, 'name') : name} 吗`,
      '提醒',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
  )
      .then(async () => {
        let result = await deletePatientService(id)
        if (result.code == 0) {
          ElMessage({
            type: 'success',
            message: '删除成功',
          })
          getPatientList()
        } else {
          ElMessage({
            type: 'error',
            message: '删除失败',
          })
        }
      })
      .catch(() => {
        ElMessage({
          type: 'info',
          message: '取消删除',
        })
      })

}

// 修改患者信息
const editButton = (row) => {
  dialogFormVisible.value = true
  // 在编辑时始终使用原始数据，不使用脱敏数据
  editForm.value = {...row}
}
const closeEditForm = () => {
  ElMessageBox.confirm(
      '确认取消修改患者信息吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '返回',
        type: 'warning'
      }
  )
      .then(() => {
        dialogFormVisible.value = false
        editForm.value = {} // 清空表单
        getPatientList()
        ElMessage({
          type: 'info',
          message: '已取消修改'
        })
      })
      .catch(() => {
        // 用户点击返回，保持弹窗打开状态
      })
}
const closeAddForm = () => {
  ElMessageBox.confirm(
      '确认取消新增患者吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '返回',
        type: 'warning'
      }
  )
      .then(() => {
        addDialogFormVisible.value = false
        addForm.value = {} // 清空表单
        ElMessage({
          type: 'info',
          message: '已取消新增'
        })
      })
      .catch(() => {
        // 用户点击返回，保持弹窗打开状态
      })
}
const submitEditForm = async () => {
  let result = await updatePatientService(editForm.value)
  if (result.code == 0) {
    ElMessage({
      type: 'success',
      message: '修改成功',
    })
    dialogFormVisible.value = false
    getPatientList()
  } else {
    ElMessage({
      type: 'error',
      message: '修改失败',
    })
    getPatientList()
  }
}
//获得所有病人信息
const getAllPatient = async () => {
  try {
    let result = await patientListService({
      pageNum: 1,
      pageSize: 1000
    })
    if (result.code === 0) {
      patientAllData.value = result.data.items
      // 更新图表
      updateCharts(result.data.items)
    } else {
      ElMessage.error('获取数据失败')
    }
  } catch (error) {
    console.error('获取患者列表失败:', error)
    ElMessage.error('获取数据失败')
  }
}
onMounted(() => {
  initCharts()
  getPatientList()
  getAllPatient()
  startLoading()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

const patientData = ref([]);
const patientAllData = ref([
  {}
])

</script>

<style scoped>
.statistics-cards {
  margin-bottom: 20px;
}

/* 统一所有卡片样式 */
.chart-card,
.el-card {
  height: 100%;
  transition: all 0.3s ease;
  border: none;
  margin-bottom: 15px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.chart-card:hover,
.el-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1) !important;
}

.chart-container {
  width: 100%;
  height: 300px;
  padding: 10px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: 500;
  color: #2c3e50;
}

.card-header .el-icon {
  margin-right: 6px;
  font-size: 18px;
  vertical-align: middle;
}

/* 添加表格卡片内部的过渡动画 */
.el-table {
  transition: all 0.3s ease;
}

/* 添加分页组件的过渡动画 */
.el-pagination {
  margin-top: 15px;
  transition: all 0.3s ease;
}

/* 添加按钮的过渡动画 */
.el-button {
  transition: all 0.3s ease;
}

.el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.15);
}

/* 添加表单项的过渡动画 */
.el-form-item {
  transition: all 0.3s ease;
}

/* 添加对话框的过渡动画 */
.el-dialog {
  border-radius: 8px;
  overflow: hidden;
}

/* 添加富文本编辑器样式 */
.quill-editor {
  height: 400px;
  margin-bottom: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.quill-editor :deep(.ql-container) {
  border-bottom-left-radius: 4px;
  border-bottom-right-radius: 4px;
  background: #fff;
  font-size: 14px;
}

.quill-editor :deep(.ql-toolbar) {
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
  border-bottom: 1px solid #dcdfe6;
  background: #f5f7fa;
}

.quill-editor :deep(.ql-editor) {
  min-height: 300px;
  max-height: 500px;
  overflow-y: auto;
  line-height: 1.6;
  padding: 12px 15px;
}
/* 汉化工具栏按钮 */
::v-deep .ql-snow .ql-picker.ql-header .ql-picker-label::before,
::v-deep .ql-snow .ql-picker.ql-header .ql-picker-item::before {
  content: '文本';
}

::v-deep .ql-snow .ql-picker.ql-header .ql-picker-label[data-value="1"]::before,
::v-deep .ql-snow .ql-picker.ql-header .ql-picker-item[data-value="1"]::before {
  content: '标题1';
}

::v-deep .ql-snow .ql-picker.ql-header .ql-picker-label[data-value="2"]::before,
::v-deep .ql-snow .ql-picker.ql-header .ql-picker-item[data-value="2"]::before {
  content: '标题2';
}

::v-deep .ql-snow .ql-picker.ql-header .ql-picker-label[data-value="3"]::before,
::v-deep .ql-snow .ql-picker.ql-header .ql-picker-item[data-value="3"]::before {
  content: '标题3';
}

::v-deep .ql-snow .ql-picker.ql-header .ql-picker-label[data-value="4"]::before,
::v-deep .ql-snow .ql-picker.ql-header .ql-picker-item[data-value="4"]::before {
  content: '标题4';
}

::v-deep .ql-snow .ql-picker.ql-header .ql-picker-label[data-value="5"]::before,
::v-deep .ql-snow .ql-picker.ql-header .ql-picker-item[data-value="5"]::before {
  content: '标题5';
}

::v-deep .ql-snow .ql-picker.ql-header .ql-picker-label[data-value="6"]::before,
::v-deep .ql-snow .ql-picker.ql-header .ql-picker-item[data-value="6"]::before {
  content: '标题6';
}

::v-deep .ql-snow .ql-picker.ql-list .ql-picker-label::before,
::v-deep .ql-snow .ql-picker.ql-list .ql-picker-item::before {
  content: '列表';
}

::v-deep .ql-snow .ql-picker.ql-list .ql-picker-label[data-value="ordered"]::before,
::v-deep .ql-snow .ql-picker.ql-list .ql-picker-item[data-value="ordered"]::before {
  content: '有序列表';
}

::v-deep .ql-snow .ql-picker.ql-list .ql-picker-label[data-value="bullet"]::before,
::v-deep .ql-snow .ql-picker.ql-list .ql-picker-item[data-value="bullet"]::before {
  content: '无序列表';
}
</style>