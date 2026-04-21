# 部署指南

## 前置要求

- GitHub 账号
- Node.js 20 或更高版本
- Python 3.8 或更高版本

## 首次发布

1. 创建一个公开仓库，名称建议为 `anti-scam-wiki`
2. 将本地代码推送到 GitHub
3. 在仓库 `Settings -> Pages` 中将来源设置为 `GitHub Actions`
4. 推送到 `main` 分支后，GitHub Actions 会自动构建并发布

## 本地命令

```bash
npm install
npm run docs:dev
npm run check
npm run docs:preview
```

## 关键配置

站点基础路径配置在：

```text
docs/.vitepress/config.mjs
```

如果仓库名不是 `anti-scam-wiki`，需要同步修改：

```javascript
export default defineConfig({
  base: '/anti-scam-wiki/'
})
```

## 自动部署

项目内置工作流：

- `.github/workflows/deploy.yml`：构建并发布 VitePress 站点
- `.github/workflows/crawl.yml`：定时抓取案例数据

## 自动抓取说明

如果需要启用 AI 提取，请在 GitHub 仓库 Secrets 中配置：

- `GOOGLE_API_KEY`

未配置时，抓取流程仍可运行，但只会输出基础模板化结构。

## 常见问题

### 页面 404

- 检查 `base` 是否与仓库名一致
- 检查 GitHub Pages 来源是否设置为 `GitHub Actions`
- 等待部署完成后再刷新页面

### 样式丢失

- 通常是 `base` 配置错误
- 确认构建产物来自 `docs/.vitepress/dist`

### 构建失败

- 先执行 `npm install`
- 再运行 `npm run check`
- 确认使用的是 Node.js 20+
