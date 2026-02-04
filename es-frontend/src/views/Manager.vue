<template>
  <div class="common-layout">
    <el-container>
      <!-- 头部导航 -->
      <el-header class="main-header">
        <div class="header-left">
          <div class="logo">
            <img src="http://cloud.epilepsy-detect.xyz/logo-no-max.png" alt="logo" class="logo-img" />
            <span class="logo-text"> 脑域衡安——智慧癫痫医疗平台</span>
          </div>
        </div>

        <el-menu

          class="el-menu-demo"
          mode="horizontal"
          :default-active="$route.path"
          @select="handleSelect"
        >
          <el-menu-item index="1" @click="(()=> {router.push('/home') })">
            <el-icon><House /></el-icon>
            首页
          </el-menu-item>
          <el-menu-item index="2" @click="(()=> {router.push('/patient')})">
            <el-icon><User   /></el-icon>
            患者管理
          </el-menu-item>
          <el-sub-menu index="3">
      <template #title>
        <el-icon><DataLine /></el-icon>脑电检测</template>
      <el-menu-item index="3-1" @click="router.push('/eeg')">
        <el-icon><CreditCard /></el-icon>
          癫痫检测</el-menu-item>
      <el-menu-item index="3-2" @click="router.push('/analysis')">
        <el-icon><Monitor /></el-icon>
        可视化分析</el-menu-item>
    </el-sub-menu>
          <el-menu-item index="4" @click="router.push('/ward')">
            <el-icon><TrendCharts /></el-icon>
            病房监测
          </el-menu-item>
          <el-menu-item index="5" @click="router.push('/chat')">
            <el-icon><ChatRound /></el-icon>
            AI辅助
          </el-menu-item>
          <el-menu-item index="6" @click="router.push('/virtual-assistant')">
            <el-icon><Service /></el-icon>
            智能助手
          </el-menu-item>
          <el-menu-item index="7" @click="router.push('data')">
            <el-icon><Histogram /></el-icon>
            数据统计
          </el-menu-item>
        </el-menu>

        <div class="header-right">
          <el-dropdown>
            <span class="user-profile">
            你好，
              <el-avatar :size="32" class="user-avatar">
                <el-icon><User /></el-icon>
              </el-avatar>
              <span class="username">{{ userInfo.name }}</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="router.push('/account')">
                  <el-icon><Setting /></el-icon>账号管理
                </el-dropdown-item>
                <el-dropdown-item divided @click="logout">
                  <el-icon><SwitchButton /></el-icon>退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 主要内容区 -->
      <el-main class="main-content">
        <RouterView></RouterView>
      </el-main>

    </el-container>    
    <!-- 添加 Loading 组件 -->
    <Loading :visible="isLoading" :text="loadingText" />
  </div>
</template>

<script lang="ts" setup>
import {ref} from 'vue'
import router from '@/router';
import {Setting, House, Edit, Cpu, TrendCharts, User, SwitchButton} from "@element-plus/icons-vue";
import { useTokenStore } from '@/stores/token';
import { userInfoService } from '@/api/user';
import { ElMessage } from 'element-plus';
import Loading from '@/components/Loading.vue'


const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
const isLoading = ref(false)
const loadingText = ref('正在退出登录，保存数据中...')



// 停止加载
const stopLoading = () => {
  isLoading.value = false
}
// 获取用户信息
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

const logout = () => {
  // 显示加载中
  isLoading.value = true
  loadingText.value = '正在退出登录，请稍候...'
  
  // 清除token
  useTokenStore().removeToken()
  //开启加载动画
  setTimeout(() => {
    // 隐藏加载
    isLoading.value = false
    // 显示成功消息
    ElMessage.success('退出成功')
    // 跳转到登录页
    router.push('/login')
  }, 3000)
}
</script>

<style scoped>
.common-layout {
  min-height: 100vh;
  background: #f5f7fa;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.el-container {
  margin: 0;
  padding: 0;
}

.main-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 60px;
  background: linear-gradient(to right, #f0f8ff, #e6f2ff, #f0f8ff);
  box-shadow: 0 2px 15px rgba(33, 150, 243, 0.1);
  position: relative;
  z-index: 2;
  border-bottom: 1px solid rgba(33, 150, 243, 0.1);
  margin: 0;
}



.header-left {
  display: flex;
  align-items: center;
}


.logo {
  display: flex;
  align-items: center;
  margin-right: 40px;
}

.logo-img {
  height: 42px;
  margin-right: 12px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
  transition: all 0.5s ease;
  animation: logoFloat 3s ease-in-out infinite;
}

.logo-img:hover {
  transform: scale(1.05) rotate(2deg);
  filter: drop-shadow(0 4px 8px rgba(33, 150, 243, 0.3));
}

.logo-text {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  background: linear-gradient(120deg, #2196f3, #1976d2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
  transition: all 0.3s ease;
}

.logo-text:hover {
  letter-spacing: 0.5px;
  transform: translateY(-1px);
}

@keyframes logoFloat {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-3px);
  }
}

.el-menu-demo {
  border: none;
  flex: 1;
  justify-content: center;
  background: transparent;
}

.el-menu-demo :deep(.el-menu-item) {
  background: transparent;
}

.el-menu-demo :deep(.el-menu-item),
.el-menu-demo :deep(.el-sub-menu__title) {
  font-size: 14px;
  height: 60px;
  line-height: 60px;
  padding: 0 20px;
  background: transparent;
  transition: all 0.3s;
}

.el-menu-demo :deep(.el-menu-item:hover),
.el-menu-demo :deep(.el-sub-menu__title:hover) {
  background: rgba(33, 150, 243, 0.08);
}

.el-menu-demo :deep(.el-menu-item.is-active) {
  color: #2196f3;
  border-bottom-color: #2196f3;
  font-weight: 500;
  background: rgba(33, 150, 243, 0.12);
}

.header-right {
  display: flex;
  align-items: center;
}

.user-profile {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 0 12px;
  height: 40px;
  border-radius: 20px;
  transition: all 0.3s;
}

.user-profile:hover {
  background: #f5f7fa;
}

.user-avatar {
  background: #2196f3;
  color: white;
}

.username {
  margin-left: 8px;
  font-size: 14px;
  color: #606266;
}

.main-content {
  padding: 20px;
  background: #f5f7fa;
  min-height: calc(100vh - 60px);
}

/* 添加响应式布局 */
@media (max-width: 768px) {
  .logo-text {
    display: none;
  }
  
  .el-menu-demo :deep(.el-menu-item),
  .el-menu-demo :deep(.el-sub-menu__title) {
    padding: 0 12px;
  }
  

  .username {
    display: none;
  }
}
</style>
