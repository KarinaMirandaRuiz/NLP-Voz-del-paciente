import sqlite3
import pandas as pd
import re
import json

# -- Carga datos --
# Conectar a la base de datos del scraping
conn = sqlite3.connect(r'google-reviews-scraper-pro/reviews.db')

# Cargar CSV con nombre de sucursales y URL, y se pasa a SQL
df_sucursales = pd.read_csv(r'data/url.csv')
df_sucursales.to_sql('sucursales_tmp', conn, if_exists='replace', index=False)

# -- Join --

# places: place_id del lugar (asignado por Scraper), coordenadas y url
# reviews: place_id y comentatios
# sucursales_tmp: SucursalID, Nombre de la sucursal y url usada para el craper

query = '''
    SELECT 
        s.SucursalID, s.Sucursal, s.Direccion, s.URL
        ,r.*, p.latitude as x, p.longitude as y
    FROM reviews r
    INNER JOIN places p
        ON r.place_id = p.place_id
    INNER JOIN sucursales_tmp s
        ON p.original_url = s.url
'''

# Se converte en df pandas
df_reviews = pd.read_sql(query, conn)
df_reviews.head()

# -- Limpieza --

# Función para limpiar tipo JSON
def extraer_texto(x, key1='en', key2 = 'text'):
    try:
        data = json.loads(x)
        # Si es {'en': {'text': '...'}}
        if isinstance(data.get(key1), dict):
            return data[key1].get(key2, '')
        # Si es {'en': 'texto simple'}
        return data.get(key1, '')
    except:
        return x

# Función para limpar texto Natural languaje proecessing
def limpiar_nlp(texto):
    texto = str(texto)
    texto = texto.lower()
    # quitar saltos de linea
    texto = re.sub(r'\s+', ' ', texto)
    # quitar urls
    texto = re.sub(r'http\S+', '', texto)
    # quitar simbolos
    texto = re.sub(r'[^a-záéíóúñü\s!?]', '', texto)
    texto = texto.strip()
    texto = texto.upper()
    return re.sub(r' +', ' ', texto).strip()

# Limpieza de comentarios en una nueva columna
df_reviews['clean_review_text'] = (
    df_reviews['review_text']
    .apply(extraer_texto)
    .apply(limpiar_nlp)
)

# Limpieza de respuestas de dueño en una nueva columna
df_reviews['clean_owner_responses'] = (
    df_reviews['owner_responses']
    .apply(extraer_texto)
    .apply(limpiar_nlp)
    .str.replace('\U0001f49a', 'Green_Heart', regex=False)
    .str.replace('\u2026', 'Right_Pointing', regex=False)
    .str.replace('\U0001f449', 'Right_Pointing', regex=False)
)

# Se eliminan emoticones en respuestas del dueño
df_reviews['owner_responses'] = (df_reviews['owner_responses']
    .str.replace('\U0001f49a', 'Green_Heart', regex=False)
    .str.replace('\u2026', 'Right_Pointing', regex=False)
    .str.replace('\U0001f449', 'Right_Pointing', regex=False)
)

# -- Guarda datos --

data = df_reviews[['SucursalID', 'Sucursal', 'x', 'y', 'URL', 'review_id', 'place_id', 'author', 'rating', 'review_date', 'raw_date', 'likes', 'clean_owner_responses', 'clean_review_text']]

# Guarda los datos limpios
data.to_csv(r'data/data.csv', encoding='utf-8-sig')
print('✅Datos guardados en: data/data.csv')