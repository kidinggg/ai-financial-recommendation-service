import joblib
import numpy as np
import pandas as pd
import tensorflow as tf

from recommendation import generate_recommendation


# =========================
# Model Paths
# =========================

FINANCIAL_RISK_MODEL_PATH = "models/financial_risk/financial_risk_model.keras"
FINANCIAL_RISK_SCALER_PATH = "models/financial_risk/financial_risk_scaler.pkl"
FINANCIAL_RISK_LABEL_ENCODER_PATH = "models/financial_risk/financial_risk_label_encoder.pkl"
FINANCIAL_RISK_FEATURE_COLUMNS_PATH = "models/financial_risk/financial_risk_feature_columns.pkl"

BEHAVIOR_SEGMENT_MODEL_PATH = "models/behavior_segment/behavior_segment_model.keras"
BEHAVIOR_SEGMENT_SCALER_PATH = "models/behavior_segment/behavior_segment_scaler.pkl"
BEHAVIOR_SEGMENT_LABEL_ENCODER_PATH = "models/behavior_segment/behavior_segment_label_encoder.pkl"
BEHAVIOR_SEGMENT_FEATURE_COLUMNS_PATH = "models/behavior_segment/behavior_segment_feature_columns.pkl"


# =========================
# Load Models and Preprocessors
# =========================

financial_risk_model = tf.keras.models.load_model(FINANCIAL_RISK_MODEL_PATH)
financial_risk_scaler = joblib.load(FINANCIAL_RISK_SCALER_PATH)
financial_risk_label_encoder = joblib.load(FINANCIAL_RISK_LABEL_ENCODER_PATH)
financial_risk_feature_columns = joblib.load(FINANCIAL_RISK_FEATURE_COLUMNS_PATH)

behavior_segment_model = tf.keras.models.load_model(BEHAVIOR_SEGMENT_MODEL_PATH)
behavior_segment_scaler = joblib.load(BEHAVIOR_SEGMENT_SCALER_PATH)
behavior_segment_label_encoder = joblib.load(BEHAVIOR_SEGMENT_LABEL_ENCODER_PATH)
behavior_segment_feature_columns = joblib.load(BEHAVIOR_SEGMENT_FEATURE_COLUMNS_PATH)


# =========================
# Feature Engineering
# =========================

def add_financial_risk_features(input_data):
    data = input_data.copy()

    total_income = data.get("total_income", 0)
    total_expense = data.get("total_expense", 0)

    if total_income == 0:
        data["expense_to_income_ratio"] = 0
    else:
        data["expense_to_income_ratio"] = total_expense / total_income

    data["discretionary_ratio"] = (
        data.get("shopping_ratio", 0)
        + data.get("entertainment_ratio", 0)
    )

    data["essential_ratio"] = (
        data.get("food_ratio", 0)
        + data.get("transport_ratio", 0)
        + data.get("health_ratio", 0)
    )

    if total_expense == 0:
        data["expense_trend_ratio"] = 0
    else:
        data["expense_trend_ratio"] = data.get("expense_trend", 0) / total_expense

    return data


# =========================
# Prediction Helper
# =========================

def predict_with_model(input_data, model, scaler, label_encoder, feature_columns):
    input_df = pd.DataFrame([input_data])

    missing_columns = [
        column for column in feature_columns
        if column not in input_df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing input columns: {missing_columns}")

    input_df = input_df[feature_columns]
    input_scaled = scaler.transform(input_df)

    prediction_prob = model.predict(input_scaled, verbose=0)
    prediction_index = int(np.argmax(prediction_prob, axis=1)[0])

    label = label_encoder.inverse_transform([prediction_index])[0]
    confidence = float(np.max(prediction_prob))

    return {
        "label": label,
        "confidence": round(confidence, 4)
    }


# =========================
# Main Inference Function
# =========================

def predict_user_financial_profile(input_data):
    financial_input = add_financial_risk_features(input_data)

    financial_risk_result = predict_with_model(
        input_data=financial_input,
        model=financial_risk_model,
        scaler=financial_risk_scaler,
        label_encoder=financial_risk_label_encoder,
        feature_columns=financial_risk_feature_columns
    )

    behavior_segment_result = predict_with_model(
        input_data=input_data,
        model=behavior_segment_model,
        scaler=behavior_segment_scaler,
        label_encoder=behavior_segment_label_encoder,
        feature_columns=behavior_segment_feature_columns
    )

    recommendation = generate_recommendation(
        input_data=input_data,
        financial_risk_label=financial_risk_result["label"],
        behavior_segment_label=behavior_segment_result["label"]
    )

    return {
        "financial_risk": financial_risk_result,
        "behavior_segment": behavior_segment_result,
        "recommendation": recommendation
    }


# =========================
# Local Test
# =========================

if __name__ == "__main__":
    sample_input = {
        "total_income": 5200000,
        "total_expense": 4100000,
        "net_cashflow": 1100000,
        "tx_count": 42,
        "avg_expense": 97619,
        "food_ratio": 0.24,
        "transport_ratio": 0.12,
        "entertainment_ratio": 0.08,
        "shopping_ratio": 0.33,
        "health_ratio": 0.05,
        "other_ratio": 0.18,
        "saving_rate": 0.21,
        "expense_trend": 250000,
        "rolling_3m_avg": 950000
    }

    result = predict_user_financial_profile(sample_input)
    print(result)