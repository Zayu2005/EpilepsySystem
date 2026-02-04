<template>
  <div class="virtual-assistant-container">
    <div class="assistant-header">
      <h1>智能医疗助手</h1>
      <p>您的专属医疗顾问，随时为您解答问题</p>
    </div>

    <div class="assistant-content">
      <div class="assistant-avatar">
        <div class="avatar-container">
          <img src="http://cloud.epilepsy-detect.xyz/logo.png" alt="医疗助手" class="avatar-image">
          <div class="avatar-status">在线</div>
          <div class="avatar-pulse"></div>
        </div>
        <div class="avatar-info">
          <h2>小智</h2>
          <p>脑域衡安智能助手</p>
          <div class="avatar-stats">
            <div class="stat-item">
              <span class="stat-value">98%</span>
              <span class="stat-label">满意度</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">24/7</span>
              <span class="stat-label">全天候服务</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">5000+</span>
              <span class="stat-label">咨询次数</span>
            </div>
          </div>
        </div>
      </div>


      <div class="assistant-features">
        <el-card v-for="(feature, index) in features" :key="index" class="feature-card">
          <div class="feature-icon">
            <el-icon>
              <component :is="feature.icon"></component>
            </el-icon>
          </div>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
          <el-button type="primary" @click="navigateTo(feature.route)" class="feature-button">
            {{ feature.buttonText }}
            <el-icon class="el-icon--right"><ArrowRight /></el-icon>
          </el-button>
        </el-card>
      </div>
    </div>

    <!-- 添加医院信息轮播图 -->
    <div class="hospital-carousel">
      <h2 class="carousel-title">癫痫先锋</h2>
      <el-carousel :interval="4000" type="card" height="300px">
        <el-carousel-item v-for="(item, index) in hospitalInfo" :key="index">
          <div class="carousel-content">
            <img :src="item.image" :alt="item.title">
            <div class="carousel-text">
              <h3>{{ item.title }}</h3>
              <p>{{ item.description }}</p>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>

    <!-- 添加最新医疗资讯 -->
    <div class="medical-news">
      <h2 class="news-title">最新医疗资讯</h2>
      <div class="news-grid">
        <el-card v-for="(news, index) in medicalNews" :key="index" class="news-card">
          <div class="news-image">
            <img :src="news.image" :alt="news.title">
            <div class="news-tag" :class="news.tagType">{{ news.tag }}</div>
          </div>
          <div class="news-content">
            <h3>{{ news.title }}</h3>
            <p>{{ news.summary }}</p>
            <div class="news-footer">
              <span class="news-date">{{ news.date }}</span>
              <el-button type="text" @click="readMore(news)">阅读更多</el-button>
            </div>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 添加医生团队展示 -->
    <div class="doctor-team">
      <h2 class="team-title">专家团队</h2>
      <div class="team-grid">
        <div v-for="(doctor, index) in doctorTeam" :key="index" class="doctor-card">
          <div class="doctor-avatar">
            <img :src="doctor.avatar" :alt="doctor.name">
          </div>
          <div class="doctor-info">
            <h3>{{ doctor.name }}</h3>
            <p class="doctor-title">{{ doctor.title }}</p>
            <p class="doctor-specialty">{{ doctor.specialty }}</p>
            <div class="doctor-stats">
              <div class="doctor-stat">
                <span class="stat-number">{{ doctor.experience }}</span>
                <span class="stat-label">年经验</span>
              </div>
              <div class="doctor-stat">
                <span class="stat-number">{{ doctor.patients }}</span>
                <span class="stat-label">患者</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加用户评价 -->
    <div class="user-testimonials">
      <h2 class="testimonials-title">医生使用评价</h2>
      <el-carousel :interval="5000" indicator-position="none" height="200px" class="testimonial-carousel">
        <el-carousel-item v-for="(testimonial, index) in testimonials" :key="index">
          <div class="testimonial-card">
            <div class="testimonial-quote">"</div>
            <p class="testimonial-content">{{ testimonial.content }}</p>
            <div class="testimonial-user">
              <img :src="testimonial.avatar" :alt="testimonial.name" class="testimonial-avatar">
              <div class="testimonial-user-info">
                <h4>{{ testimonial.name }}</h4>
                <p>{{ testimonial.title }}</p>
                <div class="testimonial-rating">
                  <el-icon v-for="i in 5" :key="i" :class="i <= testimonial.rating ? 'star-filled' : 'star-empty'">
                    <Star />
                  </el-icon>
                </div>
              </div>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>

    <!-- 虚拟形象保持在最后 -->
    <div class="virtual-avatar-floating">
      <img src="@/assets/虚拟形象-min.gif" alt="虚拟助手" class="virtual-avatar-gif">
      <div class="avatar-chat-bubble" v-if="showChatBubble">
        <p>{{ chatBubbleText }}</p>
        <div class="chat-bubble-actions">
          <el-button type="primary" size="small" @click="startChat">开始对话</el-button>
          <el-button type="text" size="small" @click="dismissBubble">稍后再说</el-button>
        </div>
      </div>
    </div>

    <!-- 页脚 -->
    <footer class="assistant-footer">
      <div class="footer-content">
        <div class="footer-section">
          <h3>关于我们</h3>
          <p>脑域衡安致力于提供最先进的癫痫诊断与治疗服务，结合AI技术为患者提供个性化医疗方案。</p>
        </div>
        <div class="footer-section">
          <h3>联系方式</h3>
          <p><el-icon><Location /></el-icon> 陕西省西安市临潼区陕鼓大道58号</p>
          <p><el-icon><Phone /></el-icon> 400-123-4567</p>
          <p><el-icon><Message /></el-icon> contact@epilepsy-ai.com</p>
        </div>
        <div class="footer-section">
          <h3>快速链接</h3>
          <ul>
            <li><a href="#">首页</a></li>
            <li><a href="#">关于我们</a></li>
            <li><a href="#">服务项目</a></li>
            <li><a href="#">专家团队</a></li>
            <li><a href="#">联系我们</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2025 脑域衡安 - 智能医疗助手. 保留所有权利.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import {
  ChatLineRound,
  User,
  Document,
  Bell,
  QuestionFilled,
  Cpu,
  TrendCharts,
  Calendar,
  ArrowRight,
  Star,
  Location,
  Phone,
  Message
} from '@element-plus/icons-vue';

