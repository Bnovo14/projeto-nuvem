# Etapa 1: Escolher a imagem base
# Usaremos uma imagem leve do Node.js, que já tem o 'npm' que precisamos.
FROM node:18-alpine

# Etapa 2: Definir o diretório de trabalho dentro do container
# É como criar uma pasta para o nosso projeto dentro da "caixa".
WORKDIR /app

# Etapa 3: Copiar os arquivos da nossa aplicação para dentro do container
# O primeiro "." significa "tudo o que está na pasta atual" (onde o Dockerfile está).
# O segundo "." significa "para o diretório de trabalho" (/app) que definimos acima.
COPY . .

# Etapa 4: Instalar o servidor web dentro do container
# Usamos o 'serve', o mesmo que usamos para testar localmente.
RUN npm install -g serve

# Etapa 5: Expor a porta que a aplicação vai usar
# Isso informa ao Docker que o container vai "escutar" na porta 8080. 
EXPOSE 8080

# Etapa 6: Definir o comando para iniciar a aplicação
# Quando o container for iniciado, este comando será executado.
# Ele inicia o servidor web na porta 8080, servindo os arquivos da nossa aplicação.
CMD ["serve", "-s", "-l", "8080"]