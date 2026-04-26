<script setup>
const scenarioLinks = [
  ['冒充客服退款', '/scenarios/fake-customer-service'],
  ['冒充公检法', '/scenarios/fake-police'],
  ['保健品诈骗', '/scenarios/health-products'],
  ['中奖免费送礼', '/scenarios/free-gift'],
  ['养老投资', '/scenarios/investment'],
  ['情感诈骗', '/scenarios/romance']
]

const contributionPoints = [
  '诈骗类型',
  '目标人群',
  '发生经过',
  '危险信号',
  '止损方式',
  '复盘教训'
]
</script>

<template>
  <div class="page-shell">
    <section class="page-hero">
      <div>
        <span class="page-badge">案例库入口</span>
        <h1>优先看真实案例，最容易让家人理解骗局套路</h1>
        <p>这里是站点里最适合“带着家人一起看”的区域。后续案例会持续自动生成并沉淀到案例库中。</p>
      </div>
      <div class="hero-side">
        <strong>现在可以直接进入</strong>
        <ul>
          <li><a href="/cases/latest">最新案例汇总</a></li>
          <li><a href="/cases/generated/">自动生成索引</a></li>
          <li><a href="/scenarios/">按诈骗场景查找</a></li>
        </ul>
      </div>
    </section>

    <section class="card-block grid-two">
      <article class="sub-card">
        <h2>先从这里看</h2>
        <div class="entry-list">
          <a href="/cases/latest">最新案例汇总 ›</a>
          <a href="/cases/generated/">自动生成案例页 ›</a>
          <a href="/profiles/">按父母类型查找 ›</a>
        </div>
      </article>

      <article class="sub-card">
        <h2>还没有足够案例时</h2>
        <div class="pill-grid">
          <a v-for="[name, href] in scenarioLinks" :key="name" :href="href" class="pill-link">{{ name }}</a>
        </div>
      </article>
    </section>

    <section class="card-block">
      <div class="section-head"><h2>如果你想补充案例</h2></div>
      <div class="tips-box">
        <strong>建议至少包含这些信息</strong>
        <ul>
          <li v-for="item in contributionPoints" :key="item">{{ item }}</li>
        </ul>
      </div>
      <p class="note">所有案例都建议先脱敏，再补充到仓库。遇到正在发生的诈骗，请先报警或联系 96110。</p>
    </section>
  </div>
</template>

<style scoped>
.page-shell { width:min(100%,1240px); margin:0 auto; padding:1.25rem 1.25rem 2rem; }
.page-hero,.card-block { border:1px solid #dce7ff; border-radius:24px; background:#fff; box-shadow:0 10px 28px rgba(44,73,138,.06); }
.page-hero { display:grid; grid-template-columns:minmax(0,1.45fr) 320px; gap:1rem; padding:1.5rem; }
.page-badge { display:inline-flex; padding:.3rem .65rem; border-radius:999px; background:#edf4ff; color:#3777f4; font-size:.82rem; font-weight:700; }
.page-hero h1 { margin:.9rem 0 .8rem; font-size:clamp(2.2rem,4vw,3.4rem); line-height:1.15; color:#213d72; }
.page-hero p,.note,.hero-side li,.tips-box li { color:#69758d; line-height:1.8; }
.hero-side { padding:1rem 1.1rem; border-radius:18px; background:linear-gradient(180deg,#f7fbff,#fff); border:1px solid #dce8ff; }
.hero-side strong,.sub-card h2,.section-head h2,.tips-box strong { color:#244073; }
.hero-side ul,.tips-box ul { margin:.8rem 0 0; padding-left:1.15rem; }
.hero-side a,.entry-list a,.pill-link { color:#4d78da; text-decoration:none; font-weight:600; }
.card-block { margin-top:1rem; padding:1.1rem; }
.grid-two { display:grid; grid-template-columns:1fr 1fr; gap:1rem; }
.sub-card { padding:1rem; border:1px solid #e4ebff; border-radius:18px; background:linear-gradient(180deg,#fff,#fbfdff); }
.entry-list { display:grid; gap:.75rem; margin-top:.8rem; }
.pill-grid { display:flex; flex-wrap:wrap; gap:.75rem; margin-top:.8rem; }
.pill-link { padding:.55rem .8rem; border-radius:999px; border:1px solid #dce7ff; background:#fff; }
.tips-box { padding:1rem; border:1px solid #dfe8ff; border-radius:16px; background:#fbfdff; }
@media (max-width: 960px) { .page-hero,.grid-two { grid-template-columns:1fr; } }
@media (max-width: 720px) { .page-shell { padding:.75rem .9rem 1.5rem; } }
</style>