const router = useRouter();
const showChatBubble = ref(false);
const chatBubbleText = ref('您好！需要我为您提供医疗咨询服务吗？');

// 功能卡片
const features = [
  {
    icon: 'ChatLineRound',
    title: '智能问诊',
    description: '通过AI技术，为您提供初步的医疗咨询和建议，解答您的健康疑问',
    buttonText: '开始咨询',
    route: '/chat'
  },
  {
    icon: 'Cpu',
    title: '脑电波分析',
    description: '上传脑电波数据，获取专业分析和建议，辅助医生进行精准诊断',
    buttonText: '上传数据',
    route: '/eeg'
  },
  {
    icon: 'Document',
    title: '病历管理',
    description: '查看和管理您的电子病历，随时掌握健康状况，跟踪治疗进展',
    buttonText: '查看病历',
    route: '/patient'
  },
  {
    icon: 'TrendCharts',
    title: '健康监测',
    description: '实时监测患者状态，及时发现异常情况，提供预警和干预建议',
    buttonText: '查看监测',
    route: '/ward'
  }
];

// 快速操作按钮
const quickActions = [
  {
    label: '预约挂号',
    icon: 'Calendar',
    type: 'primary',
    action: 'appointment'
  },
  {
    label: '紧急求助',
    icon: 'Bell',
    type: 'danger',
    action: 'emergency'
  },
  {
    label: '常见问题',
    icon: 'QuestionFilled',
    type: 'info',
    action: 'faq'
  },
  {
    label: '联系医生',
    icon: 'User',
    type: 'success',
    action: 'contact'
  }
];

