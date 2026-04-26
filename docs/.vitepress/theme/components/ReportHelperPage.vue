<script setup>
import { computed, ref } from 'vue'

const victimName = ref('')
const victimAge = ref('')
const contactName = ref('')
const contactPhone = ref('')
const incidentDate = ref('')
const incidentPlace = ref('')
const scamType = ref('')
const lossAmount = ref('')
const suspectName = ref('')
const suspectPhone = ref('')
const suspectAccount = ref('')
const suspectPlatform = ref('')
const suspectRegionGuess = ref('')
const reportSummary = ref('')
const evidenceNotes = ref('')

const evidenceChecklist = ref([
  { label: '聊天记录截图', checked: true },
  { label: '转账记录截图', checked: true },
  { label: '银行卡或收款账户信息', checked: true },
  { label: '通话记录或来电号码', checked: false },
  { label: '涉诈链接 / App / 平台页面截图', checked: false },
  { label: '快递单号 / 订单号 / 航班号等业务信息', checked: false }
])

const timeline = ref([
  { time: '', event: '' },
  { time: '', event: '' }
])

const copyLabel = ref('复制报案草稿')

function addTimelineRow() {
  timeline.value.push({ time: '', event: '' })
}

function removeTimelineRow(index) {
  if (timeline.value.length === 1) return
  timeline.value.splice(index, 1)
}

function resetForm() {
  victimName.value = ''
  victimAge.value = ''
  contactName.value = ''
  contactPhone.value = ''
  incidentDate.value = ''
  incidentPlace.value = ''
  scamType.value = ''
  lossAmount.value = ''
  suspectName.value = ''
  suspectPhone.value = ''
  suspectAccount.value = ''
  suspectPlatform.value = ''
  suspectRegionGuess.value = ''
  reportSummary.value = ''
  evidenceNotes.value = ''
  evidenceChecklist.value = evidenceChecklist.value.map((item, index) => ({
    ...item,
    checked: index < 3
  }))
  timeline.value = [{ time: '', event: '' }, { time: '', event: '' }]
  copyLabel.value = '复制报案草稿'
}

const selectedEvidence = computed(() =>
  evidenceChecklist.value.filter((item) => item.checked).map((item) => item.label)
)

const cleanTimeline = computed(() =>
  timeline.value.filter((item) => item.time.trim() || item.event.trim())
)

const reportText = computed(() => {
  const timelineBlock = cleanTimeline.value.length
    ? cleanTimeline.value.map((item, index) => `${index + 1}. ${item.time || '时间待补充'}：${item.event || '经过待补充'}`).join('\n')
    : '1. 时间线待补充'

  const evidenceBlock = selectedEvidence.value.length
    ? selectedEvidence.value.map((item, index) => `${index + 1}. ${item}`).join('\n')
    : '1. 证据目录待补充'

  return [
    '报案线索整理草稿',
    '',
    '一、报案人与受害人信息',
    `1. 受害人姓名：${victimName.value || '待补充'}`,
    `2. 受害人年龄：${victimAge.value || '待补充'}`,
    `3. 联系人姓名：${contactName.value || '待补充'}`,
    `4. 联系人电话：${contactPhone.value || '待补充'}`,
    '',
    '二、案件基本情况',
    `1. 初次受骗时间：${incidentDate.value || '待补充'}`,
    `2. 受骗地点 / 所在地：${incidentPlace.value || '待补充'}`,
    `3. 涉嫌诈骗类型：${scamType.value || '待补充'}`,
    `4. 初步损失金额：${lossAmount.value || '待补充'}`,
    `5. 简要经过：${reportSummary.value || '待补充'}`,
    '',
    '三、嫌疑人和涉诈渠道信息',
    `1. 对方姓名 / 昵称：${suspectName.value || '待补充'}`,
    `2. 对方电话 / 社交账号：${suspectPhone.value || '待补充'}`,
    `3. 收款账号 / 银行卡 / 钱包地址：${suspectAccount.value || '待补充'}`,
    `4. 涉诈平台 / App / 链接：${suspectPlatform.value || '待补充'}`,
    `5. 嫌疑人区域线索：${suspectRegionGuess.value || '待补充'}`,
    '',
    '四、时间线整理',
    timelineBlock,
    '',
    '五、已掌握证据目录',
    evidenceBlock,
    evidenceNotes.value ? `\n补充证据说明：${evidenceNotes.value}` : '',
    '',
    '六、提交提醒',
    '1. 报警时同时提供聊天记录、转账截图、收款账户、通话记录和涉诈链接信息。',
    '2. 如果仍在转账过程中，应先联系银行或支付平台止付，再提交本整理材料。',
    '3. 此草稿适合先发给家属统一信息，也可打印或复制后交给警方进一步核验。'
  ]
    .filter(Boolean)
    .join('\n')
})

