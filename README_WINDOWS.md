# Windows打包快速指南

## 🎯 目标
将Python脚本打包成Windows可执行文件（.exe），无需安装Python即可运行。

## 📋 步骤

### 1. 准备工作
- ✅ 将整个项目文件夹复制到Windows电脑
- ✅ 确保Windows电脑已安装Python 3.8+
- ✅ 确保Windows电脑已安装Chrome浏览器

### 2. 一键打包
在Windows电脑上：
1. 双击运行 `build_windows.bat`
2. 等待自动完成（约2-5分钟）
3. 在 `dist` 文件夹中找到 `问卷星自动填写工具.exe`

### 3. 使用程序
- 双击 `问卷星自动填写工具.exe` 即可运行
- 首次运行会自动下载ChromeDriver（需要网络）
- 无需安装任何Python依赖

## ⚠️ 常见问题

**Q: 提示"找不到Python"**
A: 请先安装Python 3.8+，下载地址：https://www.python.org/downloads/

**Q: Windows安全警告**
A: 点击"更多信息" → "仍要运行"

**Q: 打包失败**
A: 确保网络连接正常，可能需要下载依赖包

## 📚 详细文档
查看 `BUILD_GUIDE.md` 获取完整说明。
