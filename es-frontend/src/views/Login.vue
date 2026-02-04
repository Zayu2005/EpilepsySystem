<script setup>
import {reactive, ref, onMounted} from "vue";
import {userLoginService} from "@/api/user.js";
import router from "@/router/index.js";
import { ElMessage } from 'element-plus';
import { useTokenStore } from '@/stores/token.js';
import Loading from '@/components/Loading.vue'; // 引入Loading组件

const loginData = ref({
  username: '',
  password: '',
})

const ruleFormRef = ref()
const isLoading = ref(false) // 添加加载状态控制变量

//定义表单校验规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 5, max: 16, message: '长度为5~16位非空字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 5, max: 16, message: '长度为5~16位非空字符', trigger: 'blur' }
  ],
}

// 登录函数
const login = async() =>{
  await ruleFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        isLoading.value = true; // 显示加载动画
        let result = await userLoginService(loginData.value);
        const tokenStore = useTokenStore();
        if(result.code === 0){
          tokenStore.setToken(result.data)
          
          // 延迟跳转，保持加载动画显示约3秒
          setTimeout(() => {
            isLoading.value = false; // 隐藏加载动画
            ElMessage.success(result.msg || '登录成功')
            router.push("/")
          }, 3000);
        } else {
          ElMessage.error(result.msg || '登录失败')
          isLoading.value = false; // 登录失败时立即隐藏加载动画
        }
      } catch (error) {
        ElMessage.error(error.message || '登录失败')
        isLoading.value = false; // 发生错误时立即隐藏加载动画
      }
    }
  })
}

// 添加鼠标跟随效果
const handleMouseMove = (e) => {
  const container = e.currentTarget;
  const rect = container.getBoundingClientRect();
  const x = ((e.clientX - rect.left) / rect.width) * 100;
  const y = ((e.clientY - rect.top) / rect.height) * 100;
  container.style.setProperty('--mouse-x', `${x}%`);
  container.style.setProperty('--mouse-y', `${y}%`);
};

// 添加登录动画
const loginAnimation = ref(false)

// 添加粒子效果
const particles = ref(Array(20).fill().map(() => ({
  x: Math.random() * 100,
  y: Math.random() * 100,
  size: Math.random() * 3 + 1,
  speed: Math.random() * 1 + 0.5
})))

// 更新粒子位置
const updateParticles = () => {
  particles.value = particles.value.map(p => ({
    ...p,
    y: (p.y + p.speed) % 100
  }))
  requestAnimationFrame(updateParticles)
}

onMounted(() => {
  updateParticles()
})
</script>

<template>
  <div class="login-container" @mousemove="handleMouseMove">
    <!-- 背景元素 -->
    <div class="background-wrapper">
      <div class="gradient-bg"></div>
      <div class="particles-container">
        <div 
          v-for="(particle, index) in particles" 
          :key="index" 
          class="particle"
          :style="{
            left: `${particle.x}%`,
            top: `${particle.y}%`,
            width: `${particle.size}px`,
            height: `${particle.size}px`
          }"
        ></div>
      </div>
      <div class="medical-bg"></div>
      <div class="medical-cross"></div>
      <div class="brain-wave"></div>
      <div class="neuron-network"></div>
      <div class="dna-helix"></div>
      <div class="pulse-circles"></div>
    </div>
    
    <!-- 添加Loading组件 -->
    <Loading :visible="isLoading" text="登录中..." />
    
    <el-card class="login-card">
      <div class="card-glow"></div>
      
      <div class="login-header">
        <div class="logo-container">
          <img src="@/assets/logo-no-max.png"
            alt="Medical Logo"
            class="medical-logo"
          />
          <h1 class="main-title">脑域衡安</h1>
          <div class="subtitle-wrapper">
            <h3 class="sub-title">基于多模态和AI大模型分析的癫痫病发监测分析系统</h3>
          </div>
        </div>
      </div>

      <el-form
          ref="ruleFormRef"
          :model="loginData"
          status-icon
          :rules="rules"
          label-width="auto"
          class="login-form">
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="loginData.username" 
            placeholder="请输入用户名"
            prefix-icon="User"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="密  码" prop="password">
          <el-input 
            v-model="loginData.password" 
            placeholder="请输入密码" 
            type="password"
            prefix-icon="Lock"
            show-password
          ></el-input>
        </el-form-item>

        <el-form-item class="login-actions">
          <el-button 
            type="primary" 
            class="login-button" 
            auto-insert-space 
            @click="login"
            :loading="isLoading"
            @keyup.enter="login"
          >登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
  --mouse-x: 50%;
  --mouse-y: 50%;
}

/* 背景包装器 */
.background-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

/* 渐变背景 */
.gradient-bg {
  position: absolute;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f7ff 50%, #e3f2fd 100%);
  z-index: -10;
}

/* 粒子容器 */
.particles-container {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: -9;
}

