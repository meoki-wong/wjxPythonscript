# 使用Docker在macOS上打包Windows .exe文件

## 🎯 方案说明

通过Docker运行Windows容器，可以在macOS上直接打包生成Windows .exe文件。

## 📋 前置要求

1. **安装Docker Desktop**
   - 下载地址：https://www.docker.com/products/docker-desktop/
   - 启用Windows容器支持（在设置中）

2. **Windows镜像**
   - 需要Windows Server Core镜像

## 🚀 快速开始

### 步骤1：创建Dockerfile

```dockerfile
# 使用Windows Server Core镜像
FROM mcr.microsoft.com/windows/servercore:ltsc2022

# 设置工作目录
WORKDIR /app

# 安装Python
RUN powershell -Command \
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe" -OutFile python.exe; \
    Start-Process -FilePath python.exe -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait; \
    Remove-Item python.exe

# 安装pip
RUN python -m pip install --upgrade pip

# 复制项目文件
COPY . .

# 安装依赖
RUN pip install -r requirements.txt
RUN pip install pyinstaller

# 打包
RUN pyinstaller --clean wjx2.spec
```

### 步骤2：构建Docker镜像

```bash
docker build -t wjx-builder .
```

### 步骤3：运行容器并获取.exe文件

```bash
# 运行容器
docker run --name wjx-build wjx-builder

# 复制.exe文件到本地
docker cp wjx-build:/app/dist/问卷星自动填写工具.exe ./dist/

# 清理容器
docker rm wjx-build
```

## 📦 简化版脚本

### 一键打包脚本

```bash
#!/bin/bash

echo "========================================"
echo "   Docker Windows打包脚本"
echo "========================================"
echo ""

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker未运行，请先启动Docker Desktop"
    exit 1
fi
echo "✅ Docker已运行"
echo ""

# 构建镜像
echo "[1/3] 构建Docker镜像..."
docker build -t wjx-builder .
if [ $? -ne 0 ]; then
    echo "❌ 镜像构建失败"
    exit 1
fi
echo "✅ 镜像构建成功"
echo ""

# 运行容器
echo "[2/3] 运行打包容器..."
docker run --name wjx-build wjx-builder
echo ""

# 复制结果
echo "[3/3] 复制.exe文件..."
mkdir -p dist
docker cp wjx-build:/app/dist/问卷星自动填写工具.exe ./dist/
if [ $? -ne 0 ]; then
    echo "❌ 复制文件失败"
    docker rm wjx-build
    exit 1
fi
echo "✅ .exe文件已复制到dist目录"
echo ""

# 清理
echo "清理容器..."
docker rm wjx-build
echo ""

echo "========================================"
echo "   打包完成！"
echo "========================================"
echo ""
echo "可执行文件位置: dist/问卷星自动填写工具.exe"
echo ""
```

## 📊 优缺点

### 优点
- ✅ 本地运行，无需网络
- ✅ 完全可控
- ✅ 支持自定义配置

### 缺点
- ❌ Docker镜像较大（约10GB）
- ❌ 打包时间较长
- ❌ 需要Windows容器支持

## ⚠️ 注意事项

1. **Docker资源配置**
   - 至少分配4GB内存
   - 至少分配2个CPU核心

2. **镜像大小**
   - Windows镜像约10GB
   - 构建后镜像约15GB

3. **打包时间**
   - 首次构建约30分钟
   - 后续构建约10分钟

## 🎉 总结

使用Docker是在macOS上打包Windows .exe文件的可靠方案，适合需要本地控制的用户。如果您需要更简单的方案，推荐使用GitHub Actions。

## 📞 技术支持

如有问题，请参考：
- Docker文档：https://docs.docker.com/
- Windows容器文档：https://docs.microsoft.com/en-us/virtualization/windowscontainers/
