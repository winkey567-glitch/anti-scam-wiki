<script setup>
import { withBase } from 'vitepress'

const guides = [
  {
    title: '沟通话术',
    description: '不吓人、不争执，先让父母愿意听你说。',
    href: withBase('/guide/communication'),
    tone: 'blue'
  },
  {
    title: '情绪支持',
    description: '已经被骗后，先稳住情绪，再处理损失和复盘。',
    href: withBase('/guide/emotional'),
    tone: 'orange'
  },
  {
    title: '家庭清单',
    description: '按清单一步步做手机、支付和家庭规则配置。',
    href: withBase('/guide/checklist'),
    tone: 'green'
  },
  {
    title: '报案材料整理',
    description: '把时间线、账号、证据目录快速整理成给警方的草稿。',
    href: withBase('/guide/report-helper'),
    tone: 'blue'
  },
  {
    title: '常见问题',
    description: '家属最常问的事情，集中快速看完。',
    href: withBase('/guide/faq'),
    tone: 'blue'
  }
]
</script>

<template>
  <div class="page-shell">
    <section class="page-hero">
      <div>
        <span class="page-badge">指南中心</span>
        <h1>先选对一页，再陪父母慢慢建立防骗习惯</h1>
        <p>这里集中放“最适合拿来直接用”的内容：怎么沟通、怎么安抚、怎么做家庭配置，以及怎么整理报案材料。</p>
      </div>
      <div class="hero-side">
        <strong>建议顺序</strong>
        <ol>
          <li>先看家庭清单，做好基础配置。</li>
          <li>再看沟通话术，减少对抗。</li>
          <li>遇到损失时回到情绪支持和报案整理页。</li>
        </ol>
      </div>
    </section>

    <section class="guide-grid">
      <a v-for="item in guides" :key="item.title" :href="item.href" class="guide-card" :class="`is-${item.tone}`">
        <h2>{{ item.title }}</h2>
        <p>{{ item.description }}</p>
        <strong>进入页面 →</strong>
      </a>
    </section>
  </div>
</template>

<style scoped>
.page-shell { width:min(100%,1240px); margin:0 auto; padding:1.25rem 1.25rem 2rem; }
.page-hero,.guide-card { border:1px solid #dce7ff; border-radius:24px; background:#fff; box-shadow:0 10px 28px rgba(44,73,138,.06); }
.page-hero { display:grid; grid-template-columns:minmax(0,1.45fr) 320px; gap:1rem; padding:1.5rem; }
.page-badge { display:inline-flex; padding:.3rem .65rem; border-radius:999px; background:#edf4ff; color:#3777f4; font-size:.82rem; font-weight:700; }
.page-hero h1 { margin:.9rem 0 .8rem; font-size:clamp(2.2rem,4vw,3.4rem); line-height:1.15; color:#213d72; }
.page-hero p,.hero-side li,.guide-card p { color:#69758d; line-height:1.8; }
.hero-side { padding:1rem 1.1rem; border-radius:18px; background:linear-gradient(180deg,#f7fbff,#fff); border:1px solid #dce8ff; }
.hero-side strong,.guide-card h2 { color:#244073; }
.hero-side ol { margin:.8rem 0 0; padding-left:1.15rem; }
.guide-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:1rem; margin-top:1rem; }
.guide-card { display:block; padding:1.1rem; text-decoration:none; color:inherit; transition:.18s ease; }
.guide-card:hover { transform:translateY(-2px); box-shadow:0 12px 24px rgba(58,87,151,.09); border-color:#c9dbff; }
.guide-card h2 { margin:0; font-size:1.8rem; }
.guide-card p { margin:.65rem 0 1rem; }
.guide-card strong { color:#4d78da; }
.is-blue { background:linear-gradient(180deg,#fff,#fbfdff); }
.is-orange { background:linear-gradient(180deg,#fffaf4,#fff); border-color:#ffd9bf; }
.is-green { background:linear-gradient(180deg,#f9fff9,#fff); border-color:#d6efdc; }
@media (max-width: 960px) { .page-hero,.guide-grid { grid-template-columns:1fr; } }
@media (max-width: 720px) { .page-shell { padding:.75rem .9rem 1.5rem; } }
</style>
