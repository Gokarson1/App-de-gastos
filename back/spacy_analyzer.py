import spacy
nlp = spacy.load("es_core_news_sm")

def analyze_text_with_spacy(texts):
    gastos_keywords = ['pago', 'compra', 'factura', 'debito', 'retiro', 'consumo', 'transferencia', 'gasto']
    gastos_detectados = []

    for text in texts:
        doc = nlp(text.lower())
        for token in doc:
            if token.text in gastos_keywords:
                gastos_detectados.append(text)
                break

    return gastos_detectados