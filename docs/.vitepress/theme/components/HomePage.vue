<script setup>
import cases from '../../../../data/published/cases.json'

const fallbackCases = [
  {
    id: 'fallback-investment',
    tag: '虚假投资理财',
    title: '“高收益理财”陷阱',
    summary: '骗子以“保本高收益”为诱饵，引导老人投资虚假理财产品，最终无法提现。',
    meta: '场景库案例',
    date: '持续更新',
    href: '/scenarios/investment'
  },
  {
    id: 'fallback-police',
    tag: '冒充公检法',
    title: '冒充警察办案诈骗',
    summary: '骗子冒充警察，称老人涉嫌洗钱，要求配合调查并转账到“安全账户”。',
    meta: '高风险预警',
    date: '持续更新',
    href: '/scenarios/fake-police'
  },
  {
    id: 'fallback-health',
    tag: '保健品诈骗',
    title: '免费体检送礼品骗局',
    summary: '以免费体检、赠送礼品为名，诱导老人购买高价保健品，骗取养老金。',
    meta: '常见套路',
    date: '持续更新',
    href: '/scenarios/health-products'
  }
]

const realCases = Array.isArray(cases)
  ? [...cases]
      .sort((a, b) => (b.crawled_at || '').localeCompare(a.crawled_at || ''))
      .slice(0, 3)
      .map((item) => ({
        id: item.id,
        tag: item.scam_type || '最新案例',
        title: item.title || '未命名案例',
        summary: item.summary || '暂无摘要。',
        meta: item.source_name || '公开来源',
        date: item.crawled_at ? item.crawled_at.slice(0, 10) : '最近更新',
        href: `/cases/generated/${item.id}`
      }))
  : []

const latestCases = realCases.length ? realCases : fallbackCases

const quickLinks = [
  {
    title: '应急处理指南',
    description: '如果家人正在被骗',
    href: '/emergency',
    accent: 'blue',
    icon: '🚨'
  },
  {
    title: '测一测父母类型',
    description: '了解父母特点与风险',
    href: '/quiz',
    accent: 'green',
    icon: '👥'
  },
  {
    title: '浏览诈骗案例',
    description: '最新案例与套路解析',
    href: '/cases/latest',
    accent: 'orange',
    icon: '📂'
  },
  {
    title: '人群分类指南',
    description: '针对性防骗建议',
    href: '/profiles/',
    accent: 'purple',
    icon: '📘'
  }
]

const stats = [
  { value: '10+', label: '诈骗场景分类', note: '常见套路全覆盖', icon: '📄' },
  { value: '7+', label: '易骗人群类型', note: '按家庭特点分类', icon: '👥' },
  { value: '3+', label: '实用防骗指南', note: '快速找到解决方案', icon: '📘' },
  { value: `${Array.isArray(cases) ? cases.length : 0}+`, label: '最新入库案例', note: '后续自动持续增加', icon: '🛡️' }
]

const emergencySteps = [
  '保持冷静，立即沟通：先联系家人，了解具体情况，阻止进一步操作。',
  '停止转账，保留证据：立即停止所有转账操作，保存聊天记录、转账凭证。',
  '联系银行，尝试止付：尽快联系银行客服，申请止付或冻结相关账户。',
  '报警求助：拨打 110 报警，提供证据，配合警方调查处理。'
]
</script>

