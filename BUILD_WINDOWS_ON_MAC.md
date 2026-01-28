# 在macOS上打包Windows .exe文件

## 🎯 三种方案

### 方案一：GitHub Actions（推荐，免费）

使用GitHub的免费CI/CD服务，在云端自动打包Windows版本。

### 方案二：Docker（本地打包）

使用Docker在macOS上运行Windows环境进行打包。

### 方案三：虚拟机

在macOS上安装Windows虚拟机进行打包。

---

## ✅ 方案一：GitHub Actions（最简单）

### 步骤1：创建GitHub仓库

1. 访问 https://github.com/new
2. 创建新仓库（Public或Private都可以）
3. 仓库名称：例如 `wjx-autofill-tool`

### 步骤2：上传项目文件

```bash
# 在项目目录下
cd "/Users/wangshan/Desktop/wjx 2"

# 初始化git仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/wjx-autofill-tool.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

### 步骤3：自动打包

推送到GitHub后，GitHub Actions会自动开始打包：

1. 访问你的GitHub仓库
2. 点击 "Actions" 标签
3. 等待 "Build Windows Executable" workflow完成（约3-5分钟）
4. 点击完成的workflow
5. 在 "Artifacts" 部分下载 `问卷星自动填写工具-Windows.zip`

### 步骤4：获取Windows .exe文件

下载的zip文件包含：
```
问卷星自动填写工具-Windows.zip
└── 问卷星自动填写工具.exe
```

解压后即可在Windows上运行！

### 高级功能：自动发布

如果想创建正式版本：

```bash
# 创建标签
git tag v1.0.0

# 推送标签
git push origin v1.0.0
```

这会自动在GitHub Releases中创建发布版本。

---

## 🐳 方案二：Docker（本地打包）

### 前置要求

1. 安装Docker Desktop for Mac
   - 下载：https://www.docker.com/products/docker-desktop/

### 步骤1：创建Dockerfile

项目已包含 `Dockerfile.windows`，内容如下：

```dockerfile
FROM python:3.10-windowsservercore-ltsc2022

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pyinstaller

COPY . .

RUN pyinstaller wjx2.spec

CMD ["cmd"]
```

### 步骤2：构建Docker镜像

```bash
cd "/Users/wangshan/Desktop/wjx 2"

# 构建Windows镜像（需要Windows服务器）
docker build -f Dockerfile.windows -t wjx-windows-builder .
```

⚠️ **注意：** Docker Desktop for Mac默认不支持Windows容器，需要特殊配置。

### 步骤3：运行容器

```bash
# 运行容器
docker run --rm -v "$(pwd)/dist:/app/dist" wjx-windows-builder
```

### 步骤4：获取可执行文件

打包完成后，Windows .exe文件会在 `dist` 目录中。

---

## 💻 方案三：虚拟机

### 步骤1：安装Windows虚拟机

1. 下载虚拟机软件：
   - VMware Fusion（推荐）
   - Parallels Desktop
   - VirtualBox（免费）

2. 下载Windows ISO：
   - Windows 10/11 ISO（需要许可证）

3. 创建虚拟机并安装Windows

### 步骤2：在虚拟机中打包

1. 将项目文件夹复制到虚拟机
2. 运行 `build_windows.bat`
3. 获取生成的 `问卷星自动填写工具.exe`

3. 将 .exe文件复制回macOS

---

## 📊 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **GitHub Actions** | 免费、自动化、无需Windows | 需要GitHub账号、网络连接 | 推荐，最简单 |
| **Docker** | 本地运行、可重复 | 配置复杂、Mac支持有限 | 有Docker经验 |
| **虚拟机** | 完全控制、可测试 | 需要Windows许可证、占用资源 | 需要频繁打包 |

---

## 🎯 推荐方案

### 对于大多数用户：GitHub Actions

**原因：**
- ✅ 完全免费
- ✅ 自动化，无需手动操作
- ✅ 无需Windows许可证
- ✅ 可以设置自动触发

### 对于开发者：Docker

**原因：**
- ✅ 本地运行，不依赖外部服务
- ✅ 可重复构建
- ✅ 适合CI/CD集成

### 对于企业用户：虚拟机

**原因：**
- ✅ 完全控制
- ✅ 可以测试程序
- ✅ 支持复杂的构建流程

---

## 🚀 快速开始（GitHub Actions）

### 1分钟快速开始

```bash
# 1. 创建GitHub仓库（在网页上操作）

# 2. 在项目目录执行
cd "/Users/wangshan/Desktop/wjx 2"
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/你的用户名/仓库名.git
git branch -M main
git push -u origin main

# 3. 等待3-5分钟，在GitHub Actions中下载
```

### 5分钟详细指南

1. **创建GitHub账号**（如果没有）
   - 访问 https://github.com/signup
   - 免费注册

2. **创建新仓库**
   - 点击右上角 "+" → "New repository"
   - 仓库名：`wjx-autofill-tool`
   - 选择 Public 或 Private
   - 点击 "Create repository"

3. **上传代码**
   - 复制上面提供的git命令
   - 在终端中执行

4. **等待打包**
   - 访问仓库页面
   - 点击 "Actions" 标签
   - 等待workflow完成

5. **下载文件**
   - 点击完成的workflow
   - 在 "Artifacts" 部分下载zip文件

---

## 📝 常见问题

### Q1: GitHub Actions免费吗？

A: 是的！GitHub提供免费的Actions额度：
- Public仓库：无限
- Private仓库：每月2000分钟

### Q2: 打包需要多长时间？

A: 通常3-5分钟，取决于项目大小。

### Q3: 可以自动触发打包吗？

A: 可以！workflow配置支持：
- 推送代码时自动打包
- 创建标签时自动发布
- 手动触发打包

### Q4: Docker方案在Mac上能用吗？

A: 可以，但需要特殊配置。推荐使用GitHub Actions。

### Q5: 虚拟机需要Windows许可证吗？

A: 是的，需要合法的Windows许可证。

---

## 🎉 总结

**推荐使用GitHub Actions：**
- ✅ 最简单
- ✅ 完全免费
- ✅ 自动化
- ✅ 无需Windows

**其他方案：**
- Docker：适合有经验的开发者
- 虚拟机：适合需要完全控制的场景

选择最适合你的方案，几分钟内就能在macOS上生成Windows .exe文件！
