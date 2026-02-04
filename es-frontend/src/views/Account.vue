<template>
  <div class="account-container">
    <div class="header-actions">
      <el-button @click="handleReturn" icon="ArrowLeft">返回</el-button>
      <h2 class="page-title">用户管理</h2>
    </div>

    <!-- 顶部操作栏 -->
    <el-card class="action-bar">
      <div class="action-group">
        <el-button type="primary" @click="showAddUserDialog">
          <el-icon><Plus /></el-icon>
          添加用户
        </el-button>
        <div class="search-group">
          <el-input
            v-model="searchQuery"
            placeholder="搜索用户名/姓名"
            clearable
            @clear="handleSearch"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <el-select v-model="statusFilter" placeholder="状态筛选" clearable>
            <el-option label="启用" :value="1" />
            <el-option label="禁用" :value="0" />
          </el-select>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </div>
      </div>
    </el-card>

    <!-- 用户列表 -->
    <el-card class="user-list">
      <el-table 
        v-loading="loading" 
        :data="userList" 
        style="width: 100%" 
        border
      >
        <el-table-column type="index" label="序号" width="80" />
        <el-table-column prop="username" label="用户名" width="120" />
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="phone" label="手机号" width="120" />
        <el-table-column prop="email" label="邮箱" width="180" />
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column prop="userStatus" label="状态" width="100">
          <template #default="scope">
            <el-switch
              v-model="scope.row.userStatus"
              :active-value="1"
              :inactive-value="0"
              @change="handleStatusChange(scope.row)"
            />
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="200">
          <template #default="scope">
            <el-button link type="primary" @click="handleEdit(scope.row)">
              编辑
            </el-button>
            <el-button link type="primary" @click="handleResetPassword(scope.row)">
              重置密码
            </el-button>
            <el-button link type="danger" @click="handleDelete(scope.row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 添加/编辑用户对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '添加用户' : '编辑用户'"
      width="500px"
    >
      <el-form
        ref="userFormRef"
        :model="userForm"
        :rules="userRules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" :disabled="dialogType === 'edit'" />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="userForm.name" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="userForm.phone" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="dialogType === 'add'">
          <el-input v-model="userForm.password" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 重置密码对话框 -->
    <el-dialog
      v-model="resetPasswordVisible"
      title="重置密码"
      width="400px"
    >
      <el-form
        ref="resetPasswordFormRef"
        :model="resetPasswordForm"
        :rules="resetPasswordRules"
        label-width="100px"
      >
        <el-form-item label="新密码" prop="newPassword">
          <el-input v-model="resetPasswordForm.newPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="resetPasswordForm.confirmPassword" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="resetPasswordVisible = false">取消</el-button>
          <el-button type="primary" @click="handleResetPasswordSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, ArrowLeft } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { userListService , userStatusChangeService , addUserService , updateUserService , userInfoService } from '@/api/user'
import { onMounted } from 'vue'

onMounted(async () => {
  const res = await userInfoService()
  if(res.data.username !== 'admin'){
    ElMessage.warning('非管理员，无法访问')
    router.push('/home')
  }
  await handleSearch()
})
const router = useRouter()

// 搜索和筛选
const searchQuery = ref('')
const statusFilter = ref('')

// 分页
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 用户列表数据
const userList = ref([
  {
    username: 'zhangsan',
    name: '张三',
    phone: '13800138000',
    email: 'zhangsan@example.com',
    createTime: '2024-01-20 10:00:00',
    userStatus: 1
  }
])

// 对话框控制
const dialogVisible = ref(false)
const dialogType = ref('add')
const resetPasswordVisible = ref(false)

// 表单数据
const userForm = reactive({
  username: '',
  name: '',
  phone: '',
  email: '',
  password: ''
})

// 重置密码表单
const resetPasswordForm = reactive({
  userId: '',
  newPassword: '',
  confirmPassword: ''
})

