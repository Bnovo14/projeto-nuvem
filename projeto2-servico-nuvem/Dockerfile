
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Evitar criação de arquivos pyc e forçar saída não-buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

# Instalar dependências do sistema necessárias para compilar pacotes Python (opcional)
RUN apt-get update \
	&& apt-get install -y --no-install-recommends build-essential gcc \
	&& rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt ./
RUN pip install --upgrade pip \
	&& pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação
COPY . .

# Comando padrão para iniciar a aplicação
CMD ["python", "-u", "main.py"]

