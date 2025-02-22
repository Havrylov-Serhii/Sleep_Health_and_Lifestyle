from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd
import pickle

# Load the model
with open('./model/model.pkl', 'rb') as f:
    model = pickle.load(f)

app = FastAPI()

class InputData(BaseModel):
    age: int
    heart_rate: float
    avg_pressure: float
    bmi_category: str
    gender: str
    
# Main page
@app.get('/')
def home():
    return {'message': 'Sleep Disorder Prediction API'}

# Endpoint for predictions
@app.post('/predict/')
def predict(data: InputData):
    # Mapping Gender and BMI
    gender_mapping = {'Male':1, "Female":0}
    bmi_mapping ={'Normal':0, "Overweight":1, "Obese":2, "Underweight":3}
    
    gender_encoded = gender_mapping.get(data.gender,-1)
    bmi_encoded = bmi_mapping.get(data.bmi_category,-1)
    
    if gender_encoded == -1:
        return {'error': 'Invalid input for gender'}
    elif bmi_encoded == -1:
        return {'error': 'Invalid input for BMI'}
    
    # Make a DataFrame for a model to predict (Need to be in the same order that we taught)
    input_df = pd.DataFrame([{
        "Gender": gender_encoded,
        "Age": data.age,
        "BMI Category": bmi_encoded,
        "Heart Rate": data.heart_rate,
        "AVG_Pressure": data.avg_pressure
    }])
    
    # Making a prediction
    prediction = model.predict(input_df)[0]

    # Mappin disorders
    disorder_mapping = {0 : 'None', 1: 'Sleep Apnea', 2: 'Insomnia'}
    result = disorder_mapping.get(prediction,'Unknown')
    
    return {'prediction': result}