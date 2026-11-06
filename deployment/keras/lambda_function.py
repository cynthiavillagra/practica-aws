import json
import tensorflow as tf

model = tf.keras.models.load_model("model_keras.keras")

def lambda_handler(event, context):
    body = json.loads(event["body"])

    x = [body["features"]]

    probabilities = model.predict(x, verbose=0)[0]

    return {
        "statusCode": 200,
        "body": json.dumps({
            "prediction": int(probabilities.argmax()),
            "probabilities": probabilities.tolist()
        })
    }