// 医院信息数据
const hospitalInfo = [
  {
    title: 'Dravet综合征',
    description: '美国FDA批准首款针对Dravet综合征​（难治性癫痫）的基因疗法 ​STK-001，通过反义寡核苷酸技术修复SCN1A基因功能，减少发作频率。',
    image: 'http://cloud.epilepsy-detect.xyz/FDA.jpg'
  },
  {
    title: '癫痫治疗向个性化、精准化迈进',
    description: '首都医科大学宣武医院赵国光、任连坤团队在《Brain》发表研究，​首次提出脑深部白质节点的神经调控策略。通过靶向最外囊（EC）的白质纤维束，采用1Hz爆发式电刺激抑制癫痫发作，效果与传统高频刺激相当，为药物难治性癫痫提供新方向',
    image: 'http://cloud.epilepsy-detect.xyz/brain.png'
  },
  {
    title: '干细胞疗法实现癫痫发作减少95%',
    description: 'Neurona Therapeutics公司发布临床研究数据，​NRTX-1001干细胞疗法通过移植GABA能抑制性神经元，使两名耐药性癫痫患者的月度发作减少>95%，且无严重副作用，标志再生医学在癫痫治疗中的突破',
    image: 'http://cloud.epilepsy-detect.xyz/cell.png'
  },
  {
    title: '北京医大癫痫治疗中心专访',
    description: '高伟博士指出，​新型钙/钾通道阻滞剂药物进入临床试验，结合无创神经调控技术​（如经颅磁刺激TMS），显著提高难治性癫痫控制率。同时，​中西医结合治疗通过针灸、中药与精准药物联用，优化患者个体化方案',
    image: 'http://cloud.epilepsy-detect.xyz/%E5%AE%A3%E6%AD%A6%E5%8C%BB%E9%99%A2.jpg'
  }
];

// 添加医疗新闻
const medicalNews = [
  {
    title: '新型脑电图分析算法提高癫痫诊断准确率',
    summary: '研究人员开发出基于深度学习的脑电图分析算法，能够识别微妙的癫痫特征，诊断准确率提高30%',
    image: 'http://cloud.epilepsy-detect.xyz/bb34-8a52533ddb65ae94c4ba7f157ecdd94d.png',
    tag: '技术创新',
    tagType: 'tech',
    date: '2024-11-15',
    url: 'https://zhuanlan.zhihu.com/p/709069018'
  },
  {
    title: '癫痫患者生活质量调查报告发布',
    summary: '全国癫痫患者生活质量调查显示，规范治疗和社会支持对患者生活质量影响显著',
    image: 'https://medtion-image.medtion.com/pgc/20230130/c42f48f692b8cafc6515afe2084478b0.png?x-oss-process=image/watermark,image_d2F0ZXJtYXJrL25hb3lpaHVpLnBuZz94LW9zcy1wcm9jZXNzPWltYWdlL3Jlc2l6ZSxQXzE1',
    tag: '研究报告',
    tagType: 'research',
    date: '2024-11-10',
    url: 'https://caae.org.cn/news/show/id/308'
  },
  {
    title: '远程脑电监测系统在农村地区的应用',
    summary: '远程脑电监测系统在农村地区试点成功，让偏远地区患者也能获得专业诊断',
    image: 'https://tse4-mm.cn.bing.net/th/id/OIP-C.uK82SUgOSTIyVP7H7Tw-6wAAAA?rs=1&pid=ImgDetMain',
    tag: '医疗普惠',
    tagType: 'social',
    date: '2024-11-05',
    url: 'http://www.jcme.org.cn/update/2021/06/%E8%BF%9C%E7%A8%8B%E5%8C%BB%E7%96%97%E5%9C%A8%E5%86%9C%E6%9D%91%E5%9C%B0%E5%8C%BA%E8%84%91%E5%8D%92%E4%B8%AD%E5%81%A5%E5%BA%B7%E7%AE%A1%E7%90%86%E4%B8%AD%E7%9A%84%E7%A0%94%E7%A9%B6%E8%BF%9B%E5%B1%95.pdf'
  }
];

// 添加医生团队
const doctorTeam = [
  {
    name: '张教授',
    title: '主任医师',
    specialty: '癫痫诊断与治疗',
    experience: 25,
    patients: '5000+',
    avatar: 'https://tse4-mm.cn.bing.net/th/id/OIP-C.eiELMZuzP-Uti291B5SXAQHaEJ?rs=1&pid=ImgDetMain'
  },
  {
    name: '李医生',
    title: '副主任医师',
    specialty: '儿童癫痫',
    experience: 15,
    patients: '3000+',
    avatar: 'https://tse2-mm.cn.bing.net/th/id/OIP-C.lDACdbFCufGMcxa11Cv5xAHaEJ?w=279&h=180&c=7&r=0&o=5&dpr=1.7&pid=1.7'
  },
  {
    name: '王医生',
    title: '主治医师',
    specialty: '神经电生理',
    experience: 10,
    patients: '2000+',
    avatar: 'https://tse3-mm.cn.bing.net/th/id/OIP-C.MSooBf57xsk0GPXI4MXRAgHaE7?w=285&h=190&c=7&r=0&o=5&dpr=1.7&pid=1.7'
  }
];

