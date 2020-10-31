import os
import json
from joblib import load
import codecs


def init():
    global model

    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'model.joblib')
    model = load(model_path)


def run(data):
    try:
        data = json.loads(data)
        prediction = predict(data['number'])
        return prediction
    except Exception as e:
        error = str(e)
        return error


def predict(number):
    result = model.predict(number)
    return {"pred": str(result)}  