FROM python:3.9-slim
EXPOSE 8000
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . .
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "server.asgi:application"]