/* 粒子样式 */
.particle {
  position: absolute;
  background-color: rgba(33, 150, 243, 0.3);
  border-radius: 50%;
  filter: blur(1px);
  box-shadow: 0 0 6px rgba(33, 150, 243, 0.5);
}

/* 脉冲圆圈 */
.pulse-circles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -8;
}

.pulse-circles::before,
.pulse-circles::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  height: 300px;
  border-radius: 50%;
  border: 2px solid rgba(33, 150, 243, 0.1);
  animation: pulse 8s ease-out infinite;
}

.pulse-circles::after {
  width: 500px;
  height: 500px;
  animation-delay: 2s;
}

/* 医疗背景 */
.medical-bg {
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(
    circle at var(--mouse-x) var(--mouse-y),
    rgba(33, 150, 243, 0.05) 0%,
    transparent 70%
  );
  z-index: -7;
  transition: background 0.3s ease;
}

/* 更新心电图波形 */
.medical-bg::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100%;
  background-image: 
    linear-gradient(90deg, transparent 49.5%, rgba(33, 150, 243, 0.4) 49.5%, rgba(33, 150, 243, 0.4) 50.5%, transparent 50.5%),
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 40' width='100' height='40'%3E%3Cpath d='M0,20 L20,20 L25,20 L30,10 L35,30 L40,10 L45,30 L50,20 L55,20 L100,20' stroke='%232196f3' fill='none' stroke-width='1.5'/%3E%3C/svg%3E");
  background-size: 200px 100%, 200px 100px;
  background-position: 0 0;
  background-repeat: repeat;
  opacity: 0.08;
  filter: drop-shadow(0 0 3px rgba(33, 150, 243, 0.5));
  animation: heartbeat 6s linear infinite;
  z-index: -6;
}

/* 调整多层心电图 */
.medical-bg::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100%;
  background: repeating-linear-gradient(
    0deg,
    transparent 0px,
    transparent 100px,
    rgba(33, 150, 243, 0.03) 100px,
    rgba(33, 150, 243, 0.03) 200px
  );
  opacity: 0.2;
  animation: verticalMove 30s linear infinite;
  z-index: -5;
}

/* 医疗十字装饰 */
.medical-cross {
  position: absolute;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at center, transparent 30%, rgba(33, 150, 243, 0.02) 70%),
    repeating-conic-gradient(
      from 0deg,
      transparent 0deg 80deg,
      rgba(33, 150, 243, 0.03) 80deg 100deg,
      transparent 100deg 360deg
    );
  animation: rotate 45s linear infinite;
  opacity: 0.05;
  z-index: -4;
}

/* 登录卡片样式 */
.login-card {
  width: 460px;
  padding: 2.5rem;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  box-shadow: 
    0 15px 50px rgba(0, 105, 192, 0.1),
    0 0 0 1px rgba(255, 255, 255, 0.8) inset,
    0 0 120px rgba(33, 150, 243, 0.05);
  position: relative;
  z-index: 1;
  border: none;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.login-card:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 20px 60px rgba(0, 105, 192, 0.15),
    0 0 0 1px rgba(255, 255, 255, 0.9) inset,
    0 0 120px rgba(33, 150, 243, 0.08);
}

/* 卡片光效 */
.card-glow {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    circle at var(--mouse-x) var(--mouse-y), 
    rgba(255, 255, 255, 0.8) 0%,
    transparent 60%
  );
  opacity: 0;
  transition: opacity 0.3s;
  z-index: -1;
}

.login-card:hover .card-glow {
  opacity: 0.8;
}

.login-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.logo-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.medical-logo {
  width: 150px;
  height: auto;
  filter: drop-shadow(0 4px 16px rgba(18, 150, 219, 0.3));
  transition: all 0.4s ease;
  margin: 0 0 0.5rem;
  animation: logoPulse 3s ease-in-out infinite;
}

.medical-logo:hover {
  transform: scale(1.05);
  filter: drop-shadow(0 8px 20px rgba(18, 150, 219, 0.5));
}

.main-title {
  font-size: 2.2rem;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #1976d2, #2196f3, #64b5f6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 1px;
}

.subtitle-wrapper {
  position: relative;
  margin-top: 0.5rem;
}

.sub-title {
  font-size: 0.95rem;
  font-weight: 500;
  color: #64b5f6;
  margin: 0;
  opacity: 0.9;
  position: relative;
}

.sub-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(33, 150, 243, 0.5), transparent);
}

/* 表单样式 */
.login-form {
  max-width: 100%;
  margin-top: 2rem;
}

.login-form :deep(.el-form-item__label) {
  font-weight: 500;
  color: #1976d2;
}

.login-form :deep(.el-input) {
  --el-input-hover-border-color: #2196f3;
  --el-input-focus-border-color: #2196f3;
}

.login-form :deep(.el-input__wrapper) {
  box-shadow: 0 0 0 1px rgba(33, 150, 243, 0.2);
  border-radius: 12px;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(5px);
  padding: 0 12px;
}