<template>
  <div class="home-page">
    <section class="home-page__hero">
      <div class="home-page__hero-copy">
        <h1>保护父母，<br>从了解开始</h1>
        <p>
          专注老年人防诈骗的知识库与实践指南，
          帮助子女识别骗局、预防风险、及时应对。
        </p>

        <div class="home-page__trust">
          <div class="home-page__trust-item">
            <span>🛡️</span>
            <div>
              <strong>权威可靠</strong>
              <small>内容专业，持续更新</small>
            </div>
          </div>
          <div class="home-page__trust-item">
            <span>💙</span>
            <div>
              <strong>用心守护</strong>
              <small>实用易懂，陪伴父母</small>
            </div>
          </div>
        </div>
      </div>

      <div class="home-page__hero-stats">
        <div class="home-page__stat-grid">
          <article v-for="item in stats" :key="item.label" class="home-page__stat-item">
            <span class="home-page__stat-icon">{{ item.icon }}</span>
            <strong>{{ item.value }}</strong>
            <span>{{ item.label }}</span>
            <small>{{ item.note }}</small>
          </article>
        </div>
        <div class="home-page__hero-note">
          本站内容仅供学习参考，遇到紧急情况请立即采取应对措施或报警。
        </div>
      </div>
    </section>

    <section class="home-page__quick">
      <div class="home-page__quick-label">
        <h2>快速入口</h2>
        <p>常用功能，一键直达</p>
      </div>

      <a
        v-for="item in quickLinks"
        :key="item.title"
        :href="item.href"
        class="home-page__quick-card"
        :class="`is-${item.accent}`"
      >
        <div class="home-page__quick-icon">{{ item.icon }}</div>
        <div class="home-page__quick-body">
          <strong>{{ item.title }}</strong>
          <span>{{ item.description }}</span>
        </div>
        <div class="home-page__quick-arrow">›</div>
      </a>
    </section>

    <section class="home-page__content">
      <div class="home-page__cases">
        <div class="home-page__section-head">
          <h2>最新案例</h2>
          <a href="/cases/latest">查看更多案例 ›</a>
        </div>

        <div class="home-page__case-grid">
          <a
            v-for="item in latestCases"
            :key="item.id"
            :href="item.href"
            class="home-page__case-card"
          >
            <em>{{ item.tag }}</em>
            <h3>{{ item.title }}</h3>
            <p>{{ item.summary }}</p>
            <div class="home-page__case-meta">
              <span>{{ item.meta }}</span>
              <span>{{ item.date }}</span>
            </div>
            <strong>查看详情 ›</strong>
          </a>
        </div>
      </div>

      <aside class="home-page__solution">
        <div class="home-page__section-head is-tight">
          <h2>快速解决方案</h2>
          <span>如果家人正在被诈骗</span>
        </div>

        <ol class="home-page__steps">
          <li v-for="(item, index) in emergencySteps" :key="item">
            <span class="home-page__step-no">{{ index + 1 }}</span>
            <div>{{ item }}</div>
          </li>
        </ol>

        <a href="/emergency" class="home-page__emergency-button">立即查看完整处理指南</a>
        <p class="home-page__emergency-tip">如情况紧急，请第一时间报警，争取挽回损失。</p>
      </aside>
    </section>

    <section class="home-page__footer-strip">
      <strong>防骗提醒：</strong>
      <span>不轻信、不透露、不转账，守护父母的每一分钱。</span>
      <div class="home-page__footer-tags">
        <span>内容专业</span>
        <span>更新及时</span>
        <span>永久免费</span>
        <span>隐私保护</span>
      </div>
    </section>
  </div>
</template>

<style scoped>
:global(.VPDoc) {
  padding: 0 !important;
}

:global(.VPDoc .container),
:global(.VPDoc .content),
:global(.VPDoc .content-container) {
  max-width: 100% !important;
}

:global(.VPDoc .vp-doc) {
  max-width: 100% !important;
}

.home-page {
  width: min(100%, 1280px);
  margin: 0 auto;
  padding: 1.25rem 1.25rem 2rem;
  color: #1f2a44;
}

.home-page__hero {
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(540px, 1fr);
  gap: 1.5rem;
  align-items: stretch;
}

.home-page__hero-copy,
.home-page__hero-stats,
.home-page__quick,
.home-page__cases,
.home-page__solution,
.home-page__footer-strip {
  border: 1px solid #d9e5ff;
  border-radius: 24px;
  background: #fff;
  box-shadow: 0 10px 28px rgba(44, 73, 138, 0.06);
}

.home-page__hero-copy {
  padding: 2rem 2rem 1.75rem;
}

.home-page__hero-copy h1 {
  margin: 0;
  font-size: clamp(3rem, 5vw, 4.6rem);
  line-height: 1.05;
  letter-spacing: -0.04em;
  color: #1d3566;
}

