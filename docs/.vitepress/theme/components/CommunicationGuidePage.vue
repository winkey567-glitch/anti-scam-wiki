<script setup>
const doNotSay = [
  '你怎么这么容易被骗？',
  '我早就说过不要接陌生电话。',
  '这都看不出来，你也太糊涂了。'
]

const shouldSay = [
  '先别着急，我们一起核实。',
  '谢谢你第一时间告诉我，这很重要。',
  '不是你笨，是骗子专门研究怎么让人上当。'
]

const scenarios = [
  {
    title: '平时做预防提醒',
    wrong: '最近骗子很多，你别乱点。',
    right: '最近有一种新骗局，专门冒充客服退款。以后你遇到退款、验证码、共享屏幕，先发我看看。'
  },
  {
    title: '家人已经接触到可疑信息',
    wrong: '我就知道你又会信。',
    right: '你先把这个消息发给我，我帮你看是真是假，现在骗局做得很像真的。'
  },
  {
    title: '家人已经被骗',
    wrong: '你怎么这么糊涂，损失了多少？',
    right: '先别自责，我们先处理问题。你把刚才发生的经过告诉我，我来陪你一起处理。'
  }
]
</script>

<template>
  <div class="page-shell">
    <section class="page-hero">
      <div>
        <span class="page-badge">沟通话术</span>
        <h1>先稳住父母情绪，再谈防骗规则</h1>
        <p>很多家庭不是缺提醒，而是提醒方式一开始就错了。好的沟通不是批评，而是让父母愿意继续把情况告诉你。</p>
      </div>
      <div class="hero-side">
        <strong>这页最重要的原则</strong>
        <ul>
          <li>先安抚，再处理</li>
          <li>多说“我们”，少说“你怎么”</li>
          <li>先核实，再讲道理</li>
        </ul>
      </div>
    </section>

    <section class="grid-two">
      <article class="card-block bad">
        <div class="section-head"><h2>尽量不要这样说</h2></div>
        <ul class="bullet-list">
          <li v-for="item in doNotSay" :key="item">{{ item }}</li>
        </ul>
      </article>
      <article class="card-block good">
        <div class="section-head"><h2>更建议这样说</h2></div>
        <ul class="bullet-list">
          <li v-for="item in shouldSay" :key="item">{{ item }}</li>
        </ul>
      </article>
    </section>

    <section class="card-block">
      <div class="section-head"><h2>常见场景话术</h2></div>
      <div class="scenario-list">
        <article v-for="item in scenarios" :key="item.title" class="scenario-row">
          <h3>{{ item.title }}</h3>
          <p><strong>不建议：</strong>{{ item.wrong }}</p>
          <p><strong>更建议：</strong>{{ item.right }}</p>
        </article>
      </div>
    </section>
  </div>
</template>

<style scoped>
.page-shell { width:min(100%,1240px); margin:0 auto; padding:1.25rem 1.25rem 2rem; }
.page-hero,.card-block { border:1px solid #dce7ff; border-radius:24px; background:#fff; box-shadow:0 10px 28px rgba(44,73,138,.06); }
.page-hero { display:grid; grid-template-columns:minmax(0,1.45fr) 320px; gap:1rem; padding:1.5rem; }
.page-badge { display:inline-flex; padding:.3rem .65rem; border-radius:999px; background:#edf4ff; color:#3777f4; font-size:.82rem; font-weight:700; }
.page-hero h1 { margin:.9rem 0 .8rem; font-size:clamp(2.2rem,4vw,3.4rem); line-height:1.15; color:#213d72; }
.page-hero p,.hero-side li,.bullet-list li,.scenario-row p { color:#69758d; line-height:1.8; }
.hero-side { padding:1rem 1.1rem; border-radius:18px; background:linear-gradient(180deg,#f7fbff,#fff); border:1px solid #dce8ff; }
.hero-side strong,.section-head h2,.scenario-row h3 { color:#244073; }
.hero-side ul,.bullet-list { margin:.8rem 0 0; padding-left:1.15rem; }
.grid-two { display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-top:1rem; }
.card-block { margin-top:1rem; padding:1.1rem; }
.bad { border-color:#ffd9d1; background:linear-gradient(180deg,#fff7f5,#fff); }
.good { border-color:#d9f0df; background:linear-gradient(180deg,#f8fff9,#fff); }
.section-head h2 { margin:0; font-size:1.8rem; }
.scenario-list { display:grid; gap:.8rem; margin-top:.9rem; }
.scenario-row { padding:1rem; border:1px solid #e4ebff; border-radius:18px; background:linear-gradient(180deg,#fff,#fbfdff); }
.scenario-row h3 { margin:0 0 .45rem; }
.scenario-row p { margin:.3rem 0 0; }
@media (max-width: 960px) { .page-hero,.grid-two { grid-template-columns:1fr; } }
@media (max-width: 720px) { .page-shell { padding:.75rem .9rem 1.5rem; } }
</style>
