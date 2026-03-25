FROM python:3.12-slim
LABEL maintainer="Joel Mafra <[joelhenrique78@gmail.com]>"

# Previni a criação de arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1

# Garante que o Python não bufferize a saída
ENV PYTHONUNBUFFERED=1

# Copia os arquivos para o container
COPY ./djangoapp /djangoapp
COPY ./scripts /scripts

# Define o diretório de trabalho
WORKDIR /djangoapp

# Expõe a porta 8000
EXPOSE 8000

# RUN executa comandos em um shell dentro do container para construir a imagem. 
# O resultado da execução do comando é armazenado no sistema de arquivos da 
# imagem como uma nova camada.
# Agrupar os comandos em um único RUN pode reduzir a quantidade de camadas da 
# imagem e torná-la mais eficiente.
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    build-essential \
    postgresql-client \
    curl &&\
    rm -rf /var/lib/apt/lists/* && \
    python -m venv /.venv && \
    /.venv/bin/pip install --upgrade pip && \
    /.venv/bin/pip install -r /djangoapp/requirements.txt && \
    useradd -m -s /bin/bash duser && \
    mkdir -p /data/web/static && \
    mkdir -p /data/web/media && \
    chown -R duser:duser /.venv && \
    chown -R duser:duser /data/web/static && \
    chown -R duser:duser /data/web/media && \
    chmod -R 755 /data/web/static && \
    chmod -R 755 /data/web/media && \
    chmod -R +x /scripts

# Adiciona a pasta scripts e venv/bin 
# no $PATH do container.
ENV PATH="/scripts:/.venv/bin:$PATH"

# Muda o usuário para duser
USER duser

# Executa o arquivo scripts/commands.sh
CMD ["commands.sh"]
