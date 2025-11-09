# Proyecto Python for Data - Análisis de Campañas de Marketing Bancario

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================================================================
# 1. CARGA, INTEGRACIÓN Y TRANSFORMACIÓN INICIAL DE LOS DATOS
# ==============================================================================

# 1.1. Rutas de los archivos
RUTA_CAMPANAS = './DatosProyecto/bank-additional.csv'

# RUTA ÚNICA al archivo Excel, ya que solo es un archivo.
RUTA_DETALLES_EXCEL = './DatosProyecto/customer-details.xlsx'

# Nombres de las hojas (sheets) dentro del archivo Excel.
HOJAS_DETALLES = ['2012', '2013', '2014']


# Cargar el dataset de Campañas (Separador ';')
# Usamos index_col=False para evitar que la columna vacía inicial cause problemas de indexación.
# Y corregimos el separador si el archivo está delimitado por comas (,) en lugar de punto y coma (;)
# Si el separador es ',', usa sep=','
df_campanas = pd.read_csv(RUTA_CAMPANAS, sep=',', low_memory=False, index_col=False) # <--- Cambiado a sep=','

# Cargar y concatenar los datasets de Clientes (LEYENDO LAS HOJAS del .xlsx)
df_clientes = []
for hoja in HOJAS_DETALLES:
    # Usamos la RUTA ÚNICA y el parámetro 'sheet_name' para cargar cada hoja
    df_hoja = pd.read_excel(RUTA_DETALLES_EXCEL, sheet_name=hoja)
    df_clientes.append(df_hoja)

# Concatenar todos los DataFrames de clientes
df_clientes = pd.concat(df_clientes, ignore_index=True)

# 1. Limpiar los nombres de columna en df_clientes (para evitar espacios o mayúsculas)
df_clientes.columns = df_clientes.columns.str.lower().str.strip() 

# 2. Renombrar en df_clientes: Si el nombre de la columna es 'id' (de la original 'ID') y necesitamos 'id_'
# Esto garantiza que el nombre sea 'id_' para la unión, sin importar si el original era 'ID' o 'id'.
if 'id' in df_clientes.columns:
    df_clientes.rename(columns={'id': 'id_'}, inplace=True) 

# NO RENOMBRAMOS df_campanas porque ya confirmaste que tiene 'id_' en su cabecera.

# Unir los dos DataFrames por el identificador único 'id_'
# Esto debería funcionar ahora que 'id_' está en ambos.
df = pd.merge(df_campanas, df_clientes, on='id_', how='inner')

print(f"Dimensiones del DataFrame combinado (filas, columnas): {df.shape}")
print("-" * 50)

# ==============================================================================
# 2. TRANSFORMACIÓN Y LIMPIEZA DE LOS DATOS
# ==============================================================================

print("Iniciando Transformación y Limpieza de Datos...")

# 2.1. Limpieza de columnas con separador decimal ','
columnas_decimal_comma = [
    'emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 'euribor3m'
]
for col in columnas_decimal_comma:
    # Convertir la coma ',' a punto '.' y luego a float
    df[col] = df[col].astype(str).str.replace('"', '').str.replace(',', '.', regex=True).astype(float)

# 2.2. Estandarización de la Variable Objetivo 'y' y binarias
# 'y': Convertir 'yes' a 1 y 'no' a 0
df['y'] = df['y'].map({'yes': 1, 'no': 0})

# Columnas binarias: 'default', 'housing', 'loan'
# Mapeamos a 1/0 y tratamos 'unknown' o valores nulos
columnas_binarias = ['default', 'housing', 'loan']
for col in columnas_binarias:
    # Convertir 'yes' a 1, 'no' a 0, y el resto (incluyendo 'unknown' o nulos) a NaN para imputación/conteo
    df[col] = df[col].astype(str).str.lower().replace({'yes': 1, 'no': 0, 'nan': np.nan, '': np.nan})
    # 'unknown' se encuentra en los snippets de 'default', 'housing' y 'loan'.
    df[col] = df[col].replace({'unknown': np.nan}) 

# 2.3. Manejo de Valores Faltantes (NaN)
print("\nConteo de Nulos antes de la imputación:")
print(df.isnull().sum()[df.isnull().sum() > 0])

# Imputación de variables numéricas: 'age' e 'Income'
# 'age': Rellenar con la mediana
mediana_age = df['age'].median()
df['age'].fillna(mediana_age, inplace=True)


# 'Income': Rellenar con la mediana (la media es sensible a outliers)
mediana_income = df['income'].median()
df['income'].fillna(mediana_income, inplace=True)

# Imputación de variables categóricas ('job', 'marital', 'education')
# Rellenar con la moda o 'unknown' (ya que muchos nulos provienen de la limpieza de 'unknown')
columnas_categoricas_na = ['job', 'marital', 'education']
for col in columnas_categoricas_na:
    df[col].fillna(df[col].mode()[0], inplace=True) # Usamos la moda para simplicidad

# Limpieza final de Nulos en binarias (las que siguen siendo NaN después del mapeo 'unknown')
# En este caso, si quedan NaNs en 'default', 'housing', 'loan', asumimos 'no' (0) o la moda, 
# pero dado el contexto, si no hay información, la opción más segura es la moda
for col in columnas_binarias:
    # Si la columna es numérica (1/0), rellenamos con la moda (que será 0 o 1)
    # 1. Asegurar que los valores sean números (float)
    # errors='coerce' reemplaza cualquier valor no numérico por NaN
    df[col] = pd.to_numeric(df[col], errors='coerce') 

    # 2. Manejar los valores faltantes (NaN)
    # Los NaN no pueden ser enteros. Hay que eliminarlos o reemplazarlos.
    # Opción A (Recomendada): Rellenar NaN con 0 antes de la conversión a int
    df[col].fillna(0, inplace=True) 

    # 3. Convertir a entero
    # Esto solo funciona si NO hay NaN, o si los rellenamos en el paso 2
    df[col] = df[col].astype(int)

