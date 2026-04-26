<script setup>
const faqs = [
  {
    q: '父母总说“我知道，不会被骗”，还需要怎么提醒？',
    a: '不要直接争辩。更有效的方式是拿一条真实案例和一个具体规则去说，比如“以后凡是说退款、验证码、共享屏幕的，先发我看一下”。'
  },
  {
    q: '如果父母已经被骗，但不愿意报警怎么办？',
    a: '先别逼问原因，先帮他们把损失和证据整理出来。很多老人不是不想报警，而是怕被责怪。先站在同一边，再推动报警。'
  },
  {
    q: '家里最该先配好的 3 个防骗设置是什么？',
    a: '关闭未知来源安装、关闭免密支付、约定任何转账先打电话确认。这 3 条往往比讲很多道理更有效。'
  },
  {
    q: '什么样的骗局最适合直接给父母看案例？',
    a: '退款扣费、保健品、熟人借钱、免费领礼品、投资返利这几类最适合。因为生活感强，父母更容易代入。'
  },
  {
    q: '为什么很多老人明明听过反诈宣传，还是会被骗？',
    a: '因为真正被骗时，打动他们的不是知识点，而是情绪。恐惧、占便宜、急着止损、怕影响征信、想帮家人，都会让人短时间失去判断。'
  },
  {
    q: '我一个人要上班，没法时刻盯着父母，怎么办？',
    a: '靠流程而不是靠盯人。把关键规则固定下来，把联系方式和处理顺序贴在家里，再每周做一次简单复查，效果会比临时提醒更稳。'
  }
]
</script>

<template>
  <div class="page-shell">
    <section class="page-hero">
      <div>
        <span class="page-badge">常见问题</span>
        <h1>把家属最常问的事，先讲明白</h1>
        <p>这页适合你快速找答案，也适合发给家里其他人一起统一做法。</p>
      </div>
    </section>

    <section class="faq-list">
      <article v-for="item in faqs" :key="item.q" class="faq-card">
        <h2>{{ item.q }}</h2>
        <p>{{ item.a }}</p>
      </article>
    </section>
  </div>
</template>

<style scoped>
.page-shell { width:min(100%,1240px); margin:0 auto; padding:1.25rem 1.25rem 2rem; }
.page-hero,.faq-card { border:1px solid #dce7ff; border-radius:24px; background:#fff; box-shadow:0 10px 28px rgba(44,73,138,.06); }
.page-hero { padding:1.5rem; }
.page-badge { display:inline-flex; padding:.3rem .65rem; border-radius:999px; background:#edf4ff; color:#3777f4; font-size:.82rem; font-weight:700; }
.page-hero h1 { margin:.9rem 0 .8rem; font-size:clamp(2.2rem,4vw,3.4rem); line-height:1.15; color:#213d72; }
.page-hero p,.faq-card p { color:#69758d; line-height:1.85; }
.faq-list { display:grid; gap:1rem; margin-top:1rem; }
.faq-card { padding:1.15rem; }
.faq-card h2 { margin:0 0 .55rem; color:#244073; font-size:1.35rem; }
@media (max-width: 720px) { .page-shell { padding:.75rem .9rem 1.5rem; } }
</style>
