export const profileContent = {
  lonely: {
    title: '孤独空巢型',
    badge: '重点陪伴型',
    summary: '独居、缺少陪伴、愿意和陌生人长时间交流，更容易被情感、关怀和熟人式接近打动。',
    signals: ['经常一个人在家', '愿意和陌生人聊天', '渴望被关心和需要'],
    scams: ['情感诈骗', '假冒熟人', '上门推销'],
    actions: ['固定联系频率', '鼓励真实社交', '陌生人上门先核实身份'],
    talk: '多从“陪伴”和“关心”切入，少用责备语气。',
    scenarioLink: '/scenarios/romance'
  },
  'health-anxiety': {
    title: '健康焦虑型',
    badge: '健康防骗型',
    summary: '对生病和衰老很敏感，容易被保健品、专家讲座、免费体检和“偏方奇效”打动。',
    signals: ['频繁关注养生信息', '容易相信专家推荐', '愿意为健康高消费'],
    scams: ['保健品诈骗', '理疗仪器骗局', '名医义诊推销'],
    actions: ['优先做正规体检', '健康消费设上限', '不要现场购买高价产品'],
    talk: '用“我们一起去正规医院确认”替代正面否定。',
    scenarioLink: '/scenarios/health-products'
  },
  greedy: {
    title: '贪小便宜型',
    badge: '诱饵高风险型',
    summary: '节俭、爱薅羊毛、容易相信免费礼品和返利优惠，更容易被小额甜头慢慢套进去。',
    signals: ['喜欢参加免费活动', '容易被优惠吸引', '常觉得“不拿白不拿”'],
    scams: ['免费送礼', '刷单返利', '中奖诈骗'],
    actions: ['直接讲透“免费最贵”', '陌生二维码不扫', '不要为返利先垫资'],
    talk: '不要嘲笑父母爱占便宜，要强调骗子就是利用这个心理。',
    scenarioLink: '/scenarios/free-gift'
  },
  investor: {
    title: '盲目投资型',
    badge: '高损失预警型',
    summary: '希望让钱生钱，容易被高回报、低风险、内部机会等话术吸引，损失金额往往最大。',
    signals: ['热衷投资理财', '会听熟人推荐项目', '容易相信“内部渠道”'],
    scams: ['养老投资诈骗', '荐股骗局', '虚拟币骗局'],
    actions: ['统一资金管理', '投资前必须二次确认', '高收益默认高风险'],
    talk: '用真实亏损案例比抽象劝说更有效。',
    scenarioLink: '/scenarios/investment'
  },
  cognitive: {
    title: '认知衰退型',
    badge: '高依赖保护型',
    summary: '记忆力、判断力和应激反应下降，更容易在高压或复杂话术下直接照做。',
    signals: ['容易忘事', '分辨复杂信息吃力', '遇事容易慌张'],
    scams: ['冒充公检法', '验证码骗局', '转账诈骗'],
    actions: ['简化支付权限', '提高家属协助频率', '把规则写下来贴在家里'],
    talk: '规则越简单越好，尽量用固定流程代替临场判断。',
    scenarioLink: '/scenarios/fake-police'
  },
  social: {
    title: '热衷社交型',
    badge: '群体带动型',
    summary: '喜欢进群、参加活动、旅游和熟人圈推荐，更容易被“大家都在做”的氛围带动。',
    signals: ['活跃于社群', '爱参加活动', '容易相信熟人推荐'],
    scams: ['旅游团购', '社群团购', '熟人荐货'],
    actions: ['不在群里冲动下单', '报名活动先核实主办方', '熟人推荐也要二次确认'],
    talk: '可以从“不是不让你参加，是先帮你把关”入手。',
    scenarioLink: '/scenarios/travel'
  },
  'tech-illiterate': {
    title: '技术懵懂型',
    badge: '手机安全型',
    summary: '不熟悉手机和支付操作，容易点错链接、扫错码、装错 App，也更容易被共享屏幕和验证码套路影响。',
    signals: ['手机操作不熟练', '分不清官方和仿冒界面', '容易误触链接和二维码'],
    scams: ['AI换脸', '假冒客服退款', '钓鱼链接和假 App'],
    actions: ['关闭未知来源安装', '验证码绝不告诉别人', '陌生链接和二维码一律先问'],
    talk: '别讲太多技术词，直接讲“哪些不能点、哪些不能给”。',
    scenarioLink: '/scenarios/ai-face'
  }
}
