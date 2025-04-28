from network_security.exception.exception import NetworkSecurityException
import sys
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any
from network_security.constant.prediction_pipeline import CustomData,URLAnalyzer,PredictionPipeline
import joblib

from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()


templates = Jinja2Templates(directory="templates")


prediction_pipeline = PredictionPipeline()

class URLInput(BaseModel):
    url: str

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict/", response_class=HTMLResponse)
async def predict_url(url: str = Form(...)):
    try:
        
        analyzer = URLAnalyzer()
        features_dict = analyzer.extract_features(url)

       
        custom_data = CustomData(**features_dict)

       
        input_df = custom_data.get_pandas_dataframe()

        
        prediction = prediction_pipeline.model_prediction(input_df)

        
        if prediction[0] == 1:
            return templates.TemplateResponse("index.html", {"request": {}, "result": "Phishing Website Detected!", "prediction_class": "phishing"})
        else:
            return templates.TemplateResponse("index.html", {"request": {}, "result": "Legitimate Website", "prediction_class": "safe"})

    except Exception as e:
        raise NetworkSecurityException(e,sys)