// 表单验证规则
const userRules = {
  username: [
    { required: true,message: '请输入用户名', trigger: 'blur' },
    { min: 4, max: 20, message: '长度在 4 到 20 个字符', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
  ]
}

// 重置密码验证规则
const resetPasswordRules = {
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== resetPasswordForm.newPassword) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 显示添加用户对话框
const showAddUserDialog = () => {
  dialogType.value = 'add'
  Object.keys(userForm).forEach(key => userForm[key] = '')
  dialogVisible.value = true
}

// 处理编辑用户
const handleEdit = (row) => {
  dialogType.value = 'edit'
  Object.assign(userForm, row)
  dialogVisible.value = true
}

// 处理重置密码
const handleResetPassword = (row) => {
  resetPasswordForm.userId = row.id
  resetPasswordForm.newPassword = ''
  resetPasswordForm.confirmPassword = ''
  resetPasswordVisible.value = true
}

// 处理删除用户
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除用户 ${row.name} 吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // 调用删除API
    ElMessage.success('删除成功')
  }).catch(() => {
    ElMessage.info('已取消删除')
  })
}

// 处理状态变更
const handleStatusChange = async (row) => {
  try {
    const action = row.userStatus === 1 ? '启用' : '禁用'
    const params = {
      id: row.id,
      userStatus: row.userStatus
    }
    const res = await userStatusChangeService(params)
    if (res.code === 0) {
      ElMessage.success(`已${action}用户 ${row.name}`)
      await handleSearch()
    } else {
      ElMessage.error(res.message || '操作失败')
      // 状态修改失败，恢复原来的状态
      row.userStatus = row.userStatus === 1 ? 0 : 1
    }
  } catch (error) {
    console.error('状态修改失败:', error)
    ElMessage.error(error.message)
    // 发生错误时，恢复原来的状态
    row.userStatus = row.userStatus === 1 ? 0 : 1
  }
}

// 处理表单提交
const handleSubmit = async () => {
  // 表单验证和提交逻辑
  if(dialogType.value === 'add'){
    const res = await addUserService(userForm)
    if(res.code === 0){
      ElMessage.success('添加成功')
      dialogVisible.value = false
      await handleSearch()
    }else{
      ElMessage.error(res.message || '添加失败')
    }
  }else{
    const res = await updateUserService(userForm)
    if(res.code === 0){
      ElMessage.success('修改成功')
      dialogVisible.value = false
      await handleSearch().then(() => {
        ElMessage.success('修改成功')
      })
      .catch((error) => {
        ElMessage.error(error.message || '修改失败')
      })
    }else{
      ElMessage.error(res.message || '修改失败')
    }
  }
}

// 处理重置密码提交
const handleResetPasswordSubmit = () => {
  // 重置密码逻辑
  ElMessage.success('密码重置成功')
  resetPasswordVisible.value = false
}

// 处理搜索
const loading = ref(false)

const handleSearch = async () => {
  loading.value = true
  try {
    currentPage.value = 1 // 重置页码
    // 实现搜索逻辑
    const searchParams = {
      query: searchQuery.value,
      status: statusFilter.value,
      pageNum : currentPage.value,
      pageSize: pageSize.value
    }
    console.log('搜索参数：', searchParams)
    const res = await userListService(searchParams)
    if(res.code === 0){
      userList.value = res.data.items
      total.value = res.data.total
    }else{
      ElMessage.error('搜索失败')
    }
  } finally {
    loading.value = false
  }
}

// 处理分页
const handleSizeChange = (val) => {
  pageSize.value = val
  handleSearch() // 重新获取数据
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  handleSearch() // 重新获取数据
}

// 返回首页
const handleReturn = () => {
  router.push('/home')
}
</script>

<style scoped>
.account-container {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 48px);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.page-title {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.action-bar {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.action-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-group {
  display: flex;
  gap: 10px;
  align-items: center;
}

.user-list {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

@media screen and (max-width: 768px) {
  .action-group {
    flex-direction: column;
    gap: 16px;
  }

  .search-group {
    flex-wrap: wrap;
  }
}
</style>
