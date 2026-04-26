<script setup>
import { computed, ref } from 'vue'

const questions = [
  {
    text: '父母平时是否长期独居、缺少陪伴？',
    options: [
      { text: '是，独居或很少见面', value: 'lonely' },
      { text: '否，日常联系比较多', value: 'normal' }
    ]
  },
  {
    text: '父母是否特别关注保健、偏方、养生讲座？',
    options: [
      { text: '是，经常接触这类信息', value: 'health' },
      { text: '一般，以正规就医为主', value: 'normal' }
    ]
  },
  {
    text: '父母是否容易被免费礼品、返利优惠吸引？',
    options: [
      { text: '是，经常参加免费活动', value: 'greedy' },
      { text: '否，不太会为了便宜行动', value: 'normal' }
    ]
  },
  {
    text: '父母是否容易相信高收益投资或内部项目？',
    options: [
      { text: '是，对高回报比较心动', value: 'investor' },
      { text: '否，理财习惯比较保守', value: 'normal' }
    ]
  },
  {
    text: '父母使用手机是否不熟练，容易点错链接或安装 App？',
    options: [
      { text: '是，手机操作比较吃力', value: 'tech' },
      { text: '否，基本能正常使用', value: 'normal' }
    ]
  }
]

const answers = ref([])

const resultMap = {
  lonely: {
    name: '孤独空巢型',
    description: '这类父母更容易因为缺少陪伴，而相信陌生人、情感安慰或上门关怀。',
    link: '/profiles/lonely',
    tips: ['固定联系频率', '鼓励真实社交', '上门服务先核实身份']
  },
  health: {
    name: '健康焦虑型',
    description: '这类父母更容易被保健品、专家讲座、免费体检等话术吸引。',
    link: '/profiles/health-anxiety',
    tips: ['正规医院体检', '大额健康消费先确认', '不轻信“特效药”']
  },
  greedy: {
    name: '贪小便宜型',
    description: '这类父母更容易被免费领礼品、返利、低价促销和抽奖套路引导。',
    link: '/profiles/greedy',
    tips: ['提醒“免费最贵”', '不随便扫码', '不参加陌生领奖活动']
  },
  investor: {
    name: '盲目投资型',
    description: '这类父母更容易被高收益、养老理财、内部渠道、熟人荐股诱导。',
    link: '/profiles/investor',
    tips: ['统一资金管理', '高收益默认高风险', '投资前必须二次确认']
  },
  tech: {
    name: '技术懵懂型',
    description: '这类父母更容易被钓鱼链接、共享屏幕、验证码和假 App 套路影响。',
    link: '/profiles/tech-illiterate',
    tips: ['关闭未知来源安装', '验证码绝不外泄', '陌生链接不点击']
  },
  normal: {
    name: '综合防范型',
    description: '整体风险不算突出，但仍需要持续提醒和家庭防骗规则。',
    link: '/profiles/',
    tips: ['定期分享新骗局', '大额转账先确认', '保持持续沟通']
  }
}

const canSubmit = computed(() => answers.value.filter(Boolean).length === questions.length)

const result = computed(() => {
  if (!canSubmit.value) return null

  const counts = {}
  for (const value of answers.value) {
    counts[value] = (counts[value] || 0) + 1
  }

  const top = Object.entries(counts).sort((a, b) => b[1] - a[1])[0]?.[0] || 'normal'
  return resultMap[top] || resultMap.normal
})

const choose = (index, value) => {
  answers.value[index] = value
}

const reset = () => {
  answers.value = []
}
</script>

<template>
  <div class="page-shell">
    <section class="page-hero quiz-hero">
      <div>
        <span class="page-badge">3 分钟测试</span>
        <h1>测一测父母属于哪类高风险人群</h1>
        <p>这个测试不是为了贴标签，而是为了更快找到更适合的沟通方式和防范重点。</p>
      </div>
      <div class="hero-side">
        <strong>测试建议</strong>
        <ul>
          <li>按父母平时真实状态作答</li>
          <li>不要按“理想状态”选择</li>
          <li>结果出来后直接查看对应对策</li>
        </ul>
      </div>
    </section>

    <section class="quiz-layout">
      <div class="card-block">
        <div class="section-head">
          <h2>开始测试</h2>
          <button class="ghost-btn" @click="reset">重新开始</button>
        </div>

        <div class="question-list">
          <article v-for="(question, index) in questions" :key="question.text" class="question-card">
            <strong>{{ index + 1 }}. {{ question.text }}</strong>
            <div class="question-options">
              <button
                v-for="option in question.options"
                :key="option.text"
                class="option-btn"
                :class="{ active: answers[index] === option.value }"
                @click="choose(index, option.value)"
              >
                {{ option.text }}
              </button>
            </div>
          </article>
        </div>
      </div>

      <div class="card-block result-panel">
        <div class="section-head">
          <h2>测试结果</h2>
        </div>

        <template v-if="result">
          <span class="result-tag">{{ result.name }}</span>
          <p class="result-desc">{{ result.description }}</p>
          <div class="tips-box">
            <strong>建议先做这 3 件事</strong>
            <ul>
              <li v-for="tip in result.tips" :key="tip">{{ tip }}</li>
            </ul>
          </div>
          <a class="primary-button blue" :href="result.link">查看对应人群指南</a>
        </template>

        <template v-else>
          <p class="result-placeholder">完成全部 5 道题后，这里会直接告诉你更适合先看的防骗对策。</p>
          <div class="tips-box subtle">
            <strong>你最终会得到</strong>
            <ul>
              <li>一个更接近父母状态的人群类型</li>
              <li>3 条优先处理建议</li>
              <li>对应的详细防范页面入口</li>
            </ul>
          </div>
        </template>
      </div>
    </section>
  </div>