async function copyReport() {
  try {
    await navigator.clipboard.writeText(reportText.value)
    copyLabel.value = '已复制，可直接粘贴'
    window.setTimeout(() => {
      copyLabel.value = '复制报案草稿'
    }, 2000)
  } catch {
    copyLabel.value = '复制失败，请手动复制'
  }
}
</script>

<template>
  <div class="page-shell">
    <section class="page-hero">
      <div>
        <span class="page-badge">报案材料整理</span>
        <h1>先把线索整理清楚，再更快把资料交给警方</h1>
        <p>把时间线、联系方式、转账账户、证据目录先集中到一页，家属可以边通话边填，最后直接复制成报案草稿。</p>
      </div>
      <div class="hero-side">
        <strong>使用建议</strong>
        <ol>
          <li>先填案件经过和时间线，不要求一次填完。</li>
          <li>优先补全对方号码、账号、平台、链接和转账信息。</li>
          <li>整理完先止付，再把草稿和截图一并交给警方。</li>
        </ol>
      </div>
    </section>

    <section class="tool-grid">
      <div class="form-panel">
        <div class="section-card">
          <h2>受害人与联系人</h2>
          <div class="field-grid">
            <label><span>受害人姓名</span><input v-model="victimName" placeholder="如：张某" /></label>
            <label><span>受害人年龄</span><input v-model="victimAge" placeholder="如：68 岁" /></label>
            <label><span>联系人姓名</span><input v-model="contactName" placeholder="如：女儿李某" /></label>
            <label><span>联系人电话</span><input v-model="contactPhone" placeholder="便于警方回访" /></label>
          </div>
        </div>

        <div class="section-card">
          <h2>案件基本情况</h2>
          <div class="field-grid">
            <label><span>初次受骗时间</span><input v-model="incidentDate" placeholder="如：2026-04-26 14:30" /></label>
            <label><span>受骗地点 / 所在地</span><input v-model="incidentPlace" placeholder="如：重庆市渝中区家中" /></label>
            <label><span>诈骗类型</span><input v-model="scamType" placeholder="如：机票退改签诈骗" /></label>
            <label><span>损失金额</span><input v-model="lossAmount" placeholder="如：29800 元" /></label>
          </div>
          <label class="full-field">
            <span>简要经过</span>
            <textarea v-model="reportSummary" rows="4" placeholder="用自己的话简要说明：对方怎么联系、怎么诱导、最后怎么转账。"/>
          </label>
        </div>

        <div class="section-card">
          <h2>嫌疑人和涉诈渠道</h2>
          <div class="field-grid">
            <label><span>对方姓名 / 昵称</span><input v-model="suspectName" placeholder="如：客服小王 / 某老师" /></label>
            <label><span>对方电话 / 社交账号</span><input v-model="suspectPhone" placeholder="手机号、微信号、QQ、抖音号等" /></label>
            <label><span>收款账号 / 银行卡</span><input v-model="suspectAccount" placeholder="银行卡、支付宝、微信、钱包地址等" /></label>
            <label><span>涉诈平台 / 链接</span><input v-model="suspectPlatform" placeholder="App 名称、网址、群聊、直播间等" /></label>
          </div>
          <label class="full-field">
            <span>嫌疑人区域线索</span>
            <textarea v-model="suspectRegionGuess" rows="3" placeholder="如：提到境外来电、缅北、外地收款地名、跨省寄件、某地口音等。"/>
          </label>
        </div>

        <div class="section-card">
          <h2>时间线整理</h2>
          <div v-for="(item, index) in timeline" :key="index" class="timeline-row">
            <input v-model="item.time" placeholder="时间，如 14:35" />
            <input v-model="item.event" placeholder="发生了什么，如 对方要求下载某 App" />
            <button type="button" class="ghost-btn" @click="removeTimelineRow(index)">删除</button>
          </div>
          <button type="button" class="secondary-btn" @click="addTimelineRow">新增一条时间线</button>
        </div>

        <div class="section-card">
          <h2>证据目录</h2>
          <div class="checklist">
            <label v-for="item in evidenceChecklist" :key="item.label" class="check-item">
              <input v-model="item.checked" type="checkbox" />
              <span>{{ item.label }}</span>
            </label>
          </div>
          <label class="full-field">
            <span>补充证据说明</span>
            <textarea v-model="evidenceNotes" rows="3" placeholder="如：手机里还有录音、订单号、快递截图、航班号、短信验证码页面等。"/>
          </label>
        </div>
      </div>

      <aside class="report-panel">
        <div class="report-card">
          <div class="report-head">
            <h2>报案草稿</h2>
            <div class="report-actions">
              <button type="button" class="primary-btn" @click="copyReport">{{ copyLabel }}</button>
              <button type="button" class="ghost-btn" @click="resetForm">清空重填</button>
            </div>
          </div>
          <textarea class="report-output" :value="reportText" rows="26" readonly />
        </div>

        <div class="tips-card">
          <h3>给警方时优先补充</h3>
          <ul>
            <li>第一笔和最后一笔转账的时间、金额、去向账户。</li>
            <li>对方使用过的全部号码、昵称、账号、群名、链接、App。</li>
            <li>能够证明过程的关键截图：聊天、转账、收款码、会议共享屏幕页面。</li>
            <li>如果家属还在被诱导，先止付，不要边转账边继续跟进对方指令。</li>
          </ul>
        </div>
      </aside>
    </section>
  </div>
