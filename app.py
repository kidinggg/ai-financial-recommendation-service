from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from inference import predict_user_financial_profile
from schemas import FinancialProfileInput


app = FastAPI(
    title="AI Financial Recommendation Service",
    description="API untuk prediksi financial risk, behavior segment, dan rekomendasi keuangan pengguna.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Untuk development/demo. Nanti bisa diganti domain frontend.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "AI Financial Recommendation Service is running",
        "available_endpoints": [
            "/predict",
            "/docs",
            "/ui"
        ]
    }


@app.get("/ui")
def ui():
    return FileResponse("ui.html")


@app.post("/predict")
def predict_financial_profile(input_data: FinancialProfileInput):
    input_dict = input_data.model_dump()

    prediction_result = predict_user_financial_profile(input_dict)

    return {
        "input": input_dict,
        "prediction": prediction_result
    }