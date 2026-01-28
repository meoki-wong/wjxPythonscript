# 在macOS上打包生成Windows .exe文件

## 🎯 三种可行方案

### 方案一：使用GitHub Actions（推荐，免费）

这是最可靠且免费的方式，GitHub提供免费的Windows虚拟机来构建。

#### 步骤：

1. **创建GitHub仓库**
   - 访问 https://github.com/new
   - 创建新仓库
   - 上传项目文件

2. **创建GitHub Actions配置文件**
   - 在项目中创建 `.github/workflows/build.yml`
   - 配置自动打包工作流

3. **触发自动打包**
   - 推送代码到GitHub
   - GitHub Actions会自动运行
   - 下载生成的.exe文件

### 方案二：使用Docker（需要Docker Desktop）

通过Docker运行Windows容器进行打包。

#### 步骤：

1. **安装Docker Desktop**
   - 下载地址：https://www.docker.com/products/docker-desktop/
   - 启用Windows容器支持

2. **创建Dockerfile**
   ```dockerfile
   FROM mcr.microsoft.com/windows/servercore:ltsc2022
   RUN powershell -Command Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force
   RUN powershell -Command Install-Module -Name PowerShellGet -Force
   RUN powershell -Command Install-Module -Name Python -Force
   ```

3. **运行Docker容器打包**
   ```bash
   docker run -v $(pwd):/app -w /app mcr.microsoft.com/windows/servercore:ltsc2022 powershell -Command "python -m pip install pyinstaller && pyinstaller wjx2.spec"
   ```

### 方案三：使用wine（实验性）

通过wine模拟Windows环境，但成功率较低。

#### 步骤：

1. **安装wine**
   ```bash
   brew install wine
   ```

2. **安装Python到wine**
   ```bash
   wine python-3.10.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
   ```

3. **使用wine运行pyinstaller**
   ```bash
   wine pyinstaller wjx2.spec
   ```

## 📦 推荐方案：GitHub Actions

### 配置文件示例

```yaml
name: Build Windows Executable

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Build with PyInstaller
      run: pyinstaller --clean wjx2.spec
    
    - name: Upload artifact
      uses: actions/upload-artifact@v4
      with:
        name: windows-executable
        path: dist/问卷星自动填写工具.exe
```

## 🎯 操作指南

### 快速开始GitHub Actions

1. **创建仓库**
   - 访问 https://github.com/new
   - 命名为 `wjx-auto-fill`
   - 选择 `Add a README file`

2. **上传文件**
   - 上传所有项目文件
   - 包括 `wjx2.py`, `slider_handler.py`, `requirements.txt`, `wjx2.spec`

3. **创建workflow**
   - 点击 `Actions` 标签
   - 选择 `set up a workflow yourself`
   - 粘贴上述配置
   - 保存为 `.github/workflows/build.yml`

4. **触发构建**
   - 推送代码
   - 等待约5分钟
   - 在 `Actions` 标签下载结果

## 📊 对比表

| 方案 | 优点 | 缺点 | 成功率 |
|------|------|------|--------|
| GitHub Actions | 免费、可靠、自动 | 需要GitHub账号 | 100% |
| Docker | 本地运行、灵活 | 配置复杂 | 90% |
| wine | 快速、无需网络 | 不稳定、依赖多 | 60% |

## 🎉 推荐选择

**强烈推荐使用GitHub Actions**，这是目前最可靠的方案，完全免费且无需本地Windows环境。

## 📝 注意事项

1. **GitHub Actions限制**
   - 每月免费额度：2000分钟
   - 足够打包约200次

2. **文件大小**
   - 生成的.exe文件约50-100MB
   - 包含所有依赖

3. **兼容性**
   - 支持Windows 7/8/10/11
   - 需要安装Chrome浏览器

## 📞 技术支持

如有问题，请参考：
- GitHub Actions文档：https://docs.github.com/actions
- PyInstaller文档：https://pyinstaller.org/

## 🎯 下一步操作

1. **创建GitHub仓库**
2. **配置GitHub Actions**
3. **下载生成的.exe文件**
4. **分发给Windows用户**

通过GitHub Actions，您可以在macOS上轻松生成Windows .exe文件，无需Windows电脑！
