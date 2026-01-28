# GitHub Actions下载报错修复指南

## 🐛 问题描述

下载GitHub Actions生成的文件时出现错误：
```xml
<Error> 
  <Code>InvalidQueryParameterValue</Code> 
  <Message>Value for one of the query parameters specified in the request URI is invalid.</Message> 
  <QueryParameterName>rscd</QueryParameterName> 
  <QueryParameterValue>attachment; filename="问卷星自动填写工具-Windows.zip"</QueryParameterValue> 
  <Reason>HTTP query parameter values contain invalid characters</Reason> 
</Error>
```

## 🎯 问题原因

文件名中包含了**中文字符**和**空格**，导致HTTP查询参数解析失败。GitHub Actions的artifact下载链接对文件名有严格限制。

## 🚀 修复方案

### 方案一：修改文件名（推荐）

将文件名改为纯英文字符，避免中文字符和空格。

#### 已修改的文件：

1. **[.github/workflows/build.yml](file:///Users/wangshan/Desktop/wjx%202/.github/workflows/build.yml)** - 添加了重命名步骤
2. **[wjx2.spec](file:///Users/wangshan/Desktop/wjx%202/wjx2.spec)** - 修改了生成的可执行文件名

### 方案二：使用zip压缩（备选）

如果需要保留中文文件名，可以使用zip压缩后上传。

```yaml
- name: Zip executable
  run: |
    powershell Compress-Archive -Path "dist/问卷星自动填写工具.exe" -DestinationPath "dist/wjx-auto-fill.zip"

- name: Upload artifact
  uses: actions/upload-artifact@v4
  with:
    name: windows-executable
    path: dist/wjx-auto-fill.zip
```

## 📋 修复后的配置

### GitHub Actions配置

```yaml
- name: Rename executable
  run: |
    ren "dist/问卷星自动填写工具.exe" "wjx-auto-fill.exe"

- name: Upload artifact
  uses: actions/upload-artifact@v4
  with:
    name: windows-executable
    path: dist/wjx-auto-fill.exe
```

### PyInstaller配置

```python
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='wjx-auto-fill',  # 修改为英文文件名
    debug=False,
    # ... 其他配置
)
```

## 🎯 效果

修复后，文件名变为：
- **wjx-auto-fill.exe** - 可执行文件
- **windows-executable.zip** - 下载的压缩包

这样可以避免HTTP查询参数解析错误，顺利下载文件。

## 📦 其他注意事项

1. **文件名限制**
   - 避免使用中文字符、空格和特殊字符
   - 推荐使用小写字母、数字和连字符

2. **下载方式**
   - 修复后可以直接下载.exe文件
   - 也可以下载zip压缩包

3. **兼容性**
   - 英文文件名在所有系统中都能正常工作
   - 避免编码问题

## 🎉 总结

通过将文件名改为纯英文字符，可以解决GitHub Actions下载报错的问题。我已经为您修改了配置文件，现在可以正常下载生成的Windows可执行文件。