.home-page__hero-copy p {
  margin: 1.1rem 0 1.5rem;
  font-size: 1.22rem;
  line-height: 1.8;
  color: #6a7489;
}

.home-page__trust {
  display: flex;
  gap: 1.2rem;
  flex-wrap: wrap;
}

.home-page__trust-item {
  display: flex;
  align-items: center;
  gap: 0.7rem;
}

.home-page__trust-item span {
  font-size: 1.6rem;
}

.home-page__trust-item strong {
  display: block;
  font-size: 0.98rem;
  color: #2b4270;
}

.home-page__trust-item small {
  display: block;
  margin-top: 0.15rem;
  color: #6d7891;
}

.home-page__hero-stats {
  padding: 1.55rem 1.45rem;
  background:
    radial-gradient(circle at top right, rgba(104, 154, 255, 0.08), transparent 36%),
    linear-gradient(180deg, #ffffff, #f8fbff);
}

.home-page__stat-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0;
}

.home-page__stat-item {
  padding: 0.65rem 1rem 1rem;
  text-align: center;
  border-right: 1px solid #e3ecff;
}

.home-page__stat-item:last-child {
  border-right: 0;
}

.home-page__stat-icon {
  display: block;
  font-size: 1.7rem;
  margin-bottom: 0.55rem;
}

.home-page__stat-item strong {
  display: block;
  color: #3478f6;
  font-size: clamp(2rem, 3vw, 3rem);
  line-height: 1;
}

.home-page__stat-item span:not(.home-page__stat-icon) {
  display: block;
  margin-top: 0.45rem;
  font-weight: 700;
  color: #2b416c;
}

.home-page__stat-item small {
  display: block;
  margin-top: 0.2rem;
  color: #6e7a95;
  line-height: 1.5;
}

.home-page__hero-note {
  margin-top: 1.2rem;
  padding-top: 1rem;
  border-top: 1px solid #dce8ff;
  text-align: center;
  color: #4a74d0;
  font-weight: 600;
}

.home-page__quick {
  display: grid;
  grid-template-columns: 180px repeat(4, minmax(0, 1fr));
  gap: 0.8rem;
  padding: 0.8rem;
  margin-top: 1rem;
}

.home-page__quick-label {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 1rem 1.1rem;
}

.home-page__quick-label h2,
.home-page__section-head h2 {
  margin: 0;
  font-size: 2rem;
  color: #233e73;
}

.home-page__quick-label p {
  margin: 0.35rem 0 0;
  color: #7a8498;
}

.home-page__quick-card {
  display: flex;
  align-items: center;
  gap: 0.9rem;
  padding: 1rem;
  border: 1px solid #e2ebff;
  border-radius: 18px;
  background: #fff;
  text-decoration: none;
  color: inherit;
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}

.home-page__quick-card:hover,
.home-page__case-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(58, 87, 151, 0.09);
  border-color: #c9dbff;
}

.home-page__quick-icon {
  display: grid;
  place-items: center;
  width: 56px;
  height: 56px;
  border-radius: 14px;
  font-size: 1.7rem;
  color: #fff;
}