.login-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px rgba(33, 150, 243, 0.5);
  background: rgba(255, 255, 255, 0.9);
}

.login-form :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.3);
  background: rgba(255, 255, 255, 1);
}

.login-form :deep(.el-input__inner) {
  height: 42px;
}

.login-form :deep(.el-input__prefix-inner) {
  color: #2196f3;
}

.login-actions {
  margin-top: 2.5rem;
}

.login-button {
  width: 100%;
  height: 44px;
  background: linear-gradient(135deg, #2196f3, #1976d2);
  border: none;
  font-size: 1.05rem;
  font-weight: 500;
  letter-spacing: 1px;
  border-radius: 12px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.login-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg, 
    transparent, 
    rgba(255, 255, 255, 0.2), 
    transparent
  );
  transition: left 0.7s ease;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(33, 150, 243, 0.2);
}

.login-button:hover::before {
  left: 100%;
}

.login-button:active {
  transform: translateY(1px);
  box-shadow: 0 4px 8px rgba(33, 150, 243, 0.1);
}

/* 添加脑电波效果 */
.brain-wave {
  position: absolute;
  top: 10%;
  right: 5%;
  width: 300px;
  height: 150px;
  opacity: 0.08;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 20'%3E%3Cpath d='M0,10 C10,10 15,0 20,10 C25,20 30,0 35,10 C40,20 45,0 50,10 C55,20 60,0 65,10 C70,20 75,0 80,10 C85,20 90,10 100,10' stroke='%232196f3' fill='none' stroke-width='1'/%3E%3C/svg%3E");
  background-repeat: repeat-x;
  animation: brainwave 10s linear infinite;
  filter: drop-shadow(0 0 3px rgba(33, 150, 243, 0.3));
  z-index: -3;
}

/* 添加神经元连接效果 */
.neuron-network {
  position: absolute;
  left: 5%;
  bottom: 10%;
  width: 200px;
  height: 200px;
  opacity: 0.06;
  background-image: 
    radial-gradient(circle at 30% 30%, #2196f3 2px, transparent 2px),
    radial-gradient(circle at 70% 70%, #2196f3 2px, transparent 2px),
    radial-gradient(circle at 40% 80%, #2196f3 2px, transparent 2px),
    radial-gradient(circle at 80% 40%, #2196f3 2px, transparent 2px);
  background-size: 100% 100%;
  position: relative;
  z-index: -2;
}

.neuron-network::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(45deg, transparent 45%, #2196f3 45%, #2196f3 55%, transparent 55%),
    linear-gradient(-45deg, transparent 45%, #2196f3 45%, #2196f3 55%, transparent 55%);
  background-size: 30px 30px;
  opacity: 0.1;
  animation: neuronPulse 3s ease-in-out infinite;
}

/* 添加DNA双螺旋装饰 */
.dna-helix {
  position: absolute;
  top: 20%;
  left: 10%;
  width: 60px;
  height: 300px;
  opacity: 0.08;
  background: repeating-linear-gradient(
    45deg,
    transparent,
    transparent 10px,
    #2196f3 10px,
    #2196f3 20px
  );
  animation: dnaRotate 15s linear infinite;
  z-index: -1;
}

.dna-helix::after {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    -45deg,
    transparent,
    transparent 10px,
    #64b5f6 10px,
    #64b5f6 20px
  );
  opacity: 0.5;
}

/* 动画关键帧 */
@keyframes logoPulse {
  0%, 100% {
    filter: drop-shadow(0 4px 12px rgba(18, 150, 219, 0.2));
  }
  50% {
    filter: drop-shadow(0 8px 20px rgba(18, 150, 219, 0.4));
  }
}

@keyframes heartbeat {
  from {
    background-position-x: 0;
  }
  to {
    background-position-x: -200px;
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes verticalMove {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(-200px);
  }
}

@keyframes brainwave {
  from {
    background-position-x: 0;
  }
  to {
    background-position-x: -100px;
  }
}

@keyframes neuronPulse {
  0%, 100% {
    opacity: 0.1;
  }
  50% {
    opacity: 0.2;
  }
}

@keyframes dnaRotate {
  from {
    transform: perspective(500px) rotateY(0deg);
  }
  to {
    transform: perspective(500px) rotateY(360deg);
  }
}

@keyframes pulse {
  0% {
    transform: translate(-50%, -50%) scale(0.5);
    opacity: 0.5;
  }
  100% {
    transform: translate(-50%, -50%) scale(2);
    opacity: 0;
  }
}

/* 响应式调整 */
@media (max-width: 480px) {
  .login-card {
    width: 90%;
    margin: 0 20px;
    padding: 2rem;
  }
  
  .main-title {
    font-size: 1.8rem;
  }
  
  .sub-title {
    font-size: 0.85rem;
  }
}
</style>

