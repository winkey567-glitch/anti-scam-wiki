<script setup>
import { withBase } from 'vitepress'

const phoneSecurity = [
  '关闭未知来源应用安装',
  '关闭自动下载彩信或未知附件',
  '开启系统骚扰拦截与反诈提醒',
  '为手机设置不简单的锁屏密码'
]

const paymentSecurity = [
  '设置支付单笔和单日限额',
  '关闭免密支付',
  '关闭不需要的自动续费',
  '不要把大额银行卡直接绑定到常用支付账户'
]

const familyRules = [
  '验证码绝不告诉任何人',
  '任何转账都先打电话确认',
  '陌生链接不点，陌生 App 不装',
  '大额消费先和子女确认',
  '任何要求保密的来电默认高风险'
]

const weeklyChecks = [
  '问一次最近有没有可疑电话或短信',
  '看一次手机里有没有陌生 App',
  '看一次银行卡或支付提醒是否异常'
]
</script>

<template>
  <div class="page-shell">
    <section class="page-hero">
      <div>
        <span class="page-badge">家庭清单</span>
        <h1>按清单一步步配置，比临时提醒更有效</h1>
        <p>如果你想真正降低家人被骗概率，这页最适合直接照着做，也适合打印后贴在家里。</p>
      </div>
      <div class="hero-side">
        <strong>使用方法</strong>
        <ol>
          <li>先做手机和支付安全配置</li>
          <li>再和父母约定 3 到 5 条家庭规则</li>
          <li>每周做一次简单复查</li>
        </ol>
      </div>
    </section>

    <section class="grid-three">
      <article class="card-block list-card">
        <h2>手机安全</h2>
        <ul>
          <li v-for="item in phoneSecurity" :key="item">{{ item }}</li>
        </ul>
      </article>

      <article class="card-block list-card">
        <h2>支付安全</h2>
        <ul>
          <li v-for="item in paymentSecurity" :key="item">{{ item }}</li>
        </ul>
      </article>

      <article class="card-block list-card highlight">
        <h2>家庭规则</h2>
        <ul>
          <li v-for="item in familyRules" :key="item">{{ item }}</li>
        </ul>
      </article>
    </section>

    <section class="card-block">
      <div class="section-head"><h2>每周复查一次就够了</h2></div>
      <div class="weekly-grid">
        <article v-for="(item, index) in weeklyChecks" :key="item" class="weekly-item">
          <span>{{ index + 1 }}</span>
          <p>{{ item }}</p>
        </article>
      </div>
      <a class="primary-button" :href="withBase('/emergency')">如果已经出事，先看应急处理指南</a>
    </section>
  </div>
</template>

<style scoped>
.page-shell { width:min(100%,1240px); margin:0 auto; padding:1.25rem 1.25rem 2rem; }
.page-hero,.card-block { border:1px solid #dce7ff; border-radius:24px; background:#fff; box-shadow:0 10px 28px rgba(44,73,138,.06); }
.page-hero { display:grid; grid-template-columns:minmax(0,1.45fr) 320px; gap:1rem; padding:1.5rem; }
.page-badge { display:inline-flex; padding:.3rem .65rem; border-radius:999px; background:#edf4ff; color:#3777f4; font-size:.82rem; font-weight:700; }
.page-hero h1 { margin:.9rem 0 .8rem; font-size:clamp(2.2rem,4vw,3.4rem); line-height:1.15; color:#213d72; }
.page-hero p,.hero-side li,.list-card li,.weekly-item p { color:#69758d; line-height:1.8; }
.hero-side { padding:1rem 1.1rem; border-radius:18px; background:linear-gradient(180deg,#f7fbff,#fff); border:1px solid #dce8ff; }
.hero-side strong,.list-card h2,.section-head h2 { color:#244073; }
.hero-side ol,.list-card ul { margin:.8rem 0 0; padding-left:1.15rem; }
.grid-three { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:1rem; margin-top:1rem; }
.card-block { margin-top:1rem; padding:1.1rem; }
.list-card h2 { margin:0; font-size:1.6rem; }
.list-card ul { margin-top:.9rem; }
.highlight { background:linear-gradient(180deg,#fff9f2,#fff); border-color:#ffd8bc; }
.section-head h2 { margin:0; font-size:1.8rem; }
.weekly-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:.85rem; margin-top:.9rem; }
.weekly-item { padding:1rem; border:1px solid #e4ebff; border-radius:18px; background:linear-gradient(180deg,#fff,#fbfdff); }
.weekly-item span { display:inline-grid; place-items:center; width:32px; height:32px; border-radius:999px; background:#edf4ff; color:#3478f6; font-weight:800; }
.weekly-item p { margin:.7rem 0 0; }
.primary-button { display:block; margin-top:1rem; padding:.92rem 1rem; border-radius:14px; background:linear-gradient(180deg,#4d87f4,#356be4); color:#fff; text-align:center; text-decoration:none; font-weight:700; }
@media (max-width: 960px) { .page-hero,.grid-three,.weekly-grid { grid-template-columns:1fr; } }
@media (max-width: 720px) { .page-shell { padding:.75rem .9rem 1.5rem; } }
</style>
