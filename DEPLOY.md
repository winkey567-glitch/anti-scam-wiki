# 部署指南

## 前置要求

- GitHub 账号
- 本地安装 Node.js (v18+)
- 本地安装 Python (v3.8+) - 用于爬虫

## 第一步：创建 GitHub 仓库

1. 登录 GitHub
2. 点击右上角 **+** → **New repository**
3. 仓库名称：`anti-scam-wiki`
4. 选择 **Public**（公开）
5. 不要勾选 "Add a README file"
6. 点击 **Create repository**

## 第二步：推送代码到 GitHub

在本地项目目录执行：

```bash
cd G:\anti-scam-wiki

# 初始化 git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Anti-Scam Wiki v1.0"

# 关联远程仓库（替换为你的用户名）
git remote add origin https://github.com/你的用户名/anti-scam-wiki.git

# 推送
git push -u origin main
```

## 第三步：启用 GitHub Pages

1. 进入仓库页面
2. 点击 **Settings** 标签
3. 左侧菜单选择 **Pages**
4. **Source** 选择 **GitHub Actions**

## 第四步：配置自动部署

项目已包含 `.github/workflows/deploy.yml`，推送后会自动部署。

### 部署状态查看

1. 进入仓库页面
2. 点击 **Actions** 标签
3. 查看部署状态

## 第五步：访问网站

部署完成后，访问地址：

```
https://你的用户名.github.io/anti-scam-wiki/
```

## 可选：配置自定义域名

1. 在 `docs/.vitepress/` 目录创建 `CNAME` 文件
2. 写入你的域名，如：`fangpian.wiki`
3. 在域名服务商配置 CNAME 指向 `你的用户名.github.io`
4. 在 GitHub Pages 设置中配置自定义域名

## 本地开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run docs:dev

# 构建
npm run docs:build

# 预览构建结果
npm run docs:preview
```

## 爬虫配置（可选）

如需启用自动爬虫：

1. 获取 Google AI API Key
2. 在 GitHub 仓库设置中添加 Secret：
   - 名称：`GOOGLE_API_KEY`
   - 值：你的 API Key
3. 爬虫会每天自动运行，抓取最新案例

## 更新网站

每次推送代码到 main 分支，GitHub Actions 会自动重新部署。

```bash
git add .
git commit -m "更新内容"
git push
```

## 故障排查

### 部署失败

1. 检查 Actions 日志
2. 确保 `docs/.vitepress/config.js` 中的 `base` 配置正确
3. 确保 `package.json` 存在且正确

### 页面404

1. 检查仓库名称是否与 `base` 配置一致
2. 等待几分钟后刷新（部署可能有延迟）
3. 检查 GitHub Pages 设置是否正确

### 样式丢失

确保 `base` 配置与仓库名称一致：

```javascript
// docs/.vitepress/config.js
export default defineConfig({
  base: '/anti-scam-wiki/',  // 必须与仓库名一致
  // ...
})
```

## 完成！

网站部署完成后，你就可以通过 GitHub Pages 地址访问了。

记得把网址分享给需要的人！