// 添加用户评价
const testimonials = [
  {
    content: '  这个网站真正填补了临床癫痫管理的数字工具空白！特别是AI辅助的发作类型识别和用药建议模块，能帮助我们在紧急情况下快速调取个性化方案。多学科协作平台也让我们神经科、急诊科和影像科团队实现了无缝对接，大幅提升了抢救效率',
    name: '张医生',
    title: '神经科主任医师',
    rating: 5,
    avatar: 'https://tse1-mm.cn.bing.net/th/id/OIP-C.KZqIjr2_bI7gYxaxin3o7gHaHa?w=163&h=180&c=7&r=0&o=5&dpr=1.7&pid=1.7'
  },
  {
    content: '通过AI助手的远程咨询功能，我可以上传脑电波数据从而获得智能分析，这极大的帮助了我治疗我的患者!',
    name: '张医生',
    title: '乡村医生',
    rating: 5,
    avatar: 'data:image/jpeg;base64,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'
  },
  {
    content: '作为一名基层医生，这个系统帮助我更准确地诊断复杂病例，提高了我的工作效率和诊断准确率。',
    name: '王医生',
    title: '社区医院医师',
    rating: 4,
    avatar: 'https://tse1-mm.cn.bing.net/th/id/OIP-C.ynj93Pixkci8fWNnC9wYUAHaJ1?w=122&h=180&c=7&r=0&o=5&dpr=1.7&pid=1.7'
  }
];

// 导航到其他页面
const navigateTo = (route) => {
  router.push(route);
};

// 处理快速操作
const handleQuickAction = (action) => {
  switch(action) {
    case 'appointment':
      router.push('/appointment');
      break;
    case 'emergency':
      router.push('/emergency');
      break;
    case 'faq':
      router.push('/faq');
      break;
    case 'contact':
      router.push('/contact');
      break;
  }
};

// 阅读更多新闻
const readMore = (news) => {
  window.open(news.url, '_blank');
};

// 咨询医生
const consultDoctor = (doctor) => {
  router.push({
    path: '/doctor-consult',
    query: { doctorId: doctor.name }
  });
};

// 开始聊天
const startChat = () => {
  router.push('/chat');
};

// 关闭聊天气泡
const dismissBubble = () => {
  showChatBubble.value = false;
};

onMounted(() => {
  // 显示聊天气泡
  setTimeout(() => {
    showChatBubble.value = true;
  }, 3000);

  // 定时更换聊天气泡文本
  const bubbleTexts = [
    '您好！需要我为您提供医疗咨询服务吗？',
    '有任何关于癫痫的问题，都可以向我咨询！',
    '我可以帮您分析脑电图数据，您需要上传吗？',
    '今天感觉如何？需要查看您的健康报告吗？'
  ];

  let textIndex = 0;
  setInterval(() => {
    if (showChatBubble.value) {
      textIndex = (textIndex + 1) % bubbleTexts.length;
      chatBubbleText.value = bubbleTexts[textIndex];
    }
  }, 8000);
});
</script>

<style scoped>
.virtual-assistant-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4ecf7 100%);
  min-height: calc(100vh - 60px);
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
}

.virtual-assistant-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
      radial-gradient(circle at 10% 10%, rgba(64, 158, 255, 0.05) 0%, transparent 50%),
      radial-gradient(circle at 90% 90%, rgba(103, 194, 58, 0.05) 0%, transparent 50%);
  z-index: -1;
}

.assistant-header {
  text-align: center;
  margin-bottom: 40px;
  padding: 30px 0;
  position: relative;
  animation: fadeIn 0.8s ease-out;
}

.assistant-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 3px;
  background: linear-gradient(90deg, #409EFF, #79bbff);
  border-radius: 3px;
}

