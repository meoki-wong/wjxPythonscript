#!/bin/bash

echo "========================================"
echo "   问卷星自动填写工具 - 打包脚本"
echo "========================================"
echo ""

VENV_DIR="venv_build"
PYI_CACHE_DIR="./pyinstaller_cache"

echo "[1/7] 检查Python环境..."
python3 --version
if [ $? -ne 0 ]; then
    echo "错误: 未找到Python3，请先安装Python 3.8+"
    exit 1
fi
echo "✓ Python环境正常"
echo ""

echo "[2/7] 创建PyInstaller缓存目录..."
mkdir -p "$PYI_CACHE_DIR"
export PYINSTALLER_CONFIG_DIR="$PYI_CACHE_DIR"
echo "✓ 缓存目录创建成功: $PYI_CACHE_DIR"
echo ""

echo "[3/7] 创建虚拟环境..."
if [ -d "$VENV_DIR" ]; then
    echo "虚拟环境已存在，删除旧环境..."
    rm -rf "$VENV_DIR"
fi
python3 -m venv "$VENV_DIR"
if [ $? -ne 0 ]; then
    echo "错误: 创建虚拟环境失败"
    exit 1
fi
echo "✓ 虚拟环境创建成功"
echo ""

echo "[4/7] 激活虚拟环境..."
source "$VENV_DIR/bin/activate"
echo "✓ 虚拟环境已激活"
echo ""

echo "[5/7] 升级pip..."
pip install --upgrade pip
echo ""

echo "[6/7] 安装依赖包..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "错误: 依赖包安装失败"
    deactivate
    exit 1
fi
echo "✓ 依赖包安装完成"
echo ""

echo "[7/8] 安装PyInstaller..."
pip install pyinstaller
if [ $? -ne 0 ]; then
    echo "错误: PyInstaller安装失败"
    deactivate
    exit 1
fi
echo "✓ PyInstaller安装完成"
echo ""

echo "[8/8] 开始打包..."
echo "正在使用PyInstaller打包程序..."
pyinstaller wjx2.spec
if [ $? -ne 0 ]; then
    echo "错误: 打包失败"
    deactivate
    exit 1
fi
echo ""

echo "清理虚拟环境..."
deactivate
echo "✓ 虚拟环境已退出"
echo ""

echo "========================================"
echo "   打包完成！"
echo "========================================"
echo ""
echo "可执行文件位置: dist/问卷星自动填写工具"
echo ""
echo "注意事项:"
echo "1. macOS版本: 直接运行 dist/问卷星自动填写工具"
echo "2. Windows版本: 需要在Windows系统上运行 build_windows.bat"
echo "3. 确保电脑上已安装Chrome浏览器"
echo "4. 首次运行时，程序会自动下载匹配的ChromeDriver"
echo "5. 运行前请确保网络连接正常"
echo ""
