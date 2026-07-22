import shutil
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from enum import Enum
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

# ---------------------------------------------------------------------------
# Load trained artifacts
# ---------------------------------------------------------------------------
model = joblib.load("../linear_regression/best_model.pkl")
scaler = joblib.load("../linear_regression/scaler.pkl")

MODEL_COLUMNS = [
    'grade_level', 'year', 'month', 'female_ratio',
    'state_Adamawa', 'state_Akwa Ibom', 'state_Anambra', 'state_Bauchi', 'state_Bayelsa',
    'state_Benue', 'state_Borno', 'state_Cross River', 'state_Delta', 'state_Ebonyi',
    'state_Edo', 'state_Ekiti', 'state_Enugu', 'state_FCT', 'state_Gombe', 'state_Imo',
    'state_Jigawa', 'state_Kaduna', 'state_Kano', 'state_Katsina', 'state_Kebbi', 'state_Kogi',
    'state_Kwara', 'state_Lagos', 'state_Nasarawa', 'state_Niger', 'state_Ogun', 'state_Ondo',
    'state_Osun', 'state_Oyo', 'state_Plateau', 'state_Rivers', 'state_Sokoto', 'state_Taraba',
    'state_Yobe', 'state_Zamfara',
    'dominant_reason_early_marriage', 'dominant_reason_household_chores',
    'dominant_reason_migration', 'dominant_reason_other', 'dominant_reason_poor_performance',
    'dominant_reason_poverty', 'dominant_reason_pregnancy',
]

GRADE_LEVELS = {'JSS 1': 1, 'JSS 2': 2, 'JSS 3': 3, 'SSS 1': 4, 'SSS 2': 5, 'SSS 3': 6}


def build_feature_vector(state, grade, year, month, female_ratio, dominant_reason):
    row = dict.fromkeys(MODEL_COLUMNS, 0)
    row['grade_level'] = GRADE_LEVELS[grade]
    row['year'] = year
    row['month'] = month
    row['female_ratio'] = female_ratio

    state_col = f"state_{state}"
    if state_col in row:
        row[state_col] = 1

    reason_col = f"dominant_reason_{dominant_reason}"
    if reason_col in row:
        row[reason_col] = 1

    return pd.DataFrame([row], columns=MODEL_COLUMNS)


def predict_dropout_count(state, grade, year, month, female_ratio, dominant_reason):
    features = build_feature_vector(state, grade, year, month, female_ratio, dominant_reason)
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)
    return float(prediction[0])


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Nigerian Education Dropout Prediction API",
    description="Predicts the number of student dropouts for a given State, grade, and time period.",
    version="1.0.0",
)

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "https://your-flutter-app-domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class StateEnum(str, Enum):
    Abia = "Abia"; Adamawa = "Adamawa"; Akwa_Ibom = "Akwa Ibom"; Anambra = "Anambra"
    Bauchi = "Bauchi"; Bayelsa = "Bayelsa"; Benue = "Benue"; Borno = "Borno"
    Cross_River = "Cross River"; Delta = "Delta"; Ebonyi = "Ebonyi"; Edo = "Edo"
    Ekiti = "Ekiti"; Enugu = "Enugu"; FCT = "FCT"; Gombe = "Gombe"; Imo = "Imo"
    Jigawa = "Jigawa"; Kaduna = "Kaduna"; Kano = "Kano"; Katsina = "Katsina"
    Kebbi = "Kebbi"; Kogi = "Kogi"; Kwara = "Kwara"; Lagos = "Lagos"
    Nasarawa = "Nasarawa"; Niger = "Niger"; Ogun = "Ogun"; Ondo = "Ondo"
    Osun = "Osun"; Oyo = "Oyo"; Plateau = "Plateau"; Rivers = "Rivers"
    Sokoto = "Sokoto"; Taraba = "Taraba"; Yobe = "Yobe"; Zamfara = "Zamfara"


class GradeEnum(str, Enum):
    JSS1 = "JSS 1"; JSS2 = "JSS 2"; JSS3 = "JSS 3"
    SSS1 = "SSS 1"; SSS2 = "SSS 2"; SSS3 = "SSS 3"


