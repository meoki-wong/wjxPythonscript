@echo off
chcp 65001 >nul
echo ========================================
echo    问卷星自动填写工具 - Windows打包脚本
echo ========================================
echo.

echo [1/5] 检查Python环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)
echo ✓ Python环境正常
echo.

echo [2/5] 升级pip...
python -m pip install --upgrade pip
echo.

echo [3/5] 安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo 错误: 依赖包安装失败
    pause
    exit /b 1
)
echo ✓ 依赖包安装完成
echo.

echo [4/5] 安装PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo 错误: PyInstaller安装失败
    pause
    exit /b 1
)
echo ✓ PyInstaller安装完成
echo.

echo [5/5] 开始打包...
echo 正在使用PyInstaller打包程序...
pyinstaller --clean wjx2.spec
if errorlevel 1 (
    echo 错误: 打包失败
    pause
    exit /b 1
)
echo.

echo ========================================
echo    打包完成！
echo ========================================
echo.
echo 可执行文件位置: dist\问卷星自动填写工具.exe
echo.
echo 注意事项:
echo 1. 首次运行时，Windows可能会提示安全警告，请点击"更多信息"然后"仍要运行"
echo 2. 确保Windows电脑上已安装Chrome浏览器
echo 3. 首次运行时，程序会自动下载匹配的ChromeDriver
echo 4. 运行前请确保网络连接正常
echo.
pause
