
import json
import torch
from torch import nn

model = nn.Sequential(
    nn.Linear(4, 16),
    nn.ReLU(),
    nn.Linear(16, 3)
)

model.load_state_dict(
    torch.load("model_pytorch.pth", map_location="cpu", weights_only=True)
)
model.eval()

def lambda_handler(event, context):
    body = json.loads(event["body"])

    x = torch.tensor([body["features"]], dtype=torch.float32)

    with torch.no_grad():
        output = model(x)
        probabilities = torch.softmax(output, dim=1)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "prediction": int(output.argmax(dim=1).item()),
            "probabilities": probabilities[0].tolist()
        })
    }