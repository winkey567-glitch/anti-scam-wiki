<script setup>
const scenarios = [
  ['冒充客服退款', '快递丢失、商品退款、会员扣费等名义诱导下载 App 或共享屏幕', '网购用户', '/scenarios/fake-customer-service'],
  ['冒充公检法', '用“涉嫌洗钱、账户冻结、安全账户”制造恐慌', '所有家庭', '/scenarios/fake-police'],
  ['保健品诈骗', '用免费体检、养生讲座、特效药收割养老金', '健康焦虑型', '/scenarios/health-products'],
  ['中奖免费送礼', '扫码领礼品、抽奖返现、免费福利引诱操作', '贪小便宜型', '/scenarios/free-gift'],
  ['养老投资', '保本高息、内部项目、熟人荐股和养老理财骗局', '盲目投资型', '/scenarios/investment'],
  ['情感诈骗', '网上交友、嘘寒问暖后借钱或诱导投资', '孤独空巢型', '/scenarios/romance'],
  ['旅游团购', '低价旅行团、强制购物、熟人社群带货', '热衷社交型', '/scenarios/travel'],
  ['AI换脸', '冒充子女或熟人视频通话借钱', '技术懵懂型', '/scenarios/ai-face'],
  ['假冒熟人', '“我出事了”“先借我一笔钱”之类的熟人求助', '所有家庭', '/scenarios/fake-friend'],
  ['刷单返利', '先小额返利，后要求不断垫资', '贪小便宜型', '/scenarios/brushing']
]
</script>

<template>
  <div class="page-shell">
    <section class="page-hero">
      <div>
        <span class="page-badge">场景总览</span>
        <h1>先看骗局类型，再看识别信号和应对策略</h1>
        <p>如果你不确定该从哪里开始，最实用的路径就是先按骗局场景查，再把重点讲给父母听。</p>
      </div>
      <div class="hero-side">
        <strong>建议使用顺序</strong>
        <ol>
          <li>先看是否像家里最近遇到的场景</li>
          <li>再记住骗子最常说的话</li>
          <li>最后把识别信号讲给父母</li>
        </ol>
      </div>
    </section>

    <section class="card-block">
      <div class="section-head"><h2>高发诈骗场景</h2></div>
      <div class="scenario-grid">
        <a v-for="[title, summary, group, href] in scenarios" :key="title" :href="href" class="scenario-card">
          <h3>{{ title }}</h3>
          <p>{{ summary }}</p>
          <span>高风险人群：{{ group }}</span>
        </a>
      </div>
    </section>
  </div>
</template>

<style scoped>
.page-shell { width:min(100%,1240px); margin:0 auto; padding:1.25rem 1.25rem 2rem; }
.page-hero,.card-block { border:1px solid #dce7ff; border-radius:24px; background:#fff; box-shadow:0 10px 28px rgba(44,73,138,.06); }
.page-hero { display:grid; grid-template-columns:minmax(0,1.4fr) 320px; gap:1rem; padding:1.5rem; }
.page-badge { display:inline-flex; padding:.3rem .65rem; border-radius:999px; background:#edf4ff; color:#3777f4; font-size:.82rem; font-weight:700; }
.page-hero h1 { margin:.9rem 0 .8rem; font-size:clamp(2.2rem,4vw,3.4rem); line-height:1.15; color:#213d72; }
.page-hero p { margin:0; color:#69758d; font-size:1.08rem; line-height:1.8; }
.hero-side { padding:1rem 1.1rem; border-radius:18px; background:linear-gradient(180deg,#f7fbff,#fff); border:1px solid #dce8ff; }
.hero-side strong { color:#2e63cf; }
.hero-side ol { margin:.8rem 0 0; padding-left:1.15rem; color:#6a7181; line-height:1.9; }
.card-block { margin-top:1rem; padding:1.1rem; }
.section-head h2 { margin:0; color:#223d72; font-size:1.8rem; }
.scenario-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.9rem; margin-top:.9rem; }
.scenario-card { display:block; padding:1rem; border:1px solid #e4ebff; border-radius:18px; background:linear-gradient(180deg,#fff,#fbfdff); text-decoration:none; color:inherit; transition:.18s ease; }
.scenario-card:hover { transform:translateY(-2px); box-shadow:0 12px 24px rgba(58,87,151,.09); border-color:#c9dbff; }
.scenario-card h3 { margin:0 0 .45rem; color:#254074; }
.scenario-card p { margin:0; color:#6d7890; line-height:1.75; }
.scenario-card span { display:block; margin-top:.75rem; color:#4b78db; font-weight:600; }
@media (max-width: 960px) { .page-hero,.scenario-grid { grid-template-columns:1fr; } }
@media (max-width: 720px) { .page-shell { padding:.75rem .9rem 1.5rem; } }
</style>
