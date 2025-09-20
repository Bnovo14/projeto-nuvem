# ---- Estágio 1: O Preparador (Builder) ----
# Usamos uma imagem base super leve apenas para guardar os nossos ficheiros.
# Damos um "apelido" a este estágio: "builder"
FROM alpine:latest AS builder

# Definimos o diretório de trabalho
WORKDIR /app

# Copiamos todos os ficheiros da nossa pasta local para dentro do builder
# (index.html, script.js, default.conf)
COPY . .


# ---- Estágio 2: A Versão Final (com Nginx) ----
# Começamos do zero com a imagem oficial e otimizada do Nginx
FROM nginx:stable-alpine

# Copiamos os ficheiros da nossa aplicação (do estágio 'builder')
# para a pasta padrão onde o Nginx serve os ficheiros (/usr/share/nginx/html).
COPY --from=builder /app/ /usr/share/nginx/html

# Copiamos a nossa configuração personalizada do Nginx para o local correto,
# substituindo a configuração padrão. É esta regra que ativa o proxy reverso.
COPY --from=builder /app/default.conf /etc/nginx/conf.d/default.conf

# Expomos a porta 80, que é a porta padrão onde o Nginx escuta.
EXPOSE 80

# A imagem do Nginx já tem um comando padrão para iniciar o servidor,
# por isso não precisamos de adicionar uma linha CMD.