# 2.4. Conversión de Fechas
df['dt_customer'] = pd.to_datetime(df['dt_customer'])

# 2.5. Feature Engineering: Clientes 'Antigüedad' (Customer Tenure)
# Calculamos la antigüedad del cliente hasta una fecha reciente de la campaña (e.g., la última fecha en el dataset)
fecha_actual = df['dt_customer'].max()
df['Antiguedad_Dias'] = (fecha_actual - df['dt_customer']).dt.days

# 2.6. Tratamiento de 'duration' y 'pdays'
# 'duration' (duración del contacto) no debe usarse en modelos predictivos (conocido a posteriori), 
# pero es útil para EDA, por lo que se mantiene.
# 'pdays' = 999 significa que el cliente no fue contactado previamente
df['contactado_previamente'] = df['pdays'].apply(lambda x: 0 if x == 999 else 1)
df['pdays_limpio'] = df['pdays'].replace(999, np.nan) # Limpieza para análisis estadístico

print("Limpieza y Transformación finalizadas.")
print("-" * 50)

# ==============================================================================
# 3. ANÁLISIS DESCRIPTIVO DE LOS DATOS
# ==============================================================================

print("Iniciando Análisis Descriptivo...")

# 3.1. Resumen Estadístico de Variables Numéricas Clave
print("\nResumen Estadístico (Numéricas Clave):")
print(df[['age', 'income', 'duration', 'campaign', 'euribor3m', 'y']].describe().T)

# 3.2. Análisis de la Variable Objetivo
tasa_suscripcion = df['y'].mean() * 100
print(f"\n✅ Tasa de Suscripción Global (y=1): {tasa_suscripcion:.2f}%")

# 3.3. Análisis por Segmentos (Tasas de Suscripción)
print("\nTasa de Suscripción por Estado Civil:")
suscripcion_marital = df.groupby('marital')['y'].mean().sort_values(ascending=False)
print(suscripcion_marital)

print("\nTasa de Suscripción por Ocupación (Top 5):")
suscripcion_job = df.groupby('job')['y'].mean().sort_values(ascending=False).head(5)
print(suscripcion_job)

# 3.4. Correlación con la Suscripción ('y')
# Usamos el coeficiente de correlación de Pearson
columnas_correlacion = ['y', 'age', 'income', 'duration', 'campaign', 'euribor3m', 'nr.employed', 'Antiguedad_Dias']


# 1. Corrección de 'income' (reemplazar ',' por '.' y convertir a float)
df['income'] = df['income'].astype(str).str.replace(',', '.', regex=False)
df['income'] = pd.to_numeric(df['income'])


# 2. Corrección de  'nr.employed'
df['nr.employed'] = df['nr.employed'].astype(str).str.replace(',', '.', regex=False)
df['nr.employed'] = pd.to_numeric(df['nr.employed'])


# 3. Ahora el cálculo de correlación debería funcionar:
matriz_corr = df[columnas_correlacion].corr()


print("\nCorrelación de Pearson con la Suscripción ('y'):")
print(matriz_corr['y'].drop('y').sort_values(ascending=False))
print("-" * 50)


# ==============================================================================
# 4. VISUALIZACIÓN DE LOS DATOS
# ==============================================================================

# Configuración de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# 4.1. Visualización: Tasa de Suscripción por Ocupación
plt.figure(figsize=(12, 7))
sns.barplot(x='job', y='y', data=df, palette='viridis', errorbar=None)
plt.title('Tasa de Suscripción por Ocupación', fontsize=16)
plt.xlabel('Ocupación', fontsize=12)
plt.ylabel('Tasa de Suscripción (Promedio de Y=1)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 4.2. Visualización: Impacto de la Campaña (Número de Contactos)
df_campaign_agg = df.groupby('campaign')['y'].agg(['mean', 'count']).reset_index()
# Filtramos para visualizar solo el rango relevante de contactos
df_campaign_agg = df_campaign_agg[df_campaign_agg['count'] > 100] 

fig, ax1 = plt.subplots(figsize=(12, 7))

# Tasa de suscripción (Línea)
color = 'tab:blue'
ax1.set_xlabel('Número de Contactos en la Campaña')
ax1.set_ylabel('Tasa de Suscripción', color=color)
ax1.plot(df_campaign_agg['campaign'], df_campaign_agg['mean'], color=color, marker='o')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xlim(0, 15)

# Frecuencia de contactos (Barras)
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Frecuencia de Clientes Contactados', color=color)
ax2.bar(df_campaign_agg['campaign'], df_campaign_agg['count'], color=color, alpha=0.3)
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Tasa de Suscripción vs. Frecuencia de Contactos de Campaña', fontsize=16)
fig.tight_layout()
plt.show()

# 4.3. Visualización: Distribución de Ingresos según Suscripción
plt.figure(figsize=(10, 6))
sns.boxplot(x='y', y='income', data=df, palette=['salmon', 'lightgreen'])
plt.title('Distribución de Ingresos según Suscripción', fontsize=16)
plt.xlabel('Suscripción (0: No, 1: Sí)', fontsize=12)
plt.ylabel('Ingreso Anual', fontsize=12)
# Limitamos el eje Y para mejor visualización (excluir outliers extremos)
plt.ylim(0, df['income'].quantile(0.95))
plt.show()

