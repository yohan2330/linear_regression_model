import joblib
import numpy as np

# Load trained artifacts (must sit next to this file)
model = joblib.load("best_model.pkl")
scaler = joblib.load("scaler.pkl")

# Exact column order the model was trained on (copied from X.columns in the notebook)
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
    """Turns raw input values into the one-hot encoded vector the model expects."""
    row = dict.fromkeys(MODEL_COLUMNS, 0)
    row['grade_level'] = GRADE_LEVELS[grade]
    row['year'] = year
    row['month'] = month
    row['female_ratio'] = female_ratio

    state_col = f"state_{state}"
    if state_col in row:          # Abia is the dropped reference category -> stays all 0
        row[state_col] = 1

    reason_col = f"dominant_reason_{dominant_reason}"
    if reason_col in row:         # child_labor is the dropped reference category -> stays all 0
        row[reason_col] = 1

    return np.array([[row[c] for c in MODEL_COLUMNS]])


def predict_dropout_count(state, grade, year, month, female_ratio, dominant_reason):
    features = build_feature_vector(state, grade, year, month, female_ratio, dominant_reason)
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)
    return float(prediction[0])