.assistant-header h1 {
  font-size: 36px;
  color: #2c3e50;
  margin-bottom: 15px;
  background: linear-gradient(120deg, #2196f3, #1976d2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 1px;
}

.assistant-header p {
  font-size: 18px;
  color: #606266;
  max-width: 600px;
  margin: 0 auto;
}

.assistant-content {
  display: flex;
  flex-direction: column;
  gap: 40px;
  margin-bottom: 40px;
}

.assistant-avatar {
  display: flex;
  align-items: center;
  gap: 30px;
  background: rgba(255, 255, 255, 0.8);
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  animation: slideInLeft 0.8s ease-out;
  position: relative;
  overflow: hidden;
}

.assistant-avatar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(64, 158, 255, 0.05), transparent);
  z-index: 0;
}

.avatar-container {
  position: relative;
  z-index: 1;
}

.avatar-image {
  width: 150px;
  height: 150px;
  border-radius: 75px;
  object-fit: cover;
  border: 5px solid white;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  animation: pulse 3s infinite;
}

.avatar-pulse {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 50%;
  border: 3px solid rgba(64, 158, 255, 0.5);
  animation: pulseBorder 2s infinite;
}

@keyframes pulseBorder {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(1.3);
    opacity: 0;
  }
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(33, 150, 243, 0.4);
  }
  70% {
    box-shadow: 0 0 0 15px rgba(33, 150, 243, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(33, 150, 243, 0);
  }
}

.avatar-status {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: #67C23A;
  color: white;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  z-index: 2;
}

.avatar-info {
  flex: 1;
  z-index: 1;
}

.avatar-info h2 {
  font-size: 28px;
  margin-bottom: 8px;
  color: #2c3e50;
  position: relative;
  display: inline-block;
}

.avatar-info h2::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 40px;
  height: 3px;
  background: linear-gradient(90deg, #409EFF, #79bbff);
  border-radius: 3px;
}

.avatar-info p {
  color: #606266;
  font-size: 16px;
  margin-bottom: 20px;
}

.avatar-stats {
  display: flex;
  gap: 30px;
  margin-top: 20px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #409EFF;
}

.stat-label {
  font-size: 14px;
  color: #606266;
  margin-top: 5px;
}

.quick-actions {
  margin-bottom: 20px;
  animation: slideInRight 0.8s ease-out;
}

.quick-actions h2 {
  font-size: 22px;
  margin-bottom: 20px;
  color: #2c3e50;
  position: relative;
  display: inline-block;
}

.quick-actions h2::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 30px;
  height: 3px;
  background: linear-gradient(90deg, #409EFF, #79bbff);
  border-radius: 3px;
}

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 8px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.action-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.assistant-features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
  gap: 25px;
  animation: fadeIn 1s ease-out;
}

