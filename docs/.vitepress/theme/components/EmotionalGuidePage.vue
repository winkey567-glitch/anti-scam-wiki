<script setup>
const supportPoints = [
  '被骗之后，父母通常先感到羞愧、自责和害怕被责怪。',
  '情绪支持不是“安慰一下”，而是帮助他们恢复基本判断和求助意愿。',
  '越是损失大，越要避免一开始就盘问和批评。'
]

const actions = [
  '先告诉父母：这不是你一个人的问题，我们先一起处理。',
  '先处理账户和报警，再慢慢复盘，不要边止损边追责。',
  '短时间内多联系，避免老人陷入反复自责和二次被劝骗。',
  '如果情绪波动很大，先休息，再决定是否继续沟通细节。'
]

const avoid = [
  '当场反复追问“到底为什么会信”',
  '马上在亲戚群里公开讨论',
  '用“你不听我的才这样”进行责备',
  '逼着老人立刻回忆所有细节'
]
</script>

<template>
  <div class="page-shell">
    <section class="page-hero">
      <div>
        <span class="page-badge">情绪支持</span>
        <h1>老人被骗后，先让他敢继续说下去</h1>
        <p>很多损失之所以扩大，不是因为第一次被骗，而是因为被骗后太羞愧、不敢再告诉家人，结果继续被骗子操控。</p>
      </div>
      <div class="hero-side">
        <strong>优先顺序</strong>
        <ol>
          <li>先止损</li>
          <li>再安抚</li>
          <li>最后复盘</li>
        </ol>
      </div>
    </section>

    <section class="grid-two">
      <article class="card-block">
        <div class="section-head"><h2>先理解这几点</h2></div>
        <ul class="bullet-list">
          <li v-for="item in supportPoints" :key="item">{{ item }}</li>
        </ul>
      </article>
      <article class="card-block warning">
        <div class="section-head"><h2>尽量避免</h2></div>
        <ul class="bullet-list">
          <li v-for="item in avoid" :key="item">{{ item }}</li>
        </ul>
      </article>
    </section>

    <section class="card-block">
      <div class="section-head"><h2>更稳妥的做法</h2></div>
      <ol class="number-list">
        <li v-for="item in actions" :key="item">{{ item }}</li>
      </ol>
    </section>
  </div>
</template>

<style scoped>
.page-shell { width:min(100%,1240px); margin:0 auto; padding:1.25rem 1.25rem 2rem; }
.page-hero,.card-block { border:1px solid #dce7ff; border-radius:24px; background:#fff; box-shadow:0 10px 28px rgba(44,73,138,.06); }
.page-hero { display:grid; grid-template-columns:minmax(0,1.45fr) 320px; gap:1rem; padding:1.5rem; }
.page-badge { display:inline-flex; padding:.3rem .65rem; border-radius:999px; background:#edf4ff; color:#3777f4; font-size:.82rem; font-weight:700; }
.page-hero h1 { margin:.9rem 0 .8rem; font-size:clamp(2.2rem,4vw,3.4rem); line-height:1.15; color:#213d72; }
.page-hero p,.hero-side li,.bullet-list li,.number-list li { color:#69758d; line-height:1.8; }
.hero-side { padding:1rem 1.1rem; border-radius:18px; background:linear-gradient(180deg,#f7fbff,#fff); border:1px solid #dce8ff; }
.hero-side strong,.section-head h2 { color:#244073; }
.hero-side ol,.bullet-list,.number-list { margin:.8rem 0 0; padding-left:1.15rem; }
.grid-two { display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-top:1rem; }
.card-block { margin-top:1rem; padding:1.1rem; }
.warning { border-color:#ffd9d1; background:linear-gradient(180deg,#fff8f6,#fff); }
.section-head h2 { margin:0; font-size:1.8rem; }
@media (max-width: 960px) { .page-hero,.grid-two { grid-template-columns:1fr; } }
@media (max-width: 720px) { .page-shell { padding:.75rem .9rem 1.5rem; } }
</style>