</template>

<style scoped>
.page-shell { width:min(100%,1280px); margin:0 auto; padding:1.25rem 1.25rem 2rem; }
.page-hero,.section-card,.report-card,.tips-card { border:1px solid #dce7ff; border-radius:24px; background:#fff; box-shadow:0 10px 28px rgba(44,73,138,.06); }
.page-hero { display:grid; grid-template-columns:minmax(0,1.45fr) 320px; gap:1rem; padding:1.5rem; }
.page-badge { display:inline-flex; padding:.3rem .65rem; border-radius:999px; background:#edf4ff; color:#3777f4; font-size:.82rem; font-weight:700; }
.page-hero h1 { margin:.9rem 0 .8rem; font-size:clamp(2.2rem,4vw,3.3rem); line-height:1.12; color:#213d72; }
.page-hero p,.hero-side li,.section-card span,.tips-card li { color:#69758d; line-height:1.8; }
.hero-side { padding:1rem 1.1rem; border-radius:18px; background:linear-gradient(180deg,#f7fbff,#fff); border:1px solid #dce8ff; }
.hero-side strong,.section-card h2,.report-card h2,.tips-card h3 { color:#244073; }
.hero-side ol { margin:.8rem 0 0; padding-left:1.15rem; }
.tool-grid { display:grid; grid-template-columns:minmax(0,1.3fr) minmax(320px,.9fr); gap:1rem; margin-top:1rem; align-items:start; }
.form-panel { display:grid; gap:1rem; }
.section-card,.report-card,.tips-card { padding:1.15rem; }
.section-card h2,.report-card h2 { margin:0 0 .95rem; font-size:1.35rem; }
.field-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.85rem; }
label { display:grid; gap:.42rem; }
input,textarea { width:100%; border:1px solid #d5def0; border-radius:14px; padding:.82rem .9rem; font:inherit; color:#233a65; background:#fbfdff; }
input:focus,textarea:focus { outline:none; border-color:#7ca7ff; box-shadow:0 0 0 3px rgba(89,134,240,.12); }
.full-field { margin-top:.9rem; }
.timeline-row { display:grid; grid-template-columns:150px minmax(0,1fr) 78px; gap:.7rem; margin-bottom:.75rem; }
.checklist { display:grid; gap:.65rem; }
.check-item { display:flex; gap:.65rem; align-items:flex-start; }
.check-item input { width:auto; margin-top:.2rem; }
.report-panel { display:grid; gap:1rem; position:sticky; top:84px; }
.report-head { display:flex; justify-content:space-between; align-items:center; gap:1rem; margin-bottom:.9rem; }
.report-actions { display:flex; gap:.6rem; flex-wrap:wrap; }
.report-output { min-height:660px; background:#f8fbff; font-size:.92rem; line-height:1.65; }
.primary-btn,.secondary-btn,.ghost-btn { border-radius:999px; padding:.72rem 1rem; font:inherit; cursor:pointer; transition:.18s ease; }
.primary-btn { border:1px solid #4a75dc; background:#4a75dc; color:#fff; }
.secondary-btn { border:1px solid #dce7ff; background:#f5f8ff; color:#345aa8; }
.ghost-btn { border:1px solid #d8dfef; background:#fff; color:#51627f; }
.primary-btn:hover,.secondary-btn:hover,.ghost-btn:hover { transform:translateY(-1px); }
.tips-card ul { margin:.5rem 0 0; padding-left:1.15rem; }
@media (max-width: 1040px) { .tool-grid,.page-hero { grid-template-columns:1fr; } .report-panel { position:static; } }
@media (max-width: 720px) { .page-shell { padding:.75rem .9rem 1.5rem; } .field-grid,.timeline-row { grid-template-columns:1fr; } .report-head { align-items:flex-start; flex-direction:column; } }
</style>
