<script setup>
import { withBase } from 'vitepress'

const profiles = [
  ['孤独空巢型', '独居、缺陪伴、愿意和陌生人长时间聊天，容易被情感与关怀打动。', '情感诈骗、上门推销、假干儿子干女儿', withBase('/profiles/lonely')],
  ['健康焦虑型', '怕生病、爱养生、容易相信专家讲座和特效保健品。', '保健品诈骗、理疗仪器、虚假名医', withBase('/profiles/health-anxiety')],
  ['贪小便宜型', '节俭、喜欢领赠品、容易被免费和返利吸引。', '中奖送礼、扫码领福利、刷单返利', withBase('/profiles/greedy')],
  ['盲目投资型', '想让钱生钱，容易被高回报项目和熟人推荐吸引。', '养老理财、虚拟币、内部项目', withBase('/profiles/investor')],
  ['认知衰退型', '记忆力下降，辨别能力减弱，容易在压力下照做。', '冒充公检法、转账诈骗、验证码骗局', withBase('/profiles/cognitive')],
  ['热衷社交型', '爱进群、爱社交、爱旅游，容易被群体氛围带动。', '社群团购、旅游购物、熟人荐货', withBase('/profiles/social')],
  ['技术懵懂型', '不熟悉手机和支付操作，容易点错、扫错、装错。', '钓鱼链接、假 App、共享屏幕', withBase('/profiles/tech-illiterate')]
]
</script>

<template>
  <div class="page-shell">
    <section class="page-hero">
      <div>
        <span class="page-badge">人群分类</span>
        <h1>先理解父母的特点，再做更有效的防骗提醒</h1>
        <p>不同父母容易被不同话术打动。比起反复说“别被骗”，更有用的是找到最容易击中的风险点。</p>
      </div>
      <div class="hero-side">
        <strong>怎么用这页</strong>
        <ol>
          <li>先找最像父母的类型</li>
          <li>再看最容易中的骗局</li>
          <li>最后只重点提醒 2 到 3 条规则</li>
        </ol>
      </div>
    </section>

    <section class="card-block">
      <div class="section-head"><h2>七类高风险画像</h2><a :href="withBase('/quiz')">先做 3 分钟测试 ›</a></div>
      <div class="profile-grid">
        <a v-for="[name, desc, scams, href] in profiles" :key="name" :href="href" class="profile-card">
          <h3>{{ name }}</h3>
          <p>{{ desc }}</p>
          <span>容易中的骗局：{{ scams }}</span>
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
.section-head { display:flex; align-items:center; justify-content:space-between; gap:1rem; margin-bottom:.85rem; }
.section-head h2 { margin:0; color:#223d72; font-size:1.8rem; }
.section-head a { color:#4e78db; text-decoration:none; font-weight:600; }
.profile-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.9rem; margin-top:.9rem; }
.profile-card { display:block; padding:1rem; border:1px solid #e4ebff; border-radius:18px; background:linear-gradient(180deg,#fff,#fbfdff); text-decoration:none; color:inherit; transition:.18s ease; }
.profile-card:hover { transform:translateY(-2px); box-shadow:0 12px 24px rgba(58,87,151,.09); border-color:#c9dbff; }
.profile-card h3 { margin:0 0 .45rem; color:#254074; }
.profile-card p { margin:0; color:#6d7890; line-height:1.75; }
.profile-card span { display:block; margin-top:.75rem; color:#4b78db; font-weight:600; }
@media (max-width: 960px) { .page-hero,.profile-grid { grid-template-columns:1fr; } }
@media (max-width: 720px) { .page-shell { padding:.75rem .9rem 1.5rem; } }
</style>
