# arquivo: app.py
import streamlit as st
import joblib
import pandas as pd
import numpy as np


# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Preditor de Preços Auto",
    page_icon="🚗",
)

# --- CARREGAR O MODELO ---
# Usamos @st.cache_resource para não carregar o modelo a cada clique (fica mais rápido)
@st.cache_resource
def carregar_modelo():
    try:
        return joblib.load('modelo_carros.pkl')
    except:
        return None

modelo = carregar_modelo()

# --- CABEÇALHO ---
st.title("🚗 Quanto vale o seu carro?")
st.markdown("Use a inteligência artificial para estimar o preço de venda.")
st.divider() # Linha divisória

# --- COLUNA ESQUERDA (INPUTS) ---
# Vamos criar duas colunas para ficar bonito visualmente
col1, col2 = st.columns(2)

with col1:
    st.subheader("Características")
    
    # Input Numérico
    ano = st.number_input("Ano de Fabricação", min_value=2010, max_value=2025, value=2018)
    
    # Slider (Barra deslizante)
    km = st.slider("Quilometragem (KM)", min_value=0, max_value=200000, value=50000, step=1000)
    
    # Selectbox (Menu suspenso - simulando potência comum)
    potencia = st.slider("Potência do Motor (Cavalos)", 70, 300, 120)

# --- LÓGICA DE PREVISÃO ---
if modelo:
    # Criar o DataFrame com os dados do usuário (Mesmas colunas do treino!)
    dados_input = pd.DataFrame({
        'Ano': [ano],
        'KM': [km],
        'Potencia': [potencia]
    })
    
    # Fazer a previsão
    preco_estimado = modelo.predict(dados_input)[0]
    
    # --- COLUNA DIREITA (RESULTADO) ---
    with col2:
        st.subheader("Avaliação da IA")
        st.write("Com base no mercado atual, seu carro vale:")
        
        # Exibir em grande estilo
        st.metric(label="Preço Estimado", value=f"R$ {preco_estimado:,.2f}")
        
        # Um gráfico simples para "enfeitar"
        st.caption("Comparativo de desvalorização por KM:")
        chart_data = pd.DataFrame({
            'KM': np.linspace(0, 200000, 20),
            'Preco_Simulado': [preco_estimado - (x * 0.15) for x in range(20)]
        })
        st.line_chart(chart_data, y='Preco_Simulado')

else:
    st.error("Erro: Modelo 'modelo_carros.pkl' não encontrado. Rode o script de treino primeiro!")

# --- RODAPÉ ---
st.divider()
st.caption("Desenvolvido com Python & Streamlit")