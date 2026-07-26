# Nigerian Education Dropout Prediction

## Mission
This project predicts the number of student dropouts in Nigeria for a given State, grade level, and time period, using a Random Forest regression model. The goal is to help education authorities identify in advance where to focus resources — scholarships, awareness campaigns, family support — before dropout rates rise further.

## Dataset
Source: `nigerian_education_dropout_rates.csv` — a synthetic dataset of 150,000 individual student dropout records across 37 Nigerian States, 6 grade levels (JSS 1 to SSS 3), and 8 dropout reasons, spanning 2022–2025. The raw data is aggregated by State, grade, year, and month to create `dropout_count`, the continuous regression target.


## Project Structure

```text
linear_regression_model/
├── summative/
│   ├── linear_regression/
│   │   ├── multivariate.ipynb
│   │   ├── best_model.pkl
│   │   └── scaler.pkl
│   │
│   ├── API/
│   │   ├── prediction.py
│   │   └── requirements.txt
│   │
│   └── FlutterApp/
│       ├── lib/
│       └── main.dart
│
├── pyproject.toml
├── uv.lock
└── README.md
```

### Steps
1. Clone the repository:
git clone https://github.com/yohan2330/linear_regression_model
cd linear_regression_model/summative/API
2. Install dependencies:
uv sync
3. Make sure `best_model.pkl` and `scaler.pkl` are present at `summative/linear_regression/`
4. Run the server:

## Running the Mobile App

**Requirements:** Flutter SDK installed (`flutter doctor` should pass), an Android emulator or physical device connected via USB with USB debugging enabled.

1. Navigate to the app folder:
cd summative/FlutterApp
2. Install dependencies:
flutter pub get
3. Connect a device or start an emulator, then check it's detected:
flutter devices
4. Run the app:
flutter run

Select your Android device/emulator from the list when prompted.

The app has a single page with six input fields (State, grade, year, month, female ratio, dominant reason), a **Predict** button, and a result display area. It calls the live API above — no local backend needed.

## API Endpoint

**Swagger UI Documentation:** https://linear-regression-model-6sm2.onrender.com/docs
- `POST /predict` — takes State, grade, year, month, female ratio, and dominant reason, returns the predicted dropout count.
- `POST /retrain` — accepts a new raw CSV in the original format and retrains the model on updated data.

CORS is configured with explicit allowed origins, methods, and headers rather than a generic wildcard.

### Input Parameters
- `state` (string, one of 37 Nigerian States, e.g. "Lagos")
- `grade` (string, one of "JSS 1", "JSS 2", "JSS 3", "SSS 1", "SSS 2", "SSS 3")
- `year` (int, 2022-2027)
- `month` (int, 1-12)
- `female_ratio` (float, 0.0-1.0)
- `dominant_reason` (string, one of: child_labor, early_marriage, household_chores, migration, other, poor_performance, poverty, pregnancy)


## Model Performance

Four regression approaches were implemented and compared: Linear Regression (OLS), SGD Regressor, Random Forest, and Decision Tree. Random Forest was selected as the best-performing model (MSE 15.71, R² 0.08). Note: the R² is low across all models because the available features (State, grade, month, female ratio, dominant reason) have very weak individual correlation with dropout counts (all under 0.05) — this is discussed further in the video demo.

## Technologies Used
- **Machine Learning:** Python, scikit-learn, pandas, numpy
- **API:** FastAPI, Pydantic, uvicorn
- **Mobile App:** Flutter, Dart
- **Deployment:** Render (API)
- **Visualization:** matplotlib, seaborn

## Video Demo

Youtube Link : https://youtu.be/75iH6hvG2Ng?si=OPTVlm9L177uZSlM

## Setup (development)

This project uses `uv` for package and environment management.
