
import json
import joblib

model = joblib.load("model_sklearn.joblib")

def lambda_handler(event, context):

    body = json.loads(event["body"])

    features = body["features"]

    prediction = model.predict([features])[0]
    probabilities = model.predict_proba([features])[0]

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "prediction": int(prediction),
            "probabilities": probabilities.tolist()
        })
    }
