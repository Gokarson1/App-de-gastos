import re
from typing import List, Dict

PALABRAS_CLAVE = [
    "pago", "pagaste", "pagado", "cobro", "cargo",
    "transferencia", "transferido", "retiro", "retirado",
    "compra", "compraste", "débito", "debito", "consumo", "abonado"
]

# Regex mejorada con monedas
PATRON_MONEDA = r'(\$[\s]?\d+(?:[\.,]\d{3})*(?:[\.,]\d{2})?)\s?(CLP|MXN|USD|EUR|€|pesos|euros|dólares)?'

def contiene_palabra_clave(texto: str) -> bool:
    texto_lower = texto.lower()
    return any(palabra in texto_lower for palabra in PALABRAS_CLAVE)

def detectar_gastos_con_lugares(texto: str) -> List[Dict]:
    resultados = []
    for match in re.finditer(PATRON_MONEDA, texto, flags=re.IGNORECASE):
        monto = match.group(1).replace('$', '').replace(',', '').strip()
        moneda_raw = match.group(2) or 'Desconocido'
        moneda = normalizar_moneda(moneda_raw)

        start, end = match.span()
        contexto = texto[max(0, start - 50):min(len(texto), end + 50)]

        posibles_nombres = re.findall(r'\b[A-Z][a-zA-Z0-9]{2,}\b', contexto)
        lugar = posibles_nombres[0] if posibles_nombres else "Desconocido"

        resultados.append({
            "gasto": monto,
            "moneda": moneda,
            "tipo_gasto": lugar,            
        })

    return resultados

def normalizar_moneda(moneda: str) -> str:
    moneda = moneda.lower()
    if "clp" in moneda or "pesos" in moneda:
        return "CLP"
    if "usd" in moneda or "dólares" in moneda:
        return "USD"
    if "eur" in moneda or "euros" in moneda or "€" in moneda:
        return "EUR"
    return "Desconocido"

def analyze_text_with_context(emails: List[str]) -> Dict:
    gastos = []
    for email in emails:
        if contiene_palabra_clave(email):
            gastos += detectar_gastos_con_lugares(email)

    return gastos