class ReasonEnum(str, Enum):
    child_labor = "child_labor"
    early_marriage = "early_marriage"
    household_chores = "household_chores"
    migration = "migration"
    other = "other"
    poor_performance = "poor_performance"
    poverty = "poverty"
    pregnancy = "pregnancy"


class DropoutPredictionRequest(BaseModel):
    state: StateEnum = Field(..., description="Nigerian state")
    grade: GradeEnum = Field(..., description="School grade level")
    year: int = Field(..., ge=2022, le=2027, description="Calendar year")
    month: int = Field(..., ge=1, le=12, description="Calendar month (1-12)")
    female_ratio: float = Field(..., ge=0.0, le=1.0, description="Proportion of female students (0-1)")
    dominant_reason: ReasonEnum = Field(..., description="Most common dropout reason in the group")

    class Config:
        json_schema_extra = {
            "example": {
                "state": "Lagos", "grade": "JSS 1", "year": 2025,
                "month": 6, "female_ratio": 0.5, "dominant_reason": "poverty",
            }
        }


class DropoutPredictionResponse(BaseModel):
    predicted_dropout_count: float


@app.get("/")
def root():
    return {"message": "Nigerian Education Dropout Prediction API. See /docs for Swagger UI."}


@app.post("/predict", response_model=DropoutPredictionResponse)
def predict(request: DropoutPredictionRequest):
    try:
        result = predict_dropout_count(
            state=request.state.value,
            grade=request.grade.value,
            year=request.year,
            month=request.month,
            female_ratio=request.female_ratio,
            dominant_reason=request.dominant_reason.value,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return DropoutPredictionResponse(predicted_dropout_count=round(result, 2))


@app.post("/retrain")
def retrain(file: UploadFile = File(...)):
    """
    Upload a new raw CSV (same columns as the original training data:
    student_id, state, gender, grade, dropout_date, reason) to retrain
    the model on updated data.
    """
    try:
        temp_path = "temp_retrain_data.csv"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        raw = pd.read_csv(temp_path)
        raw['dropout_date'] = pd.to_datetime(raw['dropout_date'])
        raw['year'] = raw['dropout_date'].dt.year
        raw['month'] = raw['dropout_date'].dt.month

        agg = raw.groupby(['state', 'grade', 'year', 'month']).agg(
            dropout_count=('student_id', 'count'),
            female_ratio=('gender', lambda x: (x == 'female').mean())
        ).reset_index()
        dominant_reason = (raw.groupby(['state', 'grade', 'year', 'month'])['reason']
                            .agg(lambda x: x.value_counts().idxmax())
                            .reset_index(name='dominant_reason'))
        agg = agg.merge(dominant_reason, on=['state', 'grade', 'year', 'month'])
        agg['grade_level'] = agg['grade'].map(GRADE_LEVELS)

        X_new = pd.get_dummies(
            agg[['state', 'grade_level', 'year', 'month', 'female_ratio', 'dominant_reason']],
            columns=['state', 'dominant_reason'], drop_first=True
        )
        X_new = X_new.reindex(columns=MODEL_COLUMNS, fill_value=0)
        y_new = agg['dropout_count']

        X_train, X_test, y_train, y_test = train_test_split(X_new, y_new, test_size=0.2, random_state=42)

        new_scaler = StandardScaler()
        X_train_scaled = new_scaler.fit_transform(X_train)
        X_test_scaled = new_scaler.transform(X_test)

        new_model = RandomForestRegressor(n_estimators=200, max_depth=6, random_state=42)
        new_model.fit(X_train_scaled, y_train)
        test_r2 = new_model.score(X_test_scaled, y_test)

        joblib.dump(new_model, "../linear_regression/best_model.pkl")
        joblib.dump(new_scaler, "../linear_regression/scaler.pkl")

        global model, scaler
        model = new_model
        scaler = new_scaler

        return {"message": "Model retrained successfully.", "test_r2": round(test_r2, 4), "rows_used": len(agg)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Retraining failed: {str(e)}")