.feature-card {
  padding: 25px;
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(5px);
  border-radius: 12px;
  border: none;
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 5px;
  background: linear-gradient(90deg, #409EFF, #79bbff);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.feature-card:hover::before {
  transform: scaleX(1);
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 36px;
  color: #409EFF;
  margin-bottom: 20px;
  background: rgba(64, 158, 255, 0.1);
  width: 70px;
  height: 70px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.feature-card:hover .feature-icon {
  background: rgba(64, 158, 255, 0.2);
  transform: scale(1.1);
}

.feature-card h3 {
  font-size: 20px;
  margin-bottom: 15px;
  color: #2c3e50;
}

.feature-card p {
  color: #606266;
  margin-bottom: 20px;
  flex: 1;
  line-height: 1.6;
}

.feature-button {
  align-self: flex-start;
  transition: all 0.3s ease;
  border-radius: 8px;
  padding: 10px 20px;
}

.feature-button:hover {
  transform: translateX(5px);
}

/* 医院轮播图样式 */
.hospital-carousel {
  margin-top: 50px;
  margin-bottom: 60px;
  padding: 30px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}

.carousel-title {
  text-align: center;
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 30px;
  background: linear-gradient(120deg, #2196f3, #1976d2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  position: relative;
  display: inline-block;
  left: 50%;
  transform: translateX(-50%);
}

.carousel-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #409EFF, #79bbff);
  border-radius: 3px;
  left: 50%;
  transform: translateX(-50%);
}

.carousel-content {
  height: 100%;
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.carousel-content img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.carousel-text {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 25px;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
  color: white;
}

.carousel-text h3 {
  font-size: 22px;
  margin-bottom: 10px;
  font-weight: 600;
}

.carousel-text p {
  font-size: 14px;
  opacity: 0.9;
  line-height: 1.6;
}

.el-carousel__item {
  border-radius: 12px;
}

.el-carousel__item:hover img {
  transform: scale(1.05);
}

/* 医疗新闻样式 */
.medical-news {
  margin-bottom: 60px;
}

.news-title {
  text-align: center;
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 30px;
  background: linear-gradient(120deg, #2196f3, #1976d2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  position: relative;
  display: inline-block;
  left: 50%;
  transform: translateX(-50%);
}

.news-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #409EFF, #79bbff);
  border-radius: 3px;
  left: 50%;
  transform: translateX(-50%);
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
}

.news-card {
  border: none;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  height: 100%;
}

.news-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
}

.news-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.news-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.news-card:hover .news-image img {
  transform: scale(1.1);
}

.news-tag {
  position: absolute;
  top: 15px;
  right: 15px;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  color: white;
}

.news-tag.tech {
  background: #409EFF;
}

.news-tag.research {
  background: #67C23A;
}

.news-tag.social {
  background: #E6A23C;
}

.news-content {
  padding: 20px;
}

.news-content h3 {
  font-size: 18px;
  margin-bottom: 10px;
  color: #2c3e50;
  line-height: 1.4;
}

.news-content p {
  color: #606266;
  margin-bottom: 15px;
  line-height: 1.6;
  font-size: 14px;
}

.news-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
}

.news-date {
  color: #909399;
  font-size: 12px;
}

/* 医生团队样式 */
.doctor-team {
  margin-bottom: 60px;
}

.team-title {
  text-align: center;
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 30px;
  background: linear-gradient(120deg, #2196f3, #1976d2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  position: relative;
  display: inline-block;
  left: 50%;
  transform: translateX(-50%);
}

.team-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #409EFF, #79bbff);
  border-radius: 3px;
  left: 50%;
  transform: translateX(-50%);
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
}

.doctor-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.doctor-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
}

.doctor-avatar {
  height: 200px;
  overflow: hidden;
}

.doctor-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.doctor-card:hover .doctor-avatar img {
  transform: scale(1.1);
}

.doctor-info {
  padding: 20px;
  text-align: center;
}

.doctor-info h3 {
  font-size: 20px;
  margin-bottom: 5px;
  color: #2c3e50;
}

.doctor-title {
  color: #409EFF;
  font-weight: 500;
  margin-bottom: 5px;
}

.doctor-specialty {
  color: #606266;
  margin-bottom: 15px;
  font-size: 14px;
}

.doctor-stats {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-bottom: 15px;
}

.doctor-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-number {
  font-size: 20px;
  font-weight: 600;
  color: #409EFF;
}

.stat-label {
  font-size: 12px;
  color: #909399;
}

/* 用户评价样式 */
.user-testimonials {
  margin-bottom: 60px;
}

.testimonials-title {
  text-align: center;
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 30px;
  background: linear-gradient(120deg, #2196f3, #1976d2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  position: relative;
  display: inline-block;
  left: 50%;
  transform: translateX(-50%);
}

.testimonials-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #409EFF, #79bbff);
  border-radius: 3px;
  left: 50%;
  transform: translateX(-50%);
}

.testimonial-carousel {
  margin-top: 20px;
}

