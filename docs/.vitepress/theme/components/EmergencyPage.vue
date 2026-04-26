<script setup>
const steps = [
  {
    title: '立即联系本人',
    detail: '第一时间电话或视频联系家人，确认是否正在转账、报码、共享屏幕。'
  },
  {
    title: '要求立刻停手',
    detail: '明确告诉家人“先别操作”，不要继续输入验证码，不要继续转账。'
  },
  {
    title: '联系银行止付',
    detail: '如果已经涉及转账，马上联系银行、支付宝或微信支付客服，争取止付或冻结。'
  },
  {
    title: '保留全部证据',
    detail: '保存聊天记录、电话号码、转账截图、账户信息和可疑 APP 名称。'
  },
  {
    title: '拨打 96110 或 110',
    detail: '尽快报警并提供证据，越早处理，越有机会挽回损失。'
  }
]

const situations = [
  {
    title: '家人正在通电话',
    action: '反复拨打家人电话，抢占线路；同时联系身边亲友上门阻止。'
  },
  {
    title: '家人正在微信聊天',
    action: '立刻发送“不要转账，这是诈骗”，再打语音或视频打断。'
  },
  {
    title: '已经转账了',
    action: '立刻联系银行止付，并保留转账记录、收款账户和时间。'
  },
  {
    title: '已经下载陌生 APP',
    action: '不要再输入任何信息，卸载 APP，并尽快修改支付密码。'
  },
  {
    title: '已经交出验证码',
    action: '按最高风险处理：先冻结账户，再改密码，再报警。'
  }
]

const calls = [
  ['96110', '反诈专线，优先拨打'],
  ['110', '报警电话'],
  ['95188', '支付宝客服'],
  ['95017', '微信支付客服']
]
</script>

<template>
  <div class="page-shell">
    <section class="page-hero">
      <div>
        <span class="page-badge danger">紧急处理</span>
        <h1>如果家人正在被诈骗，先做这 5 步</h1>
        <p>
          先阻止，后核实，再止付。这个页面只做一件事：
          帮你在最慌的时候快速找到最正确的动作顺序。
        </p>
      </div>
      <div class="hero-side danger">
        <strong>优先顺序</strong>
        <ol>
          <li>先联系家人</li>
          <li>再要求停手</li>
          <li>再联系银行</li>
          <li>最后统一报警</li>
        </ol>
      </div>
    </section>

    <section class="card-block">
      <div class="section-head">
        <h2>5 步急救流程</h2>
        <a href="/guide/communication">查看沟通话术 ›</a>
      </div>
      <div class="step-grid">
        <article v-for="(step, index) in steps" :key="step.title" class="step-card">
          <span class="step-no">{{ index + 1 }}</span>
          <h3>{{ step.title }}</h3>
          <p>{{ step.detail }}</p>
        </article>
      </div>
    </section>

    <section class="two-col">
      <div class="card-block">
        <div class="section-head">
          <h2>按场景处理</h2>
        </div>
        <div class="situation-list">
          <article v-for="item in situations" :key="item.title" class="list-row">
            <strong>{{ item.title }}</strong>
            <p>{{ item.action }}</p>
          </article>
        </div>
      </div>

      <div class="card-block side-warning">
        <div class="section-head">
          <h2>紧急联系电话</h2>
        </div>
        <div class="call-list">
          <div v-for="[number, label] in calls" :key="number" class="call-item">
            <strong>{{ number }}</strong>
            <span>{{ label }}</span>
          </div>
        </div>
        <a class="primary-button" href="/guide/checklist">顺手检查家庭防骗配置</a>
      </div>
    </section>
  </div>
</template>

<style scoped>
.page-shell {
  width: min(100%, 1240px);
  margin: 0 auto;
  padding: 1.25rem 1.25rem 2rem;
}
.page-hero, .card-block {
  border: 1px solid #dce7ff;
  border-radius: 24px;
  background: #fff;
  box-shadow: 0 10px 28px rgba(44, 73, 138, 0.06);
}
.page-hero {
  display: grid;
  grid-template-columns: minmax(0, 1.5fr) 320px;
  gap: 1rem;
  padding: 1.5rem;
}
.page-badge {
  display: inline-flex;
  padding: 0.3rem 0.65rem;
  border-radius: 999px;
  font-size: 0.82rem;
  font-weight: 700;
}
.page-badge.danger {
  background: #fff0e8;
  color: #f16923;
}
.page-hero h1 {
  margin: 0.9rem 0 0.8rem;
  font-size: clamp(2.3rem, 4vw, 3.5rem);
  line-height: 1.15;
  color: #213d72;
}
.page-hero p {
  margin: 0;
  color: #69758d;
  font-size: 1.08rem;
  line-height: 1.8;
}
.hero-side {
  padding: 1rem 1.1rem;
  border-radius: 18px;
  align-self: stretch;
}
.hero-side.danger {
  background: linear-gradient(180deg, #fff8f1, #fff);
  border: 1px solid #ffd7bc;
}
.hero-side strong {
  color: #f16923;
}
.hero-side ol {
  margin: 0.8rem 0 0;
  padding-left: 1.2rem;
  color: #6a7181;
  line-height: 1.9;
}
.card-block {
  margin-top: 1rem;
  padding: 1.1rem;
}
.section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 0.85rem;
}
.section-head h2 {
  margin: 0;
  color: #223d72;
  font-size: 1.8rem;
}
.section-head a {
  color: #4e78db;
  text-decoration: none;
  font-weight: 600;
}
.step-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 0.9rem;
}
.step-card {
  padding: 1rem;
  border: 1px solid #e4ebff;
  border-radius: 18px;
  background: linear-gradient(180deg, #fff, #fbfdff);
}
.step-no {
  display: inline-grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border-radius: 999px;
  background: linear-gradient(180deg, #ff972f, #f26e20);
  color: #fff;
  font-weight: 800;
}
.step-card h3 {
  margin: 0.8rem 0 0.45rem;
  color: #254074;
}
.step-card p, .list-row p, .call-item span {
  margin: 0;
  color: #6b758b;
  line-height: 1.75;
}
.two-col {
  display: grid;
  grid-template-columns: minmax(0, 1.5fr) 340px;
  gap: 1rem;
}
.situation-list {
  display: grid;
  gap: 0.8rem;
}
.list-row {
  padding: 0.95rem 1rem;
  border: 1px solid #e4ebff;
  border-radius: 16px;
}
.list-row strong {
  display: block;
  margin-bottom: 0.3rem;
  color: #244073;
}
.side-warning {
  border-color: #ffd9bf;
  background: linear-gradient(180deg, #fffaf4, #fff);
}
.call-list {
  display: grid;
  gap: 0.75rem;
}
.call-item {
  padding: 0.9rem 1rem;
  border-radius: 16px;
  background: #fff;
  border: 1px solid #ffe6d6;
}
.call-item strong {
  display: block;
  color: #f16c22;
  font-size: 1.4rem;
}
.primary-button {
  display: block;
  margin-top: 1rem;
  padding: 0.9rem 1rem;
  border-radius: 14px;
  background: linear-gradient(180deg, #ff982e, #ff7620);
  color: #fff;
  text-align: center;
  text-decoration: none;
  font-weight: 700;
}
@media (max-width: 1100px) {
  .page-hero, .two-col { grid-template-columns: 1fr; }
  .step-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 720px) {
  .page-shell { padding: 0.75rem 0.9rem 1.5rem; }
  .step-grid { grid-template-columns: 1fr; }
}
</style>
