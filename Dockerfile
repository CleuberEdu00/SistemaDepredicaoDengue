# Imagem base para o script (batch job) de predição de dengue.
FROM python:3.11-slim

# Garante que os prints (logs) do Python apareçam na tela imediatamente e não fiquem presos na memória.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Cria e define a pasta principal lá dentro do container
WORKDIR /app

# Instala as bibliotecas primeiro. O Docker é inteligente e salva isso em cache (fica mais rápido da próxima vez).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do seu código (seus arquivos .py) para dentro do container.
COPY . .

# Comando final: executa o script principal do sistema.
CMD ["python", "main.py"]