<script setup>
import cases from '../../../../data/published/cases.json'

const sortedCases = [...cases]
  .sort((a, b) => (b.crawled_at || '').localeCompare(a.crawled_at || ''))
  .slice(0, 3)

const formatGroups = (groups) => {
  if (!Array.isArray(groups) || groups.length === 0) {
    return '待分析'
  }

  return groups.join(' / ')
}
</script>

<template>
  <section class="recent-cases">
    <div class="recent-cases__header">
      <h2>最新案例</h2>
      <a href="/cases/latest" class="recent-cases__link">查看全部</a>
    </div>

    <p class="recent-cases__intro">
      首页会自动读取最新案例数据。后续只要更新 <code>cases.json</code>，这里就会同步变化。
    </p>

    <div v-if="sortedCases.length" class="recent-cases__grid">
      <a
        v-for="item in sortedCases"
        :key="item.id"
        class="recent-cases__card"
        :href="`/cases/generated/${item.id}`"
      >
        <div class="recent-cases__meta">
          <span>{{ item.scam_type || '待分类' }}</span>
          <span>{{ item.source_name || '未知来源' }}</span>
        </div>
        <h3>{{ item.title || '未命名案例' }}</h3>
        <p>{{ item.summary || '暂无摘要。' }}</p>
        <strong>{{ formatGroups(item.target_group) }}</strong>
      </a>
    </div>

    <div v-else class="recent-cases__empty">
      <p>当前还没有正式入库的案例，首页模块已准备好，后续抓取到数据后会自动展示。</p>
      <div class="recent-cases__actions">
        <a href="/cases/latest">查看案例库状态</a>
        <a href="/scenarios/">先看诈骗场景</a>
      </div>
    </div>
  </section>
</template>

<style scoped>
.recent-cases {
  margin: 2rem 0 3rem;
  padding: 1.5rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 20px;
  background:
    radial-gradient(circle at top right, rgba(255, 208, 117, 0.18), transparent 32%),
    linear-gradient(180deg, rgba(248, 244, 235, 0.8), rgba(255, 255, 255, 0.95));
}

.recent-cases__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.recent-cases__header h2 {
  margin: 0;
  font-size: 1.4rem;
}

.recent-cases__link,
.recent-cases__actions a {
  color: var(--vp-c-brand-1);
  font-weight: 600;
  text-decoration: none;
}

.recent-cases__intro {
  margin: 0.75rem 0 1.25rem;
  color: var(--vp-c-text-2);
}

.recent-cases__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.recent-cases__card {
  display: block;
  padding: 1rem;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.92);
  color: inherit;
  text-decoration: none;
  transition:
    transform 0.18s ease,
    box-shadow 0.18s ease,
    border-color 0.18s ease;
}

.recent-cases__card:hover {
  transform: translateY(-2px);
  border-color: rgba(255, 140, 0, 0.35);
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.08);
}

.recent-cases__meta {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 0.75rem;
  font-size: 0.82rem;
  color: var(--vp-c-text-3);
}

.recent-cases__card h3 {
  margin: 0 0 0.75rem;
  font-size: 1.05rem;
  line-height: 1.45;
}

.recent-cases__card p {
  margin: 0 0 0.85rem;
  color: var(--vp-c-text-2);
  line-height: 1.7;
}

.recent-cases__card strong {
  font-size: 0.9rem;
}

.recent-cases__empty {
  padding: 1rem 0 0.25rem;
}

.recent-cases__empty p {
  margin: 0 0 0.75rem;
  color: var(--vp-c-text-2);
}

.recent-cases__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

@media (max-width: 960px) {
  .recent-cases__grid {
    grid-template-columns: 1fr;
  }
}
</style>
