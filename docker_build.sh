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

# 检查是否启用Windows容器
if ! docker info | grep -q "Windows"; then
    echo "⚠️  检测到Linux容器模式"
    echo "请在Docker Desktop设置中切换到Windows容器模式"
    echo ""
    read -p "是否继续？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
echo "✅ 容器模式检查通过"
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
echo "注意事项:"
echo "1. 首次运行时，Windows可能会提示安全警告，请点击\"更多信息\"然后\"仍要运行\""
echo "2. 确保Windows电脑上已安装Chrome浏览器"
echo "3. 首次运行时，程序会自动下载匹配的ChromeDriver"
echo "4. 运行前请确保网络连接正常"
echo ""
