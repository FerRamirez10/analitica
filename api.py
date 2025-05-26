from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

# Cargar el archivo que contiene el modelo, forecast y estadísticas
modelo_completo = joblib.load("modelo_prophet.pkl")
model = modelo_completo['modelo']
forecast_guardado = modelo_completo['forecast']
estadisticas = modelo_completo['estadisticas']

app = FastAPI()

# Formato para predicción
class PredictionRequest(BaseModel):
    fechas: list[str]  # Lista de fechas en formato 'YYYY-MM-DD'

@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        fechas_df = pd.DataFrame({'ds': pd.to_datetime(request.fechas)})
        forecast = model.predict(fechas_df)
        result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict(orient='records')
        return {"predicciones": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Nueva ruta opcional: estadísticas descriptivas
@app.get("/estadisticas")
def get_stats():
    try:
        return estadisticas.reset_index().to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")