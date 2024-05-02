import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
 

def predict():
    '''
    For rendering results on HTML GUI
    '''
    
    try:
        temperature=float(request.form.get('temperature'))
        
        if temperature >40:
            raise ValueError("Temperature should not exceed 40 degrees.")
        int_features = [float(x) for x in request.form.values()]
        final_features = [np.array(int_features)]
        prediction = model.predict(final_features)
    
        output = prediction
        return render_template('index.html', prediction_text='Suggested crop for given soil health condition is: "{}".'.format(output[0]))
    
    except ValueError as e:
        return render_template('index.html', prediction_text=f'Error: {str(e)}')
        
    

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    try:
        data = request.get_json(force=True)
        temperature=float(request.form.get('temperature'))
        
        if temperature >60:
            raise ValueError("Temperature should not exceed 60 degrees.")
            
        prediction = model.predict([np.array(list(data.values()))])

        output = prediction[0]
        return jsonify(output)

    except ValueError as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)