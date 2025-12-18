# 问卷星自动填写脚本（基于Selenium的Python版本）

## 功能介绍

本脚本是基于Selenium的Python版本问卷星自动填写工具，可定制每个选项比例概率，支持单选、多选、填空、量表、下拉框等题型。

## 原JS脚本信息

- 名称：问卷星(定制比例)模板（2025最新版！！！）
- 版本：4.8
- 作者：ZYY
- 适配网址：`https://www.wjx.cn/vm/*`, `https://www.wjx.cn/vj/*` 等问卷星链接

## 转换后的Python脚本特性

1. 使用Selenium WebDriver模拟浏览器行为
2. 支持根据比例概率选择选项
3. 处理各种题型：单选、多选、填空、量表、下拉框
4. 自动处理提交问卷和安全校验
5. 支持清除Cookie
6. 提供详细的日志输出

## 安装依赖

1. 确保已安装Python 3.7或更高版本
2. 安装所需依赖：

```bash
pip install -r requirements.txt
```

## 使用说明

1. **修改问卷URL**：在`wjx_autofill.py`文件中找到以下代码，修改为你要填写的问卷URL：

```python
# 填写问卷的网址
wenjuan_url = 'https://v.wjx.cn/vm/h9RwweO.aspx'
```

2. **修改选项比例**：根据需要修改各个问题的选项比例，例如：

```python
# 2. 性别 - 男生41%，女生59%
ops = lists[self.ccc].find_elements(By.TAG_NAME, "div")
self.ccc += 1
bili = [41, 59]  # 男生41%，女生59%
ops[self.danxuan(bili)].click()
```

3. **运行脚本**：

```bash
python wjx_autofill.py
```

4. **查看结果**：脚本运行时会打开Chrome浏览器，自动填写问卷并提交，最后会在控制台输出填写结果。

## 注意事项

1. 确保已安装Chrome浏览器
2. 首次运行时会自动下载ChromeDriver
3. 部分问卷可能需要手动处理验证码
4. 脚本运行时不要关闭浏览器窗口
5. 请遵守问卷星的使用规则，不要滥用脚本

## 脚本结构

- `wjx_autofill.py`：主脚本文件，包含所有填写逻辑
- `requirements.txt`：依赖项列表
- `README.md`：使用说明

## 核心功能说明

### 1. 比例随机选择算法

```python
def danxuan(self, bili):
    """根据比例随机选择选项"""
    rand = random.random() * 100
    total = 0
    for i, percent in enumerate(bili):
        total += percent
        if rand < total:
            return i
    return len(bili) - 1
```

### 2. 各种题型处理

- **单选题**：根据比例随机选择一个选项
- **多选题**：根据比例随机选择多个选项（最多选三项）
- **填空题**：根据预设规则生成填写内容
- **量表题**：根据预设规则选择评分
- **下拉框**：点击下拉框并选择选项

### 3. 安全校验处理

脚本会自动处理问卷星的安全校验弹窗，包括：
- 查找并点击确认按钮
- 处理阿里云验证码弹窗
- 处理各种验证元素

## 常见问题

1. **Q**: 脚本运行时提示找不到ChromeDriver怎么办？
   **A**: 确保已安装最新版本的Chrome浏览器，脚本会自动下载匹配的ChromeDriver。

2. **Q**: 脚本运行时浏览器自动关闭怎么办？
   **A**: 脚本运行完成后会自动关闭浏览器，如需保持浏览器打开，可以修改`run`方法中的`time.sleep(10)`为更长时间。

3. **Q**: 问卷填写过程中出错怎么办？
   **A**: 查看控制台输出的错误信息，根据错误提示调整脚本逻辑。

4. **Q**: 如何修改填写速度？
   **A**: 可以调整脚本中的`time.sleep()`参数，增加或减少等待时间。

## 免责声明

本脚本仅供学习和研究使用，请勿用于商业用途或违反问卷星使用规则的行为。使用本脚本造成的任何后果由使用者自行承担。
