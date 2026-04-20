# 人群测试

> 3分钟测试，了解父母属于哪种易骗类型

---

<script setup>
import { ref } from 'vue'

const questions = [
  {
    text: '父母平时独居还是和子女同住？',
    options: [
      { text: '独居，很少见面', value: 'lonely' },
      { text: '同住或经常见面', value: 'normal' }
    ]
  },
  {
    text: '父母对健康的关注程度？',
    options: [
      { text: '非常关注，经常买保健品', value: 'health' },
      { text: '一般，正常体检', value: 'normal' }
    ]
  },
  {
    text: '父母是否喜欢占便宜、领免费礼品？',
    options: [
      { text: '经常参加免费活动', value: 'greedy' },
      { text: '不太在意这些', value: 'normal' }
    ]
  },
  {
    text: '父母对投资理财的态度？',
    options: [
      { text: '想钱生钱，容易相信高回报', value: 'investor' },
      { text: '保守，存银行定期', value: 'normal' }
    ]
  },
  {
    text: '父母使用手机熟练程度？',
    options: [
      { text: '不太会，经常点错', value: 'tech' },
      { text: '会用微信、刷视频', value: 'normal' }
    ]
  }
]

const answers = ref([])
const result = ref(null)

const answer = (idx, value) => {
  answers.value[idx] = value
}

const calculateResult = () => {
  const counts = {}
  answers.value.forEach(v => {
    counts[v] = (counts[v] || 0) + 1
  })
  
  const maxType = Object.entries(counts)
    .sort((a, b) => b[1] - a[1])[0][0]
  
  const results = {
    lonely: {
      name: '孤独空巢型',
      description: '父母独居、缺乏陪伴，容易相信陌生人和上门推销。',
      tips: [
        '每天固定时间视频通话',
        '帮父母建立社交圈',
        '上门人员必须经你确认'
      ],
      link: '/profiles/lonely'
    },
    health: {
      name: '健康焦虑型',
      description: '父母怕生病、信特效，容易被保健品和养生讲座忽悠。',
      tips: [
        '定期带父母去正规医院体检',
        '消费权限限制，大额需审核',
        '买正规保健品满足需求'
      ],
      link: '/profiles/health-anxiety'
    },
    greedy: {
      name: '贪小便宜型',
      description: '父母节俭、爱薅羊毛，容易被免费礼品和返利诈骗。',
      tips: [
        '科普"免费的东西最贵"',
        '主动帮父母采购生活用品',
        '禁止随意扫码、点击链接'
      ],
      link: '/profiles/greedy'
    },
    investor: {
      name: '盲目投资型',
      description: '父母想钱生钱、信高回报，容易被养老理财和虚拟货币诈骗。',
      tips: [
        '资金统一管理',
        '科普"高收益=高风险"',
        '屏蔽投资类骚扰信息'
      ],
      link: '/profiles/investor'
    },
    tech: {
      name: '技术懵懂型',
      description: '父母不会用手机，容易点错链接、扫错码。',
      tips: [
        '关闭"允许安装未知应用"',
        '手把手教学',
        '设置手机权限管控'
      ],
      link: '/profiles/tech-illiterate'
    },
    normal: {
      name: '综合防范型',
      description: '父母相对理性，但仍需保持警惕。',
      tips: [
        '定期分享最新诈骗案例',
        '建立家庭反诈确认流程',
        '保持沟通，及时发现异常'
      ],
      link: '/profiles/'
    }
  }
  
  result.value = results[maxType] || results.normal
}

const reset = () => {
  answers.value = []
  result.value = null
}
</script>

<div class="quiz-container">
  <h2>开始测试</h2>
  
  <div v-if="!result" class="questions">
    <div v-for="(q, idx) in questions" :key="idx" class="question">
      <p class="q-text">{{ idx + 1 }}. {{ q.text }}</p>
      <div class="options">
        <button 
          v-for="opt in q.options" 
          :key="opt.value"
          @click="answer(idx, opt.value)"
          :class="{ selected: answers[idx] === opt.value }"
        >
          {{ opt.text }}
        </button>
      </div>
    </div>
    
    <button 
      v-if="answers.length === questions.length"
      @click="calculateResult"
      class="submit-btn"
    >
      查看结果
    </button>
  </div>
  
  <div v-else class="result">
    <h3>测试结果：{{ result.name }}</h3>
    <p class="desc">{{ result.description }}</p>
    <div class="advice">
      <h4>针对性建议：</h4>
      <ul>
        <li v-for="tip in result.tips" :key="tip">{{ tip }}</li>
      </ul>
    </div>
    <a :href="result.link" class="detail-link">查看详细防范指南 →</a>
    <button @click="reset" class="reset-btn">重新测试</button>
  </div>
</div>

<style scoped>
.quiz-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px 0;
}

.question {
  margin-bottom: 24px;
  padding: 16px;
  background: #f5f5f5;
  border-radius: 8px;
}

.q-text {
  font-weight: 500;
  margin-bottom: 12px;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.options button {
  padding: 10px 16px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  text-align: left;
}

.options button.selected {
  background: #4CAF50;
  color: white;
  border-color: #4CAF50;
}

.submit-btn, .reset-btn {
  width: 100%;
  padding: 14px;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
}

.result {
  text-align: center;
  padding: 24px;
  background: #e8f5e9;
  border-radius: 12px;
}

.result h3 {
  color: #2e7d32;
  margin-bottom: 12px;
}

.desc {
  color: #555;
  margin-bottom: 20px;
}

.advice {
  text-align: left;
  background: white;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.advice h4 {
  margin-bottom: 12px;
}

.advice ul {
  padding-left: 20px;
}

.advice li {
  margin-bottom: 8px;
}

.detail-link {
  display: inline-block;
  color: #2196F3;
  text-decoration: none;
  margin-bottom: 16px;
}

.reset-btn {
  background: #757575;
}
</style>
