import pandas as pd
import spacy

# -- Carga datos --
df_reviews = pd.read_csv('data/reviews_con_sentimiento.csv', encoding='utf-8-sig')

# -- Modelo de lenguaje en español --
nlp = spacy.load('es_core_news_lg')

# Función para análizar el cometario
def analizar_comentario(texto):
    # Formato para que pueda procesar el texto
    doc = nlp(texto.lower())
    
    # Diccionario para indicar si se habla del tema (puede hablar de varios temas a la vez)
    topicos = {
        'TIEMPO': 0,
        'SERVICIO': 0,
        'ESTUDIOS': 0,
        'CITAS': 0,
        'COSTOS': 0,
        'INSTALACIONES': 0,
        'OPTICA': 0
    }
    
    # Se crean los lemmas para cada tema (raíz de las palabras)
    lemmas_tiempo = {'tarde', 'esperar','demorar', 'fila','hora', 'minuto', 'día',
                     'retraso', 'tardanza','rápido', 'puntualidad','eficiente', 'turno'}

    lemmas_servicio = {'atención', 'servicio','trato', 'personal','gente', 'atender','amable', 'grosero', 'accesibles',
                       'déspota', 'maleducado','amabilidad', 'profesional','recepción', 'turno', 'resultados'}

    lemmas_estudios = {'resultado', 'estudio','análisis', 'examen','entrega', 'muestra',
                       'laboratorio', 'ultrasonido','mastografía', 'resonancia',
                       'tomografía', 'densitometría','rayos x', 'sangre', 'radiología',
                       'incorrecto', 'dolor','calidad', 'toma','error', 'preciso'}

    lemmas_citas = {'cita', 'agendar','turno', 'programar','whatsapp', 'teléfono','reserva', 'llamar',
                    'internet', 'contestar','cancelar', 'sistema'}

    lemmas_costos = {'precio', 'costo','caro', 'barato','cobro', 'pago','factura', 'cobrar',
                     'barato', 'incorrecto','elevado', 'justo','tarjeta', 'accesible','económico'}

    lemmas_instalaciones = {'sucio', 'limpio','baño', 'instalaciones','higiene', 'estacionamiento','lugar',
                            'bonito','organizado', 'moderno','cómodo', 'ordenado','olor', 'feo'}

    lemmas_optica = {'lente', 'lentes','graduación', 'armazón','optometrista', 'taller','vista', 'anteojos','defectuoso'}

    # Revisa cada palabra del comentario para ver si es alguna flexión (token.lemma_) de cada lema (palabra raíz) 
    for token in doc:
        if token.lemma_ in 'lente' and token.pos_ == 'NOUN': # lentes
            topicos['OPTICA'] = 1

        if token.lemma_ == 'lento' and token.pos_ in 'ADJ': # lento
            topicos['TIEMPO'] = 1

        if token.lemma_ in lemmas_tiempo:
            topicos['TIEMPO'] = 1

        if token.lemma_ in lemmas_servicio:
            topicos['SERVICIO'] = 1

        if token.lemma_ in lemmas_estudios:
            topicos['ESTUDIOS'] = 1

        if token.lemma_ in lemmas_citas:
            topicos['CITAS'] = 1

        if token.lemma_ in lemmas_costos:
            topicos['COSTOS'] = 1

        if token.lemma_ in lemmas_instalaciones:
            topicos['INSTALACIONES'] = 1

        if token.lemma_ in lemmas_optica:
            topicos['OPTICA'] = 1

    return list(topicos.values())

# Función para recorrer todos los comentarios y guardar los temas pertenecientes
def analizar_temas(df):

    for i, coment in enumerate(df['clean_review_text']):
        df.loc[i, ['TIEMPO','SERVICIO','ESTUDIOS','CITAS','COSTOS','INSTALACIONES','OPTICA']] = analizar_comentario(coment)
        
    return df

# Se aplica la función para todos los comentarios
df_temas = analizar_temas(df_reviews)

# -- Guarda datos --
 
df_temas.to_csv('data/reviews_con_temas.csv', index=False, encoding='utf-8-sig')
print('✅Datos guardados en: data/reviews_con_temas.csv')