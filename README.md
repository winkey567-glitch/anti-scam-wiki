# 老年人防诈骗 Wiki

> 面向子女的老年人防诈骗知识库与家庭应急手册

## 项目简介

这是一个开源、公益、社区共建的小型反诈知识库项目，目标很简单：

- 帮助子女快速识别父母可能遭遇的常见骗局
- 提供发现风险时可直接执行的家庭应急流程
- 用尽量低维护成本的方式长期稳定运行

## 当前功能

- 应急 SOP：发现家人正在被骗时的处理步骤
- 人群测试：帮助判断父母更容易被哪类骗局影响
- 诈骗场景库：整理常见诈骗套路、危险信号和应对方式
- 人群分类指南：按性格和习惯给出针对性建议
- 家庭防御清单：适合打印后给家人使用

## 技术栈

- 前端文档站：VitePress
- 数据抓取：Python + requests + BeautifulSoup
- AI 提取：Gemini API
- 部署：GitHub Pages + GitHub Actions

## 本地开发

建议使用 Node.js 20 或更高版本。

```bash
git clone https://github.com/your-username/anti-scam-wiki.git
cd anti-scam-wiki
npm install
npm run docs:dev
```

构建检查：

```bash
npm run check
```

## 自动推送到 GitHub

如果你希望本机在每次 `git commit` 后自动推送到 GitHub，可以执行：

```bash
powershell -ExecutionPolicy Bypass -File scripts/setup-git-hooks.ps1
```

启用后，本地每次提交都会自动执行一次：

```bash
git push origin 当前分支
```

项目还内置了一个一键发布脚本：

```bash
powershell -ExecutionPolicy Bypass -File scripts/publish.ps1 -Message "更新说明"
```

这条命令会自动完成：

- `npm run check`
- `git add -A`
- `git commit -m "..."`
- `git push origin 当前分支`（由 `post-commit` 钩子自动执行）

## 数据抓取

```bash
pip install -r requirements.txt
export GOOGLE_API_KEY="your-api-key"
python scripts/process.py
```

如果没有配置 `GOOGLE_API_KEY`，AI 提取模块会退回到模板化输出，方便先跑通流程。

## 项目结构

```text
anti-scam-wiki/
├── docs/                   # VitePress 站点内容
│   ├── .vitepress/         # 站点配置
│   ├── scenarios/          # 诈骗场景
│   ├── profiles/           # 人群分类
│   ├── cases/              # 案例库
│   └── guide/              # 指南内容
├── scripts/                # 抓取与处理脚本
│   ├── crawl/              # 数据源抓取
│   └── ai/                 # AI 提取逻辑
├── data/                   # 抓取结果与发布数据
└── .github/workflows/      # 自动部署与定时任务
```

## 开源协作

欢迎以低负担方式参与：

- 提交真实案例或补充公开案例
- 修正文案、错别字、链接和流程说明
- 改进抓取脚本和发布流程
- 增加更适合老人家庭使用的内容

## 运行原则

这个项目优先追求：

1. 内容清晰
2. 构建稳定
3. 易于部署
4. 低维护成本

不追求复杂功能，不引入重型后台，不把维护门槛抬高。

## 免责声明

本站内容仅供反诈预防参考，不构成官方建议或法律意见。如遇诈骗，请第一时间联系：

- `96110` 反诈专线
- `110` 报警电话

## 许可证

[MIT License](LICENSE)
