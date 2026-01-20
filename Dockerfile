# 1. Imagem base (Python leve)
FROM python:3.9-slim

# 2. Definir pasta de trabalho dentro do container
WORKDIR /app

# 3. Copiar apenas o arquivo de requisitos primeiro (para aproveitar o cache do Docker)
COPY requirements.txt .

# 4. Instalar as bibliotecas
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar o restante dos arquivos (app.py, gerar_modelo.py) para dentro do container
COPY . .

# 6. IMPORTANTE: Treinar o modelo DENTRO do container na hora do build
# Isso garante que o arquivo .pkl exista e seja compatível com o Linux do container
RUN python gerar_modelo.py

# 7. Expor a porta padrão do Streamlit
EXPOSE 8501

# 8. Comando para iniciar o site
# --server.address=0.0.0.0 é CRUCIAL no Docker para o host conseguir acessar
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]