"""Consume el modelo de iris publicado en AWS Lambda.

Uso:
    pip install requests
    python consumir_modelo.py
"""
import requests

# Pegá acá la Function URL que te pasó la docente (termina en .lambda-url.<region>.on.aws/)
URL = "https://PEGAR-AQUI.lambda-url.us-east-2.on.aws/"

# Largo y ancho del sépalo, largo y ancho del pétalo (en cm)
flor = {"features": [5.1, 3.5, 1.4, 0.2]}

r = requests.post(URL, json=flor, timeout=30)

print("Código HTTP:", r.status_code)
print("Respuesta:", r.json())
