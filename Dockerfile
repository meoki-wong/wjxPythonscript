# 使用Windows Server Core镜像
FROM mcr.microsoft.com/windows/servercore:ltsc2022

# 设置工作目录
WORKDIR /app

# 安装Python 3.10.0
RUN powershell -Command \
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe" -OutFile python.exe; \
    Start-Process -FilePath python.exe -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait; \
    Remove-Item python.exe

# 升级pip
RUN python -m pip install --upgrade pip

# 复制项目文件
COPY . .

# 安装依赖
RUN pip install -r requirements.txt
RUN pip install pyinstaller

# 打包
RUN pyinstaller --clean wjx2.spec
