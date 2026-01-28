# Docker打包Windows .exe文件使用指南

## 📋 准备工作

### 1. 安装Docker Desktop

**下载地址：** https://www.docker.com/products/docker-desktop/

**安装步骤：**
1. 双击下载的.dmg文件
2. 将Docker图标拖到Applications文件夹
3. 启动Docker Desktop

### 2. 切换到Windows容器模式

Docker默认使用Linux容器，需要切换到Windows容器：

1. 点击Docker图标（右上角菜单栏）
2. 选择 "Settings"（设置）
3. 点击 "General"（通用）
4. 勾选 "Use the WSL 2 based engine"（如果使用WSL2）
5. 重启Docker
6. 再次点击Docker图标，选择 "Switch to Windows containers..."

### 3. 配置资源

Docker需要足够的资源来运行Windows容器：

1. 点击Docker图标
2. 选择 "Settings" → "Resources"（资源）
3. 分配至少4GB内存和2个CPU核心
4. 应用设置并重启Docker

## 🚀 一键打包

### 方式一：使用一键脚本（推荐）

```bash
# 进入项目目录
cd "/Users/wangshan/Desktop/wjx 2"

# 运行一键打包脚本
./docker_build.sh
```

### 方式二：手动执行

```bash
# 1. 构建Docker镜像
docker build -t wjx-builder .

# 2. 运行容器打包
docker run --name wjx-build wjx-builder

# 3. 复制.exe文件到本地
docker cp wjx-build:/app/dist/问卷星自动填写工具.exe ./dist/

# 4. 清理容器
docker rm wjx-build
```

## 📊 打包时间预估

| 步骤 | 时间 | 说明 |
|------|------|------|
| 下载Windows镜像 | 10-30分钟 | 首次需要下载约10GB镜像 |
| 构建Docker镜像 | 5-15分钟 | 安装Python和依赖 |
| 运行打包 | 5-10分钟 | PyInstaller打包 |
| **总计** | **20-55分钟** | **首次打包较慢** |

## ⚠️ 常见问题

### 问题1：Docker未运行

```
❌ Docker未运行，请先启动Docker Desktop
```

**解决方案：**
- 启动Docker Desktop
- 等待Docker完全加载（图标显示为稳定状态）

### 问题2：容器模式不匹配

```
⚠️  检测到Linux容器模式
请在Docker Desktop设置中切换到Windows容器模式
```

**解决方案：**
- 点击Docker图标
- 选择 "Switch to Windows containers..."
- 等待Docker重启

### 问题3：内存不足

```
Error response from daemon: Insufficient memory to start container
```

**解决方案：**
- 增加Docker的内存分配（至少4GB）
- 关闭其他占用内存的应用

### 问题4：网络问题

```
Invoke-WebRequest : 无法连接到远程服务器
```

**解决方案：**
- 检查网络连接
- 尝试更换Python版本
- 手动下载Python安装包

## 📦 打包结果

成功后，.exe文件将位于：
```
dist/问卷星自动填写工具.exe
```

## 🎯 下一步

1. **启动Docker Desktop**
2. **切换到Windows容器模式**
3. **运行一键打包脚本**
4. **获取生成的.exe文件**

## 📞 技术支持

如果遇到问题，请参考：
- Docker官方文档：https://docs.docker.com/
- Windows容器文档：https://docs.microsoft.com/en-us/virtualization/windowscontainers/

## 🎉 总结

使用Docker可以在macOS上直接打包生成Windows .exe文件，无需Windows电脑。首次打包可能较慢，但后续打包会更快。

祝您打包成功！
