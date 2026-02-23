# ============================================================
#   app.py — Streamlit Dashboard
#   Drought Warning & Smart Tanker Management System
# ============================================================

import streamlit as st
import pandas as pd
from model import predict_tanker_need, get_drought_risk

st.set_page_config(page_title="Drought Warning System", page_icon="💧", layout="centered")

st.title("💧 Drought Warning & Tanker Management System")
st.markdown("Move the sliders below and click **Predict** to see results.")
st.markdown("---")

# Sidebar
st.sidebar.header("🏘️ Village Details")
village_name = st.sidebar.text_input("Village Name", value="Rampur")
population   = st.sidebar.number_input("Population", min_value=100, max_value=50000, value=4200, step=100)
st.sidebar.markdown("---")
st.sidebar.markdown("**How to use:**")
st.sidebar.markdown("1. Enter village name & population")
st.sidebar.markdown("2. Adjust the sliders")
st.sidebar.markdown("3. Click the Predict button")
st.sidebar.markdown("4. See results appear ✅")

# Sliders
st.subheader("📊 Enter Environmental Data")
col1, col2 = st.columns(2)
with col1:
    rainfall = st.slider("🌧️ Rainfall (mm)", min_value=0, max_value=600, value=150, step=5)
with col2:
    groundwater = st.slider("🕳️ Groundwater Depth (meters)", min_value=0, max_value=100, value=20, step=1)

st.markdown("---")

# Predict Button
predict_clicked = st.button("🔍 Predict Tanker Requirement", use_container_width=True)

if predict_clicked:

    tankers      = predict_tanker_need(rainfall, groundwater, population)
    stress_index = (600 - rainfall) + (20 - groundwater)
    risk         = get_drought_risk(rainfall, groundwater)

    if risk == "High":
        risk_icon = "🔴"
    elif risk == "Medium":
        risk_icon = "🟡"
    else:
        risk_icon = "🟢"

    st.markdown("---")
    st.subheader("📈 Prediction Results")

    r1, r2, r3 = st.columns(3)
    with r1:
        st.metric(label="🚛 Tankers Needed", value=f"{tankers} tankers")
    with r2:
        st.metric(label="💦 Water Stress Index", value=stress_index)
    with r3:
        st.metric(label="🚨 Risk Level", value=f"{risk_icon} {risk}")

    st.markdown("---")
    st.subheader("📋 Full Summary")

    if risk == "High":
        st.error(f"🔴 HIGH RISK — Immediate tanker deployment required for {village_name}!")
    elif risk == "Medium":
        st.warning(f"🟡 MEDIUM RISK — Monitor closely. Prepare tankers on standby for {village_name}.")
    else:
        st.success(f"🟢 LOW RISK — Situation stable in {village_name}. Routine monitoring sufficient.")

    summary_data = {
        "Detail": ["Village", "Population", "Rainfall (mm)", "Groundwater Depth (m)", "Water Stress Index", "Tankers Needed", "Risk Level"],
        "Value":  [village_name, f"{int(population):,}", rainfall, groundwater, stress_index, tankers, f"{risk_icon} {risk}"]
    }
    st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("📉 Stress Level Gauge")
    normalised = min(1.0, max(0.0, stress_index / 620))
    st.progress(normalised, text=f"Water Stress Index: {stress_index}")

else:
    st.info("👆 Adjust the sliders above and click Predict Tanker Requirement to see results.")

# Map Section
st.markdown("---")
st.subheader("🗺️ Tanker Route Map")

try:
    import folium
    from streamlit_folium import st_folium

    NAGPUR = {"name": "Nagpur (HQ)", "lat": 21.1458, "lon": 79.0882}
    VILLAGES = [
        {"name": "Ramtek",   "lat": 21.3942, "lon": 79.3259, "rainfall": 95,  "groundwater": 52, "population": 18000},
        {"name": "Hingna",   "lat": 21.0747, "lon": 78.8367, "rainfall": 140, "groundwater": 38, "population": 12000},
        {"name": "Parseoni", "lat": 21.3200, "lon": 79.0100, "rainfall": 60,  "groundwater": 67, "population": 8500},
    ]

    for v in VILLAGES:
        v["tankers"] = predict_tanker_need(v["rainfall"], v["groundwater"], v["population"])
        v["risk"]    = get_drought_risk(v["rainfall"], v["groundwater"])
        v["color"]   = "red" if v["risk"] == "High" else ("orange" if v["risk"] == "Medium" else "green")

    m = folium.Map(location=[NAGPUR["lat"], NAGPUR["lon"]], zoom_start=9, tiles="CartoDB dark_matter")

    folium.Marker(
        location=[NAGPUR["lat"], NAGPUR["lon"]],
        tooltip="Nagpur — Tanker HQ",
        popup=folium.Popup("<b>Nagpur</b><br>Tanker Dispatch HQ", max_width=200),
        icon=folium.Icon(color="blue", icon="home", prefix="fa")
    ).add_to(m)

    for v in VILLAGES:
        folium.Marker(
            location=[v["lat"], v["lon"]],
            tooltip=f"{v['name']} · {v['risk']} risk · {v['tankers']} tankers",
            popup=folium.Popup(f"<b>{v['name']}</b><br>Rainfall: {v['rainfall']}mm<br>Groundwater: {v['groundwater']}m<br>Tankers: {v['tankers']}<br>Risk: {v['risk']}", max_width=200),
            icon=folium.Icon(color=v["color"], icon="tint", prefix="fa")
        ).add_to(m)
        folium.PolyLine(
            locations=[[NAGPUR["lat"], NAGPUR["lon"]], [v["lat"], v["lon"]]],
            color=v["color"], weight=2.5, opacity=0.7, dash_array="6 4"
        ).add_to(m)

    st_folium(m, width="100%", height=420, returned_objects=[])

except ImportError:
    st.warning("Map not available. Run this in your terminal: pip install folium streamlit-folium")

st.markdown("---")
st.caption("🌍 Integrated Drought Warning & Smart Tanker Management System · Streamlit + scikit-learn")