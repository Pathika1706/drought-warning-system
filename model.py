# ============================================================
#   model.py — Drought Warning & Tanker Prediction Model
#   Uses Linear Regression to predict tanker demand
# ============================================================

import pandas as pd
from sklearn.linear_model import LinearRegression

# ── Step 1: Load the CSV file ─────────────────────────────────
# IMPORTANT: data.csv must be in the same folder as this file!
df = pd.read_csv("data.csv")

# ── Step 2: Create the target column "Tanker Demand" ─────────
# Logic:
#   More population    → more tankers needed
#   Less rainfall      → more tankers needed
#   Deeper groundwater → more tankers needed
df["Tanker Demand"] = (
    df["Population"] / 500
    - (df["Rainfall (mm)"] / 100)
    + (df["Groundwater Level (meters)"] / 10)
).round().astype(int)

# Make sure demand is never less than 1
df["Tanker Demand"] = df["Tanker Demand"].clip(lower=1)

# ── Step 3: Set up inputs (X) and output (y) ─────────────────
# X = what we feed into the model (rainfall, groundwater, population)
# y = what we want to predict (tanker demand)
X = df[["Rainfall (mm)", "Groundwater Level (meters)", "Population"]]
y = df["Tanker Demand"]

# ── Step 4: Train the model ───────────────────────────────────
model = LinearRegression()
model.fit(X, y)

# ── Step 5: Prediction function (used by app.py) ─────────────
def predict_tanker_need(rainfall, groundwater, population=5000):
    """
    Takes rainfall, groundwater depth, and population.
    Returns the number of tankers needed (as a whole number).
    """
    input_data = pd.DataFrame(
        [[rainfall, groundwater, population]],
        columns=["Rainfall (mm)", "Groundwater Level (meters)", "Population"]
    )
    result = model.predict(input_data)[0]
    return max(1, round(result))   # always at least 1 tanker

# ── Step 6: Risk label function (used by app.py) ─────────────
def get_drought_risk(rainfall, groundwater):
    """
    Returns a risk level string based on rainfall and groundwater.
    """
    if rainfall < 100 and groundwater > 50:
        return "High"
    elif rainfall < 250 or groundwater > 30:
        return "Medium"
    else:
        return "Low"
