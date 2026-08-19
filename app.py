
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import io

app = Flask(__name__)
model = joblib.load('superkart_model.joblib')

@app.route('/v1/predict', methods=['POST'])
def predict():
    data = request.get_json()
    df = pd.DataFrame([data])
    prediction = model.predict(df)
    return jsonify({'prediction': prediction[0]})

@app.route('/v1/predictbatch', methods=['POST'])
def predict_batch():
    file = request.files['file']
    df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    predictions = model.predict(df)
    return jsonify(pd.Series(predictions).to_dict())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
