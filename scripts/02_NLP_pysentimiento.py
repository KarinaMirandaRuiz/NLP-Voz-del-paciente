import pandas as pd
from pysentimiento import create_analyzer

# -- Carga datos --

df_reviews = pd.read_csv(r'data/data.csv')

# -- Análisis --

# Definimos emociones y sentimientos en español
sentiment_analyzer = create_analyzer(task='sentiment', lang='es')
emotion_analyzer = create_analyzer(task='emotion', lang='es')

# Función para predecir emociones y sentimientos de los comentarios
def analizar_fila(texto):
    
    # si no hay texto, no calcula nada
    if not isinstance(texto, str) or texto.strip() == '':
        return None, None, None, None, None
    
    # predicción de emociones y sentimientos
    sent = sentiment_analyzer.predict(texto)
    emot = emotion_analyzer.predict(texto)
    
    return (
        sent.output,                    # POS, NEG, NEU
        sent.probas.get('POS', 0),      # probabilidad de tener una sentimiento positivo
        sent.probas.get('NEG', 0),      # probabilidad de tener un sentimiento negativo
        emot.output,                    # joy, anger, sadness...
        max(emot.probas.values())       # score de la emoción dominante
    )

# Cálculo de emociones y sentimientos a datos scrapeados
resultados = df_reviews['clean_review_text'].apply(analizar_fila)

df_reviews[['sentimiento', 'score_pos', 'score_neg', 
            'emocion', 'score_emocion']] = pd.DataFrame(
    resultados.tolist(), index=df_reviews.index
)

# -- Guarda datos --

df_reviews.to_csv('data/reviews_pysentimiento.csv', index=False, encoding='utf-8-sig')
print('✅Datos guardados en: data/reviews_pysentimiento.csv')
print(df_reviews[['sentimiento', 'score_pos', 'score_neg', 'emocion', 'score_emocion']].head(2))