.is-blue .home-page__quick-icon { background: linear-gradient(180deg, #4e86f4, #356be4); }
.is-green .home-page__quick-icon { background: linear-gradient(180deg, #42caa6, #2ca98d); }
.is-orange .home-page__quick-icon { background: linear-gradient(180deg, #ffb03a, #ff8c1f); }
.is-purple .home-page__quick-icon { background: linear-gradient(180deg, #7c70ff, #6553ef); }

.home-page__quick-body strong {
  display: block;
  font-size: 1.1rem;
  color: #273f72;
}

.home-page__quick-body span {
  display: block;
  margin-top: 0.28rem;
  color: #7a869c;
}

.home-page__quick-arrow {
  margin-left: auto;
  color: #334155;
  font-size: 1.8rem;
}

.home-page__content {
  display: grid;
  grid-template-columns: minmax(0, 1.7fr) minmax(340px, 0.95fr);
  gap: 1rem;
  margin-top: 1rem;
}

.home-page__cases,
.home-page__solution {
  padding: 1rem;
}

.home-page__section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 0.9rem;
}

.home-page__section-head a,
.home-page__section-head span {
  color: #4c77db;
  font-weight: 600;
  text-decoration: none;
}

.home-page__section-head.is-tight span {
  color: #ff6f1f;
}

.home-page__case-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.9rem;
}

.home-page__case-card {
  display: block;
  padding: 1rem;
  border: 1px solid #e4ecff;
  border-radius: 18px;
  text-decoration: none;
  color: inherit;
  background: linear-gradient(180deg, #ffffff, #fbfdff);
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}

.home-page__case-card em {
  display: inline-flex;
  padding: 0.22rem 0.5rem;
  border-radius: 999px;
  background: #fff2e7;
  color: #ff8b2b;
  font-style: normal;
  font-size: 0.8rem;
  font-weight: 700;
}

.home-page__case-card h3 {
  margin: 0.75rem 0 0.55rem;
  font-size: 1.28rem;
  line-height: 1.4;
  color: #253f71;
}

.home-page__case-card p {
  margin: 0;
  min-height: 96px;
  color: #6d7890;
  line-height: 1.75;
}

.home-page__case-meta {
  display: flex;
  justify-content: space-between;
  gap: 0.8rem;
  margin-top: 0.95rem;
  color: #8a93a6;
  font-size: 0.9rem;
}

.home-page__case-card strong {
  display: inline-block;
  margin-top: 0.9rem;
  color: #3478f6;
}

.home-page__solution {
  background:
    linear-gradient(180deg, #fffaf5, #fff);
  border-color: #ffd9bf;
}

.home-page__steps {
  margin: 0;
  padding: 0;
  list-style: none;
}

.home-page__steps li {
  display: grid;
  grid-template-columns: 34px 1fr;
  gap: 0.75rem;
  align-items: start;
  padding: 0.72rem 0;
  border-bottom: 1px solid #ffe7d5;
  color: #5c6375;
  line-height: 1.7;
}

.home-page__steps li:last-child {
  border-bottom: 0;
}

.home-page__step-no {
  display: grid;
  place-items: center;
  width: 30px;
  height: 30px;
  border-radius: 999px;
  background: linear-gradient(180deg, #ff9c2b, #ff7a1d);
  color: #fff;
  font-weight: 800;
}

.home-page__emergency-button {
  display: block;
  margin-top: 1rem;
  padding: 0.92rem 1rem;
  border-radius: 14px;
  background: linear-gradient(180deg, #ff922b, #ff6f1f);
  color: #fff;
  text-align: center;
  text-decoration: none;
  font-weight: 800;
}

.home-page__emergency-tip {
  margin: 0.8rem 0 0;
  color: #8c6f5a;
  text-align: center;
}

.home-page__footer-strip {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.2rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}

.home-page__footer-strip strong {
  color: #2f6de0;
}

.home-page__footer-strip > span {
  color: #546174;
}

.home-page__footer-tags {
  display: flex;
  gap: 1rem;
  margin-left: auto;
  flex-wrap: wrap;
  color: #6883bf;
}

@media (max-width: 1200px) {
  .home-page__hero,
  .home-page__content {
    grid-template-columns: 1fr;
  }

  .home-page__quick {
    grid-template-columns: 1fr 1fr;
  }

  .home-page__quick-label {
    grid-column: 1 / -1;
  }
}

@media (max-width: 960px) {
  .home-page__stat-grid,
  .home-page__case-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 720px) {
  .home-page {
    padding: 0.5rem 0.9rem 1.5rem;
  }

  .home-page__hero-copy,
  .home-page__hero-stats,
  .home-page__quick,
  .home-page__cases,
  .home-page__solution,
  .home-page__footer-strip {
    border-radius: 18px;
  }

  .home-page__quick,
  .home-page__stat-grid,
  .home-page__case-grid {
    grid-template-columns: 1fr;
  }

  .home-page__stat-item {
    border-right: 0;
    border-bottom: 1px solid #e3ecff;
  }

  .home-page__stat-item:last-child {
    border-bottom: 0;
  }

  .home-page__case-card p {
    min-height: auto;
  }

  .home-page__footer-tags {
    margin-left: 0;
  }
}
</style>
