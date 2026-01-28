#!/bin/bash

echo "========================================"
echo "   使用Docker在macOS上打包Windows .exe"
echo "========================================"
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: 未找到Docker"
    echo ""
    echo "请先安装Docker Desktop for Mac:"
    echo "下载地址: https://www.docker.com/products/docker-desktop/"
    exit 1
fi

echo "✓ Docker已安装"
echo ""

# 检查Docker是否运行
if ! docker info &> /dev/null; then
    echo "❌ 错误: Docker未运行"
    echo ""
    echo "请启动Docker Desktop"
    exit 1
fi

echo "✓ Docker正在运行"
echo ""

# 构建Docker镜像
echo "[1/3] 构建Docker镜像..."
docker build -f Dockerfile.windows -t wjx-windows-builder .
if [ $? -ne 0 ]; then
    echo "❌ 错误: Docker镜像构建失败"
    exit 1
fi
echo "✓ Docker镜像构建成功"
echo ""

# 运行容器进行打包
echo "[2/3] 运行容器进行打包..."
docker run --rm -v "$(pwd)/dist:/app/dist" wjx-windows-builder
if [ $? -ne 0 ]; then
    echo "❌ 错误: 打包失败"
    exit 1
fi
echo "✓ 打包成功"
echo ""

# 检查输出文件
echo "[3/3] 检查输出文件..."
if [ -f "dist/问卷星自动填写工具.exe" ]; then
    echo "✓ Windows可执行文件已生成"
    echo ""
    echo "文件位置: dist/问卷星自动填写工具.exe"
    echo ""
    echo "========================================"
    echo "   打包完成！"
    echo "========================================"
    echo ""
    echo "您现在可以将 dist/问卷星自动填写工具.exe 复制到Windows电脑上运行"
else
    echo "❌ 警告: 未找到可执行文件"
    echo ""
    echo "请检查Docker容器输出"
fi
