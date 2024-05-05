# 使用官方Python运行环境
FROM python:3.8-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录下的所有文件到容器的/app目录
COPY . /app

# 安装依赖
RUN pip install -r requirements.txt

# 设置容器对外暴露80端口
EXPOSE 80

# 运行app.py来启动Flask应用
CMD ["python", "app.py"]
