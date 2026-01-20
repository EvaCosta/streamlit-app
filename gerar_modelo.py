import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor

# 1. Gerar dados simulados
np.random.seed(42)
n = 1000
df = pd.DataFrame({
    'Ano': np.random.randint(2010, 2025, n),
    'KM': np.random.randint(0, 150000, n),
    'Potencia': np.random.randint(70, 250, n) # Cavalos
})

# Lógica de preço
df['Preco'] = 50000 + (df['Ano']-2010)*2000 - (df['KM']*0.15) + (df['Potencia']*150)
df['Preco'] += np.random.normal(0, 2000, n) # Ruído

# 2. Treinar
modelo = RandomForestRegressor(n_estimators=100, random_state=42)
modelo.fit(df[['Ano', 'KM', 'Potencia']], df['Preco'])

# 3. Salvar
joblib.dump(modelo, 'modelo_carros.pkl')
print("✅ Modelo salvo como 'modelo_carros.pkl'")