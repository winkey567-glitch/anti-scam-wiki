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
- 家庭防骗清单：适合打印后给家人使用
- 案例库：按时间、热度、区域查看真实公开案例
- 趋势研判：自动生成诈骗趋势、区域预警和嫌疑人范围研判
- 报案材料整理：把线索快速整理成给警方的报案草稿

## 技术栈

- 前端文档站：VitePress
- 数据抓取：Python + requests + BeautifulSoup
- 结构化提取：规则优先，可选 AI 辅助
- 部署：GitHub Pages + GitHub Actions

## 本地开发

建议使用 Node.js 20 或更高版本。

```bash
git clone https://github.com/winkey567-glitch/anti-scam-wiki.git
cd anti-scam-wiki
npm install
npm run docs:dev
```

构建检查：

```bash
npm run check
```

如果涉及 Python 抓取脚本：

```bash
python -m compileall scripts
python scripts/process.py
```

## 自动发布

仓库内置了一条一键发布脚本：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\publish.ps1 -Message "更新说明"
```

这条命令会自动完成：

- `npm run check`
- `git add -A`
- `git commit -m "..."`
- `git push origin 当前分支`

## 项目结构

```text
anti-scam-wiki/
├─ docs/                   # VitePress 站点内容
│  ├─ .vitepress/          # 站点配置与主题组件
│  ├─ scenarios/           # 诈骗场景
│  ├─ profiles/            # 人群分类
│  ├─ cases/               # 案例库
│  ├─ insights/            # 趋势与区域预警
│  └─ guide/               # 指南与报案整理工具
├─ scripts/                # 抓取、分析、生成脚本
├─ data/                   # 原始抓取结果与发布数据
└─ .github/workflows/      # 部署与定时任务
```

## 开源协作

欢迎以低负担方式参与：

- 提交公开可核实案例
- 修正文案、错别字、失效链接
- 改进抓取脚本和构建流程
- 增加更适合老年人家庭使用的内容

协作说明见：[CONTRIBUTING.md](/G:/anti-scam-wiki/CONTRIBUTING.md)

## 最小安全配置

这个项目建议保持“公开可读、少数人可写”的模式：

- 保护 `main` 分支，只通过 PR 合并
- 开启构建检查后再允许合并
- 不在仓库和页面里存放真实隐私信息
- 自动抓取结果视为待审核内容，不直接当作官方结论
- 报案整理工具仅做本地整理与复制，不做服务端收集

完整说明见：[SECURITY.md](/G:/anti-scam-wiki/SECURITY.md)

## 免责说明

本站内容仅供反诈预防参考，不构成官方建议、法律意见或警方结论。

如遇诈骗，请第一时间联系：

- `96110` 反诈专线
- `110` 报警电话

## 许可证

[MIT License](LICENSE)
