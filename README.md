# AI Financial Recommendation Service

AI Financial Recommendation Service adalah service berbasis FastAPI yang digunakan untuk memprediksi kondisi keuangan pengguna dan memberikan rekomendasi keuangan berdasarkan data agregasi transaksi bulanan.

Service ini menggunakan dua model TensorFlow:

1. **Financial Risk Model**  
   Mengklasifikasikan kondisi keuangan pengguna menjadi:
   - Healthy
   - Watchlist
   - At Risk

2. **Behavior Segment Model**  
   Mengklasifikasikan pola perilaku keuangan pengguna menjadi:
   - Good Saver
   - High Food Spender
   - Stable Spender
   - Increasing Spender
   - Negative Cashflow
   - Shopping Heavy
   - Entertainment Heavy

Hasil prediksi dari kedua model digunakan untuk menghasilkan rekomendasi keuangan yang lebih personal.

---

## Project Structure

```text
ai-service/
├── app.py
├── inference.py
├── recommendation.py
├── schemas.py
├── ui.html
├── requirements.txt
└── models/
    ├── financial_risk/
    │   ├── financial_risk_model.keras
    │   ├── financial_risk_scaler.pkl
    │   ├── financial_risk_label_encoder.pkl
    │   └── financial_risk_feature_columns.pkl
    │
    └── behavior_segment/
        ├── behavior_segment_model.keras
        ├── behavior_segment_scaler.pkl
        ├── behavior_segment_label_encoder.pkl
        └── behavior_segment_feature_columns.pkl
```

---

## Installation

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## Run API Service

Jalankan service dengan perintah:

```bash
python -m uvicorn app:app --reload
```

Jika berhasil, service akan berjalan di:

```text
http://127.0.0.1:8000
```

---

## Available Endpoints

### Root Endpoint

```http
GET /
```

Digunakan untuk mengecek apakah service berjalan.

Response:

```json
{
  "message": "AI Financial Recommendation Service is running",
  "available_endpoints": [
    "/predict",
    "/docs",
    "/ui"
  ]
}
```

---

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

Digunakan untuk testing endpoint API melalui UI bawaan FastAPI.

---

### Simulation UI

```text
http://127.0.0.1:8000/ui
```

Digunakan untuk simulasi prediksi melalui form sederhana. User dapat memasukkan total income dan pengeluaran per kategori, lalu sistem akan menghitung fitur yang dibutuhkan model secara otomatis.

---

### Prediction Endpoint

```http
POST /predict
```

Endpoint ini menerima fitur keuangan bulanan pengguna dan mengembalikan hasil prediksi financial risk, behavior segment, dan rekomendasi.

Request body:

```json
{
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
```

Response example:

```json
{
  "input": {
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
  },
  "prediction": {
    "financial_risk": {
      "label": "Watchlist",
      "confidence": 0.9051
    },
    "behavior_segment": {
      "label": "Shopping Heavy",
      "confidence": 0.9998
    },
    "recommendation": {
      "title": "Belanja perlu dikontrol",
      "message": "Porsi pengeluaran belanja kamu cukup tinggi. Coba bedakan kebutuhan dan keinginan sebelum melakukan pembelian."
    }
  }
}
```

---

## Input Feature Explanation

| Feature | Description |
|---|---|
| total_income | Total pemasukan user dalam satu periode/bulan |
| total_expense | Total pengeluaran user dalam satu periode/bulan |
| net_cashflow | Selisih antara pemasukan dan pengeluaran |
| tx_count | Jumlah transaksi dalam periode tersebut |
| avg_expense | Rata-rata nominal pengeluaran |
| food_ratio | Rasio pengeluaran kategori food terhadap total expense |
| transport_ratio | Rasio pengeluaran kategori transport terhadap total expense |
| entertainment_ratio | Rasio pengeluaran kategori entertainment terhadap total expense |
| shopping_ratio | Rasio pengeluaran kategori shopping terhadap total expense |
| health_ratio | Rasio pengeluaran kategori health terhadap total expense |
| other_ratio | Rasio pengeluaran kategori other terhadap total expense |
| saving_rate | Rasio cashflow terhadap total income |
| expense_trend | Perubahan total pengeluaran dibanding periode sebelumnya |
| rolling_3m_avg | Rata-rata cashflow 3 bulan terakhir |

---

## Notes for Front-End / Back-End Team

User tidak perlu menginput fitur seperti `food_ratio`, `saving_rate`, atau `avg_expense` secara manual.

Di aplikasi sebenarnya, user cukup mencatat transaksi seperti:

- income
- expense
- amount
- category
- transaction date
- description

Kemudian backend atau proses agregasi data menghitung fitur bulanan seperti:

- total_income
- total_expense
- net_cashflow
- category ratio
- saving_rate
- expense_trend
- rolling_3m_avg

Setelah fitur bulanan terbentuk, data tersebut dikirim ke endpoint `/predict` untuk mendapatkan hasil prediksi dan rekomendasi.

---

## Recommended Integration Flow

Alur integrasi yang disarankan:

```text
User mencatat transaksi
↓
Backend menyimpan transaksi
↓
Backend menghitung fitur keuangan berdasarkan periode yang dipilih
↓
Backend mengirim data ke AI service /predict
↓
AI service mengembalikan financial risk, behavior segment, dan rekomendasi
↓
Frontend menampilkan hasil ke user
```

Untuk MVP, sistem dapat menggunakan pendekatan berikut:

1. **Default monthly analysis**  
   Secara default, sistem menjalankan analisis keuangan secara bulanan.

2. **Manual analysis button**  
   Frontend dapat menyediakan tombol seperti "Analisis Keuangan Saya" atau "Dapatkan Rekomendasi" agar user bisa meminta analisis kapan saja.

3. **Optional weekly analysis**  
   Jika diperlukan, user dapat diberikan opsi untuk memilih frekuensi analisis, misalnya mingguan atau bulanan.

Jika hasil prediksi menunjukkan `At Risk` atau `Negative Cashflow`, frontend dapat menampilkan hasilnya sebagai alert atau warning agar lebih terlihat oleh user.

---

## Model Information

Model dibuat menggunakan TensorFlow Functional API.

Model yang digunakan:

- `financial_risk_model.keras`
- `behavior_segment_model.keras`

Model disimpan dalam format `.keras` dan dilengkapi dengan:

- scaler
- label encoder
- feature columns

Hal ini digunakan agar proses inference konsisten dengan proses training.

---

## Development Status

Current status:

- Model inference berhasil berjalan
- FastAPI endpoint berhasil berjalan
- Swagger UI tersedia
- Simulation UI tersedia
- Recommendation logic tersedia
- Service siap untuk deployment