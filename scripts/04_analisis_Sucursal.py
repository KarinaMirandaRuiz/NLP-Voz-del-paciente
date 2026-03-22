import pandas as pd

# -- Carga datos --

df_reviews = pd.read_csv('data/reviews_con_sentimiento.csv', encoding='utf-8-sig')

# -- Agrupado por sucursal --
resumen_sucursal = df_reviews.groupby(['SucursalID', 'Sucursal', 'x', 'y']).agg(
    total_reviews          = ('review_id', 'count'),
    total_reviews_pos      = ('sentimiento', lambda x: (x == 'POS').sum()),
    total_reviews_neg      = ('sentimiento', lambda x: (x == 'NEG').sum()),
    total_reviews_neu      = ('sentimiento', lambda x: (x == 'NEU').sum()),
    rating_promedio        = ('rating', 'mean'),
    likes_totales          = ('likes', 'sum'),
    score_positivo_prom    = ('score_pos', 'mean'),
    score_negativo_prom    = ('score_neg', 'mean'),
    emocion_frecuente      = ('emocion', lambda x: x.value_counts().index[0]),
    pct_positivos          = ('sentimiento', lambda x: (x == 'POS').mean() * 100),
    pct_negativos          = ('sentimiento', lambda x: (x == 'NEG').mean() * 100),
    pct_neutros            = ('sentimiento', lambda x: (x == 'NEU').mean() * 100),
).reset_index()



# score_positivo_prom → qué tan positivos son los comentarios en promedio
# pct_positivos → qué porcentaje de comentarios fueron clasificados como positivos

# Índice general de sentimientos: media ponderada poniendo el score negativo en valores negativos
resumen_sucursal['indice_sentimientos'] = (
    (resumen_sucursal['score_positivo_prom'] * resumen_sucursal['total_reviews_pos'])
    - (resumen_sucursal['score_negativo_prom'] * resumen_sucursal['total_reviews_neg'])
) / (resumen_sucursal['total_reviews_pos'] + resumen_sucursal['total_reviews_neg'])

# Redondea
resumen_sucursal[['rating_promedio','score_positivo_prom', 'score_negativo_prom'
                  ,'pct_positivos','pct_negativos','pct_neutros'
                  ]] = round(
                      resumen_sucursal[['rating_promedio','score_positivo_prom', 'score_negativo_prom'
                                        ,'pct_positivos','pct_negativos','pct_neutros']],2)

# print(f'Mínimo: {resumen_sucursal['indice_sentimientos'].min():.3f}')
# print(f'Máximo: {resumen_sucursal['indice_sentimientos'].max():.3f}')
# print(f'Promedio: {resumen_sucursal['indice_sentimientos'].mean():.3f}')

# -- Guarda datos --
resumen_sucursal.to_csv('data/resumen_por_sucursal.csv', index=False, encoding='utf-8-sig')
print('✅Datos guardados en: data/resumen_por_sucursal.csv')