.testimonial-card {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.testimonial-quote {
  position: absolute;
  top: 20px;
  left: 20px;
  font-size: 60px;
  color: rgba(64, 158, 255, 0.1);
  font-family: Georgia, serif;
  line-height: 1;
}

.testimonial-content {
  font-size: 16px;
  color: #606266;
  line-height: 1.8;
  margin-bottom: 20px;
  font-style: italic;
}

.testimonial-user {
  display: flex;
  align-items: center;
  gap: 15px;
}

.testimonial-avatar {
  width: 50px;
  height: 50px;
  border-radius: 25px;
  object-fit: cover;
}

.testimonial-user-info h4 {
  font-size: 16px;
  margin-bottom: 3px;
  color: #2c3e50;
}

.testimonial-user-info p {
  font-size: 14px;
  color: #909399;
  margin-bottom: 5px;
}

.testimonial-rating {
  display: flex;
  gap: 3px;
}

.star-filled {
  color: #E6A23C;
}

.star-empty {
  color: #DCDFE6;
}

/* 虚拟形象样式 */
.virtual-avatar-floating {
  position: fixed;
  right: 30px;
  bottom: 30px;
  z-index: 100;
  filter: drop-shadow(0 8px 20px rgba(0, 0, 0, 0.3));
  animation: floatAvatar 3s ease-in-out infinite;
  transition: transform 0.3s ease;
}

.virtual-avatar-gif {
  width: 220px;
  height: 220px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid rgba(255, 255, 255, 0.9);
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(5px);
  cursor: pointer;
}

.virtual-avatar-floating:hover {
  transform: scale(1.08);
}

.avatar-chat-bubble {
  position: absolute;
  top: -100px;
  right: 0;
  background: white;
  padding: 15px 20px;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 250px;
  animation: fadeInUp 0.5s ease;
}

.avatar-chat-bubble::after {
  content: '';
  position: absolute;
  bottom: -10px;
  right: 30px;
  width: 20px;
  height: 20px;
  background: white;
  transform: rotate(45deg);
  box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1);
}

.avatar-chat-bubble p {
  margin-bottom: 15px;
  color: #2c3e50;
}

.chat-bubble-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

@keyframes floatAvatar {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-15px);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 页脚样式 */
.assistant-footer {
  margin-top: 60px;
  background: #2c3e50;
  color: white;
  border-radius: 12px;
  overflow: hidden;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  padding: 40px;
}

.footer-section h3 {
  font-size: 18px;
  margin-bottom: 20px;
  position: relative;
  display: inline-block;
}

.footer-section h3::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 30px;
  height: 2px;
  background: #409EFF;
}

.footer-section p {
  margin-bottom: 10px;
  opacity: 0.8;
  line-height: 1.6;
}

.footer-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-section ul li {
  margin-bottom: 10px;
}

.footer-section ul li a {
  color: white;
  opacity: 0.8;
  text-decoration: none;
  transition: all 0.3s ease;
}

.footer-section ul li a:hover {
  opacity: 1;
  color: #409EFF;
}

.footer-bottom {
  background: rgba(0, 0, 0, 0.2);
  padding: 15px 40px;
  text-align: center;
}

.footer-bottom p {
  margin: 0;
  font-size: 14px;
  opacity: 0.7;
}

/* 响应式设计 */
@media (max-width: 992px) {
  .assistant-avatar {
    flex-direction: column;
    text-align: center;
  }

  .avatar-info h2::after {
    left: 50%;
    transform: translateX(-50%);
  }

  .avatar-stats {
    justify-content: center;
  }

  .quick-actions h2 {
    display: block;
    text-align: center;
    width: 100%;
  }

  .quick-actions h2::after {
    left: 50%;
    transform: translateX(-50%);
  }

  .action-buttons {
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .assistant-header h1 {
    font-size: 28px;
  }

  .assistant-header p {
    font-size: 16px;
  }

  .avatar-image {
    width: 120px;
    height: 120px;
  }

  .feature-card {
    padding: 20px;
  }

  .feature-icon {
    width: 60px;
    height: 60px;
    font-size: 28px;
  }

  .feature-card h3 {
    font-size: 18px;
  }

  .carousel-text h3 {
    font-size: 18px;
  }

  .carousel-text p {
    font-size: 12px;
  }

  .virtual-avatar-gif {
    width: 150px;
    height: 150px;
  }

  .avatar-chat-bubble {
    width: 200px;
  }
}

@media (max-width: 576px) {
  .assistant-header h1 {
    font-size: 24px;
  }

  .assistant-header p {
    font-size: 14px;
  }

  .avatar-image {
    width: 100px;
    height: 100px;
  }

  .avatar-stats {
    flex-direction: column;
    gap: 10px;
  }

  .action-button {
    width: 100%;
  }

  .virtual-avatar-gif {
    width: 120px;
    height: 120px;
  }

  .avatar-chat-bubble {
    width: 180px;
    top: -80px;
  }

  .footer-content {
    grid-template-columns: 1fr;
    padding: 30px;
  }
}
</style>