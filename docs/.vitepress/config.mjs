import { defineConfig } from 'vitepress'

export default defineConfig({
  title: '老年人防诈骗 Wiki',
  description: '面向子女的老年人防诈骗知识库与家庭应急手册',
  base: '/anti-scam-wiki/',
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '诈骗场景', link: '/scenarios/' },
      { text: '人群分类', link: '/profiles/' },
      { text: '案例库', link: '/cases/' },
      { text: '指南', link: '/guide/checklist' }
    ],
    sidebar: {
      '/scenarios/': [
        { text: '场景总览', link: '/scenarios/' },
        { text: '冒充客服退款', link: '/scenarios/fake-customer-service' },
        { text: '冒充公检法', link: '/scenarios/fake-police' },
        { text: '保健品诈骗', link: '/scenarios/health-products' },
        { text: '中奖/免费送礼', link: '/scenarios/free-gift' },
        { text: '养老投资', link: '/scenarios/investment' },
        { text: '情感诈骗', link: '/scenarios/romance' },
        { text: '旅游团购', link: '/scenarios/travel' },
        { text: 'AI换脸', link: '/scenarios/ai-face' },
        { text: '假冒熟人', link: '/scenarios/fake-friend' },
        { text: '刷单返利', link: '/scenarios/brushing' }
      ],
      '/profiles/': [
        { text: '人群总览', link: '/profiles/' },
        { text: '孤独空巢型', link: '/profiles/lonely' },
        { text: '健康焦虑型', link: '/profiles/health-anxiety' },
        { text: '贪小便宜型', link: '/profiles/greedy' },
        { text: '盲目投资型', link: '/profiles/investor' },
        { text: '认知衰退型', link: '/profiles/cognitive' },
        { text: '热衷社交型', link: '/profiles/social' },
        { text: '技术懵懂型', link: '/profiles/tech-illiterate' }
      ],
      '/guide/': [
        { text: '沟通话术', link: '/guide/communication' },
        { text: '情绪支持', link: '/guide/emotional' },
        { text: '家庭清单', link: '/guide/checklist' }
      ],
      '/cases/': [
        { text: '案例库说明', link: '/cases/' },
        { text: '最新案例', link: '/cases/latest' },
        { text: '自动生成索引', link: '/cases/generated/' }
      ]
    },
    search: {
      provider: 'local'
    },
    footer: {
      message: '本站信息仅供反诈预防参考，如遇诈骗请第一时间拨打 96110 或 110',
      copyright: 'Copyright © 2026 Anti-Scam Wiki Contributors'
    }
  }
})
