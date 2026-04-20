# 老年人防诈骗 Wiki

> 面向子女的老年人防诈骗知识库与家庭应急手册

## 项目简介

这是一个**开源、公益、社区共建**的老年人防诈骗知识库，旨在帮助子女更好地保护父母免受诈骗侵害。

### 核心功能

- 🚨 **应急SOP** - 发现父母正在被诈骗时的5步急救指南
- 🎯 **人群测试** - 3分钟测试，了解父母属于哪种易骗类型
- 📚 **诈骗场景库** - 10大高发诈骗场景，真实案例+识别要点
- 👥 **人群分类指南** - 7类易骗人群深度分析
- 🛡️ **家庭防御清单** - 可打印的A4检查清单

## 快速开始

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/your-username/anti-scam-wiki.git
cd anti-scam-wiki

# 安装依赖
npm install

# 启动开发服务器
npm run docs:dev
```

### 数据抓取

```bash
# 安装Python依赖
pip install -r requirements.txt

# 设置Gemini API密钥
export GOOGLE_API_KEY="your-api-key"

# 运行爬虫
python scripts/process.py
```

## 项目结构

```
anti-scam-wiki/
├── docs/                    # VitePress文档
│   ├── .vitepress/         # 配置文件
│   ├── scenarios/          # 诈骗场景
│   ├── profiles/           # 人群分类
│   ├── cases/              # 案例库
│   └── guide/              # 指南
├── scripts/                # Python脚本
│   ├── crawl/              # 爬虫
│   └── ai/                 # AI处理
├── data/                   # 数据
│   ├── raw/                # 原始数据
│   └── published/          # 已发布案例
└── .github/workflows/      # 自动部署
```

## 贡献指南

### 你可以这样贡献

- 📝 **提交案例** - 通过GitHub Issue提交真实诈骗案例
- 🔧 **改进代码** - 优化爬虫、AI处理或前端展示
- 📖 **完善文档** - 补充人群分析、沟通话术等内容
- 🌐 **翻译推广** - 帮助推广到更多社区

### 提交案例模板

```markdown
**诈骗类型**：冒充客服退款
**受骗人群**：技术懵懂型老人
**诈骗话术**：
- "您的快递丢了，要给您退款"
- "需要下载APP办理退款"

**识别要点**：
- 主动来电声称快递问题
- 要求下载陌生APP

**应对措施**：
- 立即挂断
- 通过官方平台核实
```

## 技术栈

- **前端**: VitePress
- **爬虫**: Python + requests + BeautifulSoup
- **AI处理**: Gemini API
- **部署**: GitHub Pages
- **自动化**: GitHub Actions

## 免责声明

本站信息仅供预防参考，不构成官方反诈建议。如遇诈骗请立即拨打：

- **96110** - 反诈专线
- **110** - 报警电话

## 许可证

[MIT License](LICENSE)

---

**保护父母，从了解开始。**
