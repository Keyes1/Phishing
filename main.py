from flask import Flask, request, jsonify
import joblib
from pandas import DataFrame

app = Flask(__name__)
loaded_model = joblib.load('skin_model.pkl') 

@app.route('/predict', methods=['POST'])
def receive_data():
    data = request.get_json()  
    df = DataFrame(data)  
    prediction = loaded_model.predict(df)  
    return jsonify({'prediction': prediction.tolist()})  

if __name__ == '__main__':
    app.run(debug=True)