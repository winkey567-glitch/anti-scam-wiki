<script setup>
import { computed } from 'vue'
import { withBase } from 'vitepress'
import { profileContent } from '../content/profiles'

const props = defineProps({
  slug: { type: String, required: true }
})

const content = computed(() => profileContent[props.slug])
</script>

<template>
  <div v-if="content" class="page-shell">
    <section class="page-hero">
      <div>
        <span class="page-badge">{{ content.badge }}</span>
        <h1>{{ content.title }}</h1>
        <p>{{ content.summary }}</p>
      </div>
      <div class="hero-side">
        <strong>最适合先提醒的一句话</strong>
        <p>{{ content.talk }}</p>
      </div>
    </section>

    <section class="grid-three">
      <article class="card-block">
        <div class="section-head"><h2>典型特征</h2></div>
        <ul class="bullet-list">
          <li v-for="item in content.signals" :key="item">{{ item }}</li>
        </ul>
      </article>
      <article class="card-block">
        <div class="section-head"><h2>容易中的骗局</h2></div>
        <ul class="bullet-list">
          <li v-for="item in content.scams" :key="item">{{ item }}</li>
        </ul>
      </article>
      <article class="card-block">
        <div class="section-head"><h2>优先做的事</h2></div>
        <ul class="bullet-list">
          <li v-for="item in content.actions" :key="item">{{ item }}</li>
        </ul>
      </article>
    </section>

    <section class="card-block next-links">
      <div class="section-head"><h2>对应骗局场景</h2></div>
      <div class="link-row">
        <a :href="withBase(content.scenarioLink)">查看更像的诈骗场景 ›</a>
        <a :href="withBase('/guide/communication')">查看沟通话术 ›</a>
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
.page-hero p,.hero-side p,.bullet-list li { color:#69758d; line-height:1.8; }
.hero-side { padding:1rem 1.1rem; border-radius:18px; background:linear-gradient(180deg,#f7fbff,#fff); border:1px solid #dce8ff; }
.hero-side strong,.section-head h2 { color:#244073; }
.grid-three { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:1rem; margin-top:1rem; }
.card-block { padding:1.1rem; }
.section-head h2 { margin:0; font-size:1.8rem; }
.bullet-list { margin:.9rem 0 0; padding-left:1.15rem; }
.next-links { margin-top:1rem; }
.link-row { display:flex; gap:.8rem; flex-wrap:wrap; margin-top:.9rem; }
.link-row a { padding:.58rem .85rem; border-radius:999px; border:1px solid #dbe7ff; color:#4d78da; text-decoration:none; font-weight:600; }
@media (max-width: 960px) { .page-hero,.grid-three { grid-template-columns:1fr; } }
@media (max-width: 720px) { .page-shell { padding:.75rem .9rem 1.5rem; } }
</style>
