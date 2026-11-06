import base64
import json

import joblib

# Se carga UNA sola vez, cuando arranca el contenedor (no en cada pedido)
model = joblib.load("model_sklearn.joblib")

CLASES = ["setosa", "versicolor", "virginica"]


def respuesta(status, datos):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(datos),
    }


def lambda_handler(event, context):
    # Con Function URL el JSON que manda el cliente llega como texto en event["body"]
    body = event.get("body") or "{}"
    if event.get("isBase64Encoded"):
        body = base64.b64decode(body).decode("utf-8")

    try:
        datos = json.loads(body)
        features = [float(x) for x in datos["features"]]
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        return respuesta(400, {
            "error": 'Mandá un JSON así: {"features": [5.1, 3.5, 1.4, 0.2]}'
        })

    if len(features) != 4:
        return respuesta(400, {
            "error": "Hacen falta 4 valores: largo y ancho del sépalo, largo y ancho del pétalo (en cm)"
        })

    prediccion = int(model.predict([features])[0])
    probabilidades = model.predict_proba([features])[0]

    return respuesta(200, {
        "prediction": prediccion,
        "clase": CLASES[prediccion],
        "probabilities": [round(float(p), 4) for p in probabilidades],
    })
