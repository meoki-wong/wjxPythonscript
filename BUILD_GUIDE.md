# 问卷星自动填写工具 - 打包说明

## 📦 打包方案

本工具使用 **PyInstaller** 将Python脚本打包成独立的可执行文件，无需安装Python环境即可运行。

## 🎯 支持平台

- ✅ **Windows** (推荐) - 生成 `.exe` 可执行文件
- ✅ **macOS** - 生成可执行文件
- ⚠️ **Linux** - 需要额外配置

## 📋 前置要求

### Windows系统
1. 安装 **Python 3.8+** (推荐 3.10)
   - 下载地址: https://www.python.org/downloads/
   - 安装时勾选 "Add Python to PATH"

2. 安装 **Chrome浏览器**
   - 下载地址: https://www.google.com/chrome/

### macOS系统
1. 安装 **Python 3.8+**
   ```bash
   brew install python3
   # 或从官网下载: https://www.python.org/downloads/
   ```

2. 安装 **Chrome浏览器**
   - 下载地址: https://www.google.com/chrome/

## 🚀 快速打包

### 方式一：Windows系统打包（推荐）

1. 将项目文件夹复制到Windows电脑
2. 双击运行 `build_windows.bat`
3. 等待打包完成
4. 在 `dist` 文件夹中找到 `问卷星自动填写工具.exe`

### 方式二：macOS系统打包

1. 打开终端，进入项目目录
2. 运行打包脚本：
   ```bash
   chmod +x build.sh
   ./build.sh
   ```
3. 等待打包完成
4. 在 `dist` 文件夹中找到可执行文件

### 方式三：手动打包

如果自动脚本失败，可以手动执行以下步骤：

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 安装PyInstaller
pip install pyinstaller

# 3. 打包
pyinstaller --clean wjx2.spec
```

## 📁 打包后的文件结构

```
项目文件夹/
├── dist/                          # 打包输出目录
│   └── 问卷星自动填写工具.exe     # Windows可执行文件
│   └── 问卷星自动填写工具         # macOS可执行文件
├── build/                         # 打包临时文件（可删除）
├── wjx2.py                        # 主程序
├── slider_handler.py              # 滑块处理模块
├── requirements.txt               # 依赖列表
├── wjx2.spec                      # PyInstaller配置
├── build_windows.bat              # Windows打包脚本
└── build.sh                       # macOS/Linux打包脚本
```

## 🎮 使用说明

### Windows用户

1. **首次运行**
   - 双击 `问卷星自动填写工具.exe`
   - Windows可能显示安全警告，点击"更多信息" → "仍要运行"
   - 程序会自动下载匹配的ChromeDriver（需要网络连接）

2. **配置问卷链接**
   - 打开 `wjx2.py` 文件
   - 找到 `url` 变量，替换为您的问卷链接
   - 保存后重新打包

3. **运行程序**
   - 双击运行即可，无需安装任何依赖

### macOS用户

1. **首次运行**
   - 在终端中运行：`./dist/问卷星自动填写工具`
   - 程序会自动下载匹配的ChromeDriver（需要网络连接）

2. **配置问卷链接**
   - 打开 `wjx2.py` 文件
   - 找到 `url` 变量，替换为您的问卷链接
   - 保存后重新打包

## ⚙️ 高级配置

### 修改程序名称

编辑 `wjx2.spec` 文件，修改 `name` 参数：

```python
name='您的程序名称',
```

### 添加程序图标

1. 准备 `.ico` 文件（Windows）或 `.icns` 文件（macOS）
2. 编辑 `wjx2.spec` 文件，添加 `icon` 参数：

```python
icon='path/to/icon.ico',  # Windows
# 或
icon='path/to/icon.icns',  # macOS
```

### 隐藏控制台窗口

编辑 `wjx2.spec` 文件，修改 `console` 参数：

```python
console=False,  # 隐藏控制台窗口
```

## 🔧 常见问题

### Q1: 打包失败，提示找不到模块

**解决方案：**
- 确保已安装所有依赖：`pip install -r requirements.txt`
- 检查 `wjx2.spec` 中的 `hiddenimports` 是否包含所有模块

### Q2: 运行时提示找不到ChromeDriver

**解决方案：**
- 确保已安装Chrome浏览器
- 检查网络连接，程序需要自动下载ChromeDriver
- 手动下载ChromeDriver并放到程序同目录

### Q3: Windows安全警告

**解决方案：**
- 点击"更多信息" → "仍要运行"
- 或将程序添加到Windows Defender白名单

### Q4: macOS无法打开

**解决方案：**
```bash
# 给予执行权限
chmod +x dist/问卷星自动填写工具

# 如果提示"无法打开，因为无法验证开发者"
# 在系统偏好设置 → 安全性与隐私 → 通用 → 点击"仍要打开"
```

### Q5: 程序运行缓慢

**解决方案：**
- 确保网络连接正常
- 检查Chrome浏览器版本是否过旧
- 关闭其他占用资源的程序

## 📝 注意事项

1. **首次运行**需要网络连接以下载ChromeDriver
2. **Windows Defender**可能会误报，请添加信任
3. **Chrome浏览器**必须已安装
4. **问卷链接**需要在代码中配置
5. **代理IP**可选，不配置则使用本地IP

## 🔄 更新程序

修改代码后，重新运行打包脚本即可：

```bash
# Windows
build_windows.bat

# macOS/Linux
./build.sh
```

## 📞 技术支持

如有问题，请参考：
- PyInstaller官方文档: https://pyinstaller.org/
- Selenium文档: https://www.selenium.dev/

## 📄 许可证

本工具仅供学习和研究使用，请勿用于商业用途。
