from pydantic import BaseModel, Field


class FinancialProfileInput(BaseModel):
    total_income: float = Field(..., example=4500000)
    total_expense: float = Field(..., example=3200000)
    net_cashflow: float = Field(..., example=1300000)
    tx_count: int = Field(..., example=35)
    avg_expense: float = Field(..., example=91428)

    food_ratio: float = Field(..., example=0.42)
    transport_ratio: float = Field(..., example=0.12)
    entertainment_ratio: float = Field(..., example=0.08)
    shopping_ratio: float = Field(..., example=0.15)
    health_ratio: float = Field(..., example=0.05)
    other_ratio: float = Field(..., example=0.18)

    saving_rate: float = Field(..., example=0.28)
    expense_trend: float = Field(..., example=300000)
    rolling_3m_avg: float = Field(..., example=1200000)