</template>

<style scoped>
.page-shell { width: min(100%, 1240px); margin: 0 auto; padding: 1.25rem 1.25rem 2rem; }
.page-hero, .card-block { border: 1px solid #dce7ff; border-radius: 24px; background: #fff; box-shadow: 0 10px 28px rgba(44,73,138,.06); }
.page-hero { display:grid; grid-template-columns:minmax(0,1.4fr) 300px; gap:1rem; padding:1.5rem; }
.page-badge { display:inline-flex; padding:.3rem .65rem; border-radius:999px; background:#edf4ff; color:#3777f4; font-size:.82rem; font-weight:700; }
.page-hero h1 { margin:.9rem 0 .8rem; font-size:clamp(2.2rem,4vw,3.4rem); line-height:1.15; color:#213d72; }
.page-hero p { margin:0; color:#69758d; font-size:1.08rem; line-height:1.8; }
.hero-side { padding:1rem 1.1rem; border-radius:18px; background:linear-gradient(180deg,#f7fbff,#fff); border:1px solid #dce8ff; }
.hero-side strong { color:#2e63cf; }
.hero-side ul { margin:.8rem 0 0; padding-left:1.15rem; color:#6a7181; line-height:1.9; }
.quiz-layout { display:grid; grid-template-columns:minmax(0,1.55fr) 360px; gap:1rem; margin-top:1rem; }
.card-block { padding:1.1rem; }
.section-head { display:flex; justify-content:space-between; align-items:center; gap:1rem; margin-bottom:.85rem; }
.section-head h2 { margin:0; color:#223d72; font-size:1.8rem; }
.ghost-btn { border:1px solid #d9e4ff; background:#fff; color:#4d78da; border-radius:12px; padding:.6rem .9rem; cursor:pointer; }
.question-list { display:grid; gap:.85rem; }
.question-card { padding:1rem; border:1px solid #e4ebff; border-radius:18px; background:linear-gradient(180deg,#fff,#fbfdff); }
.question-card strong { display:block; color:#254074; margin-bottom:.8rem; }
.question-options { display:grid; grid-template-columns:1fr 1fr; gap:.65rem; }
.option-btn { padding:.9rem 1rem; border:1px solid #dfe8ff; border-radius:14px; background:#fff; color:#5d6b83; text-align:left; cursor:pointer; transition:.18s ease; }
.option-btn.active { border-color:#4d7de4; background:#edf4ff; color:#21427c; font-weight:700; }
.result-panel { background:linear-gradient(180deg,#f8fbff,#fff); }
.result-tag { display:inline-flex; padding:.35rem .75rem; border-radius:999px; background:#ecf4ff; color:#3776f2; font-weight:700; }
.result-desc, .result-placeholder { margin:1rem 0 0; color:#6b758b; line-height:1.8; }
.tips-box { margin-top:1rem; padding:1rem; border:1px solid #dfe8ff; border-radius:16px; background:#fff; }
.tips-box.subtle { background:#fbfdff; }
.tips-box strong { color:#244073; }
.tips-box ul { margin:.7rem 0 0; padding-left:1.1rem; color:#69758d; line-height:1.8; }
.primary-button { display:block; margin-top:1rem; padding:.92rem 1rem; border-radius:14px; color:#fff; text-align:center; text-decoration:none; font-weight:700; }
.primary-button.blue { background:linear-gradient(180deg,#4d87f4,#356be4); }
@media (max-width: 1100px) { .page-hero,.quiz-layout { grid-template-columns:1fr; } }
@media (max-width: 720px) { .page-shell { padding:.75rem .9rem 1.5rem; } .question-options { grid-template-columns:1fr; } }
</style>
