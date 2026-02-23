# ============================================================
#   app.py — Streamlit Dashboard
#   District Water Command Center
#   Drought Warning & Smart Tanker Management System
# ============================================================

import streamlit as st
import pandas as pd
from model import predict_tanker_need, get_drought_risk

# ── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="District Water Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS: Dark Government Dashboard Theme ───────────────
st.markdown("""
<style>
    /* ---- Import fonts ---- */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono&family=Exo+2:wght@300;400;600&display=swap');

    /* ---- Global background ---- */
    .stApp {
        background-color: #0a0e17;
        background-image:
            radial-gradient(ellipse at 10% 20%, rgba(0, 80, 160, 0.12) 0%, transparent 50%),
            radial-gradient(ellipse at 90% 80%, rgba(0, 160, 120, 0.08) 0%, transparent 50%);
        font-family: 'Exo 2', sans-serif;
        color: #c8d8e8;
    }

    /* ---- Sidebar ---- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #080c14 0%, #0d1520 100%);
        border-right: 1px solid #1a3a5c;
    }
    [data-testid="stSidebar"] * {
        color: #a0bcd8 !important;
    }

    /* ---- Header Banner ---- */
    .gov-header {
        background: linear-gradient(135deg, #071120 0%, #0d2340 50%, #071120 100%);
        border: 1px solid #1e4a7a;
        border-left: 4px solid #00a8ff;
        border-radius: 4px;
        padding: 20px 30px;
        margin-bottom: 8px;
        position: relative;
        overflow: hidden;
    }
    .gov-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(
            90deg,
            transparent,
            transparent 60px,
            rgba(0, 168, 255, 0.03) 60px,
            rgba(0, 168, 255, 0.03) 61px
        );
    }
    .gov-header h1 {
        font-family: 'Rajdhani', sans-serif;
        font-size: 2.1rem;
        font-weight: 700;
        color: #e8f4ff;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin: 0 0 4px 0;
    }
    .gov-header .sub {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.75rem;
        color: #00a8ff;
        letter-spacing: 4px;
        text-transform: uppercase;
    }
    .gov-header .badge {
        position: absolute;
        top: 18px; right: 24px;
        background: rgba(0, 168, 255, 0.1);
        border: 1px solid #00a8ff;
        border-radius: 3px;
        padding: 4px 12px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.7rem;
        color: #00a8ff;
        letter-spacing: 2px;
    }

    /* ---- Section Headers ---- */
    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        background: linear-gradient(90deg, rgba(0, 80, 160, 0.2) 0%, transparent 100%);
        border-left: 3px solid #0070cc;
        padding: 8px 16px;
        margin: 18px 0 10px 0;
        border-radius: 0 4px 4px 0;
    }
    .section-header span {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.05rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #7ec8ff;
    }

    /* ---- Metric Cards ---- */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #0a1628 0%, #0f1e35 100%);
        border: 1px solid #1a3a5c;
        border-radius: 4px;
        padding: 16px !important;
    }
    [data-testid="stMetric"]:hover {
        border-color: #0070cc;
        box-shadow: 0 0 12px rgba(0, 112, 204, 0.2);
    }
    [data-testid="stMetricLabel"] {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.72rem !important;
        letter-spacing: 2px !important;
        color: #5a8ab0 !important;
        text-transform: uppercase;
    }
    [data-testid="stMetricValue"] {
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #e0f0ff !important;
    }

    /* ---- Risk Alert Boxes ---- */
    .risk-high {
        background: linear-gradient(135deg, #2a0808, #1a0505);
        border: 1px solid #cc2200;
        border-left: 4px solid #ff3300;
        border-radius: 4px;
        padding: 16px 20px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 1px;
        color: #ff8070;
    }
    .risk-medium {
        background: linear-gradient(135deg, #1a1200, #120e00);
        border: 1px solid #aa7700;
        border-left: 4px solid #ffaa00;
        border-radius: 4px;
        padding: 16px 20px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 1px;
        color: #ffc060;
    }
    .risk-low {
        background: linear-gradient(135deg, #001a0a, #001206);
        border: 1px solid #007733;
        border-left: 4px solid #00cc55;
        border-radius: 4px;
        padding: 16px 20px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 1px;
        color: #50e890;
    }

    /* ---- Divider ---- */
    .cmd-divider {
        border: none;
        border-top: 1px solid #1a3a5c;
        margin: 20px 0;
    }

    /* ---- Buttons ---- */
    .stButton > button {
        background: linear-gradient(135deg, #00408a 0%, #0060cc 100%) !important;
        color: #e8f4ff !important;
        border: 1px solid #0080ff !important;
        border-radius: 3px !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        letter-spacing: 3px !important;
        text-transform: uppercase !important;
        padding: 10px 24px !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #0060cc 0%, #0080ff 100%) !important;
        box-shadow: 0 0 20px rgba(0, 128, 255, 0.4) !important;
    }

    /* ---- Sliders ---- */
    [data-testid="stSlider"] label {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.8rem !important;
        letter-spacing: 1px !important;
        color: #7ec8ff !important;
    }

    /* ---- Inputs ---- */
    .stTextInput input, .stNumberInput input {
        background: #0a1628 !important;
        border: 1px solid #1a3a5c !important;
        color: #c8d8e8 !important;
        border-radius: 3px !important;
        font-family: 'Share Tech Mono', monospace !important;
    }

    /* ---- Info Box ---- */
    .stInfo {
        background: rgba(0, 80, 160, 0.12) !important;
        border: 1px solid #1a4a7a !important;
        color: #7ec8ff !important;
    }

    /* ---- Dataframe ---- */
    [data-testid="stDataFrame"] {
        border: 1px solid #1a3a5c !important;
        border-radius: 4px !important;
    }

    /* ---- Status dot ---- */
    .status-dot {
        display: inline-block;
        width: 8px; height: 8px;
        background: #00cc55;
        border-radius: 50%;
        box-shadow: 0 0 6px #00cc55;
        margin-right: 6px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }

    /* ---- Forecast card ---- */
    .forecast-card {
        background: linear-gradient(135deg, #0a1628 0%, #0d1e38 100%);
        border: 1px solid #1a3a5c;
        border-top: 2px solid #0060cc;
        border-radius: 4px;
        padding: 18px;
        text-align: center;
    }
    .forecast-card .fc-label {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.68rem;
        color: #5a8ab0;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .forecast-card .fc-value {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #e0f0ff;
    }
    .forecast-card .fc-sub {
        font-family: 'Exo 2', sans-serif;
        font-size: 0.75rem;
        color: #4a7a9a;
        margin-top: 4px;
    }

    /* ── hide default streamlit elements ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 1.5rem !important;}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#   SIDEBAR — Navigation Panel
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 20px 0;'>
        <div style='font-family: Rajdhani, sans-serif; font-size: 1.1rem;
                    letter-spacing: 3px; color: #7ec8ff; text-transform: uppercase;
                    border-bottom: 1px solid #1a3a5c; padding-bottom: 12px;'>
            🛡️ COMMAND NAV
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### 📍 Village Details")
    village_name = st.text_input("Village Name", value="Rampur", label_visibility="collapsed",
                                  placeholder="Enter village name…")
    st.caption("🏘️ Village / Gram Panchayat Name")

    population = st.number_input("👥 Population", min_value=100, max_value=50000,
                                   value=4200, step=100)

    st.markdown("<hr style='border-color:#1a3a5c; margin: 16px 0;'>", unsafe_allow_html=True)

    st.markdown("##### 🗂️ Sections")
    st.markdown("""
    <div style='font-family: Share Tech Mono, monospace; font-size: 0.75rem;
                color: #4a8ab0; line-height: 2.2;'>
        📊 &nbsp;VILLAGE INPUT<br>
        🚨 &nbsp;RISK ASSESSMENT<br>
        🚛 &nbsp;TANKER ALLOCATION<br>
        📈 &nbsp;FORECASTING
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1a3a5c; margin: 16px 0;'>", unsafe_allow_html=True)

    st.markdown("""
    <div style='font-family: Share Tech Mono, monospace; font-size: 0.65rem;
                color: #2a5a7a; line-height: 1.8;'>
        SYS VERSION: v2.4.1<br>
        DATA FEED: LIVE<br>
        AUTHORITY: STATE WATER DEPT.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#   HEADER BANNER
# ══════════════════════════════════════════════════════════════
st.markdown(f"""
<div class='gov-header'>
    <h1>🛡️ District Water Command Center</h1>
    <div class='sub'>Integrated Drought Warning &amp; Smart Tanker Management System</div>
    <div class='badge'><span class='status-dot'></span>SYSTEM ACTIVE</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#   SECTION 1 — VILLAGE INPUT
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-header'>
    <span>📊 Section 1 — Village Input</span>
</div>
""", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        rainfall = st.slider("🌧️  Rainfall (mm)", min_value=0, max_value=600, value=150, step=5)
    with col2:
        groundwater = st.slider("🕳️  Groundwater Depth (meters)", min_value=0, max_value=100, value=20, step=1)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("🏘️ Village", village_name)
    with c2:
        st.metric("👥 Population", f"{int(population):,}")
    with c3:
        stress_preview = (600 - rainfall) + (20 - groundwater)
        st.metric("💦 Stress Index (preview)", stress_preview)

st.markdown("<hr class='cmd-divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#   PREDICT BUTTON
# ══════════════════════════════════════════════════════════════
_, btn_col, _ = st.columns([2, 3, 2])
with btn_col:
    predict_clicked = st.button("⚡  EXECUTE ASSESSMENT", use_container_width=True)

st.markdown("<hr class='cmd-divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#   RESULTS
# ══════════════════════════════════════════════════════════════
if predict_clicked:

    tankers      = predict_tanker_need(rainfall, groundwater, population)
    stress_index = (600 - rainfall) + (20 - groundwater)
    risk         = get_drought_risk(rainfall, groundwater)

    if risk == "High":
        risk_icon, risk_color = "🔴", "#ff3300"
    elif risk == "Medium":
        risk_icon, risk_color = "🟡", "#ffaa00"
    else:
        risk_icon, risk_color = "🟢", "#00cc55"

    # ── Section 2: Risk Assessment ──────────────────────────
    st.markdown("""
    <div class='section-header'>
        <span>🚨 Section 2 — Risk Assessment</span>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        ra1, ra2, ra3 = st.columns(3)
        with ra1:
            st.metric("🌧️ Rainfall Input", f"{rainfall} mm",
                      delta="Critical" if rainfall < 100 else ("Moderate" if rainfall < 250 else "Safe"),
                      delta_color="inverse")
        with ra2:
            st.metric("🕳️ Groundwater Depth", f"{groundwater} m",
                      delta="Critical" if groundwater > 50 else ("Watch" if groundwater > 30 else "Normal"),
                      delta_color="inverse")
        with ra3:
            st.metric("🚨 Threat Level", f"{risk_icon} {risk}")

        if risk == "High":
            st.markdown(f"""<div class='risk-high'>
                🔴 &nbsp; HIGH THREAT — Immediate emergency tanker deployment required for <b>{village_name}</b>.
                Contact District Collector and activate emergency protocol.
            </div>""", unsafe_allow_html=True)
        elif risk == "Medium":
            st.markdown(f"""<div class='risk-medium'>
                🟡 &nbsp; ELEVATED RISK — Pre-position tankers on standby for <b>{village_name}</b>.
                Increase monitoring frequency to 12-hour cycles.
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class='risk-low'>
                🟢 &nbsp; SITUATION STABLE — Routine monitoring sufficient for <b>{village_name}</b>.
                Next scheduled assessment in 7 days.
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='cmd-divider'>", unsafe_allow_html=True)

    # ── Section 3: Tanker Allocation ────────────────────────
    st.markdown("""
    <div class='section-header'>
        <span>🚛 Section 3 — Tanker Allocation</span>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        ta1, ta2, ta3, ta4 = st.columns(4)
        with ta1:
            st.metric("🚛 Tankers Deployed", f"{tankers}")
        with ta2:
            litres = tankers * 10000
            st.metric("💧 Water Capacity", f"{litres:,} L")
        with ta3:
            per_person = round(litres / population, 1)
            st.metric("👤 Per Capita (L)", f"{per_person}")
        with ta4:
            st.metric("💦 Stress Index", stress_index)

        st.markdown("**Water Stress Gauge**")
        normalised = min(1.0, max(0.0, stress_index / 620))
        st.progress(normalised, text=f"Stress Level: {stress_index} / 620 (max)")

        summary_data = {
            "Parameter": ["Village", "Population", "Rainfall (mm)", "Groundwater Depth (m)",
                           "Water Stress Index", "Tankers Deployed", "Water Supplied (L)",
                           "Per Capita (L/person)", "Risk Level"],
            "Value":     [village_name, f"{int(population):,}", rainfall, groundwater,
                          stress_index, tankers, f"{litres:,}", per_person, f"{risk_icon} {risk}"],
            "Status":    ["—", "—",
                          "🔴 Critical" if rainfall < 100 else ("🟡 Low" if rainfall < 250 else "🟢 Normal"),
                          "🔴 Deep" if groundwater > 50 else ("🟡 Moderate" if groundwater > 30 else "🟢 Shallow"),
                          "🔴 High" if stress_index > 500 else ("🟡 Medium" if stress_index > 300 else "🟢 Low"),
                          "—", "—", "—", f"{risk_icon} {risk}"]
        }
        st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)

    st.markdown("<hr class='cmd-divider'>", unsafe_allow_html=True)

    # ── Section 3.5: AI-Based Tanker Deployment Recommendation ──
    st.markdown("""
    <div class='section-header'>
        <span>🤖 AI-Based Tanker Deployment Recommendation</span>
    </div>
    """, unsafe_allow_html=True)

    with st.container():

        # ── Per-risk bordered recommendation panel ────────────
        if risk == "High":
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #200808, #180404);
                        border: 2px solid #cc2200; border-radius: 6px;
                        padding: 24px 28px; margin-bottom: 14px;'>
                <div style='font-family: Rajdhani, sans-serif; font-size: 1.4rem;
                            font-weight: 700; color: #ff4422; letter-spacing: 2px;
                            text-transform: uppercase; margin-bottom: 6px;'>
                    🚨 DIRECTIVE: IMMEDIATE TANKER DISPATCH
                </div>
                <div style='font-family: Share Tech Mono, monospace; font-size: 0.72rem;
                            color: #882200; letter-spacing: 3px; margin-bottom: 16px;'>
                    AI CONFIDENCE: HIGH &nbsp;|&nbsp; RESPONSE WINDOW: &lt; 6 HOURS
                </div>
                <div style='font-family: Exo 2, sans-serif; font-size: 0.92rem;
                            color: #ffb0a0; line-height: 1.9;'>
                    The AI model has classified <b style='color:#ff6644;'>{village_name}</b>
                    as a <b style='color:#ff4422;'>HIGH RISK</b> zone based on critically low
                    rainfall ({rainfall} mm) and deep groundwater ({groundwater} m).
                    Immediate dispatch of <b style='color:#ffddcc;'>{tankers} tankers</b> is recommended
                    without waiting for further monitoring cycles.<br><br>
                    <b style='color:#ff8866;'>Recommended Actions:</b><br>
                    ① &nbsp;Dispatch {tankers} tankers from Nagpur HQ within 6 hours<br>
                    ② &nbsp;Notify District Collector and activate Emergency Water Protocol<br>
                    ③ &nbsp;Set up community distribution point at village centre<br>
                    ④ &nbsp;Re-assess groundwater levels every 24 hours<br>
                    ⑤ &nbsp;Flag village for bore-well deepening / rainwater harvesting scheme
                </div>
            </div>
            """, unsafe_allow_html=True)

        elif risk == "Medium":
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #191000, #120c00);
                        border: 2px solid #aa7700; border-radius: 6px;
                        padding: 24px 28px; margin-bottom: 14px;'>
                <div style='font-family: Rajdhani, sans-serif; font-size: 1.4rem;
                            font-weight: 700; color: #ffaa00; letter-spacing: 2px;
                            text-transform: uppercase; margin-bottom: 6px;'>
                    ⚠️ DIRECTIVE: SCHEDULED SUPPLY
                </div>
                <div style='font-family: Share Tech Mono, monospace; font-size: 0.72rem;
                            color: #886600; letter-spacing: 3px; margin-bottom: 16px;'>
                    AI CONFIDENCE: MEDIUM &nbsp;|&nbsp; RESPONSE WINDOW: 24–48 HOURS
                </div>
                <div style='font-family: Exo 2, sans-serif; font-size: 0.92rem;
                            color: #ffd080; line-height: 1.9;'>
                    The AI model has classified <b style='color:#ffcc44;'>{village_name}</b>
                    as a <b style='color:#ffaa00;'>MEDIUM RISK</b> zone. Conditions are
                    deteriorating but have not yet reached the emergency threshold.
                    A scheduled supply of <b style='color:#ffeecc;'>{tankers} tankers</b>
                    should be pre-positioned within 48 hours as a precautionary measure.<br><br>
                    <b style='color:#ffcc66;'>Recommended Actions:</b><br>
                    ① &nbsp;Schedule {tankers} tankers for delivery within 48 hours<br>
                    ② &nbsp;Alert Taluka Water Officer — place tankers on standby<br>
                    ③ &nbsp;Increase monitoring frequency to every 12 hours<br>
                    ④ &nbsp;Advise village head to implement household water rationing<br>
                    ⑤ &nbsp;Prepare contingency plan in case situation escalates to High
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #001a08, #001205);
                        border: 2px solid #007733; border-radius: 6px;
                        padding: 24px 28px; margin-bottom: 14px;'>
                <div style='font-family: Rajdhani, sans-serif; font-size: 1.4rem;
                            font-weight: 700; color: #00cc55; letter-spacing: 2px;
                            text-transform: uppercase; margin-bottom: 6px;'>
                    ✅ DIRECTIVE: MONITORING ONLY
                </div>
                <div style='font-family: Share Tech Mono, monospace; font-size: 0.72rem;
                            color: #006622; letter-spacing: 3px; margin-bottom: 16px;'>
                    AI CONFIDENCE: HIGH &nbsp;|&nbsp; NEXT REVIEW: 7 DAYS
                </div>
                <div style='font-family: Exo 2, sans-serif; font-size: 0.92rem;
                            color: #80e8a8; line-height: 1.9;'>
                    The AI model has classified <b style='color:#44ee88;'>{village_name}</b>
                    as a <b style='color:#00cc55;'>LOW RISK</b> zone. Rainfall ({rainfall} mm)
                    and groundwater levels ({groundwater} m) are within acceptable ranges.
                    No tanker deployment is needed at this time; available tankers should be
                    redirected to higher-priority villages in this district.<br><br>
                    <b style='color:#44ee88;'>Recommended Actions:</b><br>
                    ① &nbsp;No tanker dispatch required — reallocate fleet to High/Medium zones<br>
                    ② &nbsp;Continue standard 7-day monitoring cycle<br>
                    ③ &nbsp;Ensure local reservoirs and handpumps are operational<br>
                    ④ &nbsp;Log current readings as baseline for seasonal comparison<br>
                    ⑤ &nbsp;No immediate intervention required by District Administration
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Decision logic explainer ──────────────────────────
        st.markdown(f"""
        <div style='background: rgba(0, 60, 120, 0.12);
                    border: 1px solid #1a3a5c; border-left: 3px solid #00a8ff;
                    border-radius: 4px; padding: 16px 20px; margin-top: 6px;'>
            <div style='font-family: Share Tech Mono, monospace; font-size: 0.68rem;
                        color: #3a7aaa; letter-spacing: 3px; margin-bottom: 10px;'>
                🧠 HOW THIS CONVERTS PREDICTION INTO ACTIONABLE PLANNING
            </div>
            <div style='font-family: Exo 2, sans-serif; font-size: 0.83rem;
                        color: #6a9cbd; line-height: 1.85;'>
                The ML model predicts <b style='color:#a0d0f0;'>{tankers} tankers</b> — a raw number.
                This AI Recommendation layer translates that number into a
                <b style='color:#a0d0f0;'>decision with a deadline and named owner</b>:<br><br>
                &nbsp;&nbsp;📊 &nbsp;<b style='color:#88b8d8;'>Prediction</b> tells you
                <i>how many</i> tankers are needed.<br>
                &nbsp;&nbsp;🤖 &nbsp;<b style='color:#88b8d8;'>Recommendation</b> tells you
                <i>when</i> to send them, <i>who</i> to notify, and <i>what else</i> to do.<br><br>
                This closes the gap between a data output and a field action — the exact step
                that typically causes delays in manual drought response workflows.
                Risk thresholds (High / Medium / Low) map directly to Standard Operating
                Procedures, so any officer reading this screen knows the next step without
                needing to interpret the numbers themselves.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='cmd-divider'>", unsafe_allow_html=True)

    # ── Section 4: Forecasting ───────────────────────────────
    st.markdown("""
    <div class='section-header'>
        <span>📈 Section 4 — Operational Forecast</span>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        fc1, fc2, fc3 = st.columns(3)

        with fc1:
            t7 = predict_tanker_need(max(0, rainfall - 20), min(100, groundwater + 5), population)
            st.markdown(f"""<div class='forecast-card'>
                <div class='fc-label'>📅 7-Day Projection</div>
                <div class='fc-value'>{t7} Tankers</div>
                <div class='fc-sub'>Rainfall ↓20mm · GW ↑5m</div>
            </div>""", unsafe_allow_html=True)

        with fc2:
            t14 = predict_tanker_need(max(0, rainfall - 40), min(100, groundwater + 10), population)
            st.markdown(f"""<div class='forecast-card'>
                <div class='fc-label'>📅 14-Day Projection</div>
                <div class='fc-value'>{t14} Tankers</div>
                <div class='fc-sub'>Rainfall ↓40mm · GW ↑10m</div>
            </div>""", unsafe_allow_html=True)

        with fc3:
            t30 = predict_tanker_need(max(0, rainfall - 80), min(100, groundwater + 20), population)
            st.markdown(f"""<div class='forecast-card'>
                <div class='fc-label'>📅 30-Day Projection</div>
                <div class='fc-value'>{t30} Tankers</div>
                <div class='fc-sub'>Rainfall ↓80mm · GW ↑20m</div>
            </div>""", unsafe_allow_html=True)

        trend = "📈 WORSENING" if t30 > tankers else ("📉 IMPROVING" if t30 < tankers else "➡️ STABLE")
        st.info(f"**30-Day Trend:** {trend} — from {tankers} → {t30} tankers over the projection window.")

else:
    st.markdown("""
    <div style='text-align:center; padding: 40px; color: #2a5a7a;
                font-family: Share Tech Mono, monospace; font-size: 0.85rem;
                letter-spacing: 2px; border: 1px dashed #1a3a5c; border-radius: 4px;'>
        ⚡ &nbsp; AWAITING OPERATOR INPUT — ADJUST PARAMETERS AND EXECUTE ASSESSMENT
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # still show section placeholders so layout feels structured
    for section in ["🚨 Section 2 — Risk Assessment", "🚛 Section 3 — Tanker Allocation", "📈 Section 4 — Operational Forecast"]:
        st.markdown(f"<div class='section-header'><span>{section}</span></div>", unsafe_allow_html=True)
        st.markdown("""<div style='padding: 12px 16px; color: #1e4a6a;
                        font-family: Share Tech Mono, monospace; font-size: 0.75rem;'>
                        — DATA PENDING EXECUTION —</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#   SECTION 5 — DISTRICT SEVERITY RANKING TABLE
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-header'>
    <span>🏆 Section 5 — District Severity Ranking</span>
</div>
""", unsafe_allow_html=True)

# ── Severity Score Formula ────────────────────────────────────
# Score = (600 - rainfall) * 0.5   →  low rain = high score  (max ~300)
#       + groundwater_depth * 3    →  deep water = high score (max ~300)
#       + population / 1000        →  more people = more urgent (variable)
# Normalised to 0–100 for readability.
# This formula weights groundwater depth most heavily because a dry
# aquifer takes months to recover, making it the strongest indicator
# of a prolonged crisis requiring sustained tanker supply.

def severity_score(rainfall, groundwater, population):
    raw = (600 - rainfall) * 0.5 + groundwater * 3 + population / 1000
    max_possible = 600 * 0.5 + 100 * 3 + 50  # normalise against ceiling
    return round((raw / max_possible) * 100, 1)

# ── Village registry — add your own villages here ─────────────
ALL_VILLAGES = [
    {"Village Name": "Ramtek",    "rainfall": 95,  "groundwater": 52, "population": 18000},
    {"Village Name": "Parseoni",  "rainfall": 60,  "groundwater": 67, "population": 8500},
    {"Village Name": "Hingna",    "rainfall": 140, "groundwater": 38, "population": 12000},
    {"Village Name": "Butibori",  "rainfall": 210, "groundwater": 28, "population": 22000},
    {"Village Name": "Kamptee",   "rainfall": 175, "groundwater": 19, "population": 31000},
    {"Village Name": "Katol",     "rainfall": 85,  "groundwater": 44, "population": 9800},
    {"Village Name": "Savner",    "rainfall": 230, "groundwater": 22, "population": 14500},
    {"Village Name": "Narkhed",   "rainfall": 55,  "groundwater": 71, "population": 7200},
]

# Also inject the currently assessed village (from sidebar) so it
# appears live in the ranking alongside the static villages.
if village_name not in [v["Village Name"] for v in ALL_VILLAGES]:
    ALL_VILLAGES.append({
        "Village Name": f"★ {village_name}",
        "rainfall": rainfall if predict_clicked else 150,
        "groundwater": groundwater if predict_clicked else 20,
        "population": int(population),
    })

# ── Build the ranked dataframe ────────────────────────────────
rows = []
for v in ALL_VILLAGES:
    score = severity_score(v["rainfall"], v["groundwater"], v["population"])
    risk  = get_drought_risk(v["rainfall"], v["groundwater"])
    tanks = predict_tanker_need(v["rainfall"], v["groundwater"], v["population"])

    risk_icon_map = {"High": "🔴 High", "Medium": "🟡 Medium", "Low": "🟢 Low"}
    priority_map  = {"High": "🚨 IMMEDIATE", "Medium": "⚠️ STANDBY", "Low": "✅ ROUTINE"}

    rows.append({
        "Rank":           0,           # filled after sort
        "Village Name":   v["Village Name"],
        "Severity Score": score,
        "Tankers Needed": tanks,
        "Risk Level":     risk_icon_map[risk],
        "Action":         priority_map[risk],
        "Population":     f"{v['population']:,}",
        "Rainfall (mm)":  v["rainfall"],
        "GW Depth (m)":   v["groundwater"],
    })

rank_df = (
    pd.DataFrame(rows)
    .sort_values("Severity Score", ascending=False)
    .reset_index(drop=True)
)
rank_df["Rank"] = ["🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"
                   for i in range(len(rank_df))]

with st.container():
    # ── Top-3 emergency callout cards ────────────────────────
    st.markdown("##### 🚨 Top 3 Priority Deployments")
    top3_cols = st.columns(3)
    for idx, col in enumerate(top3_cols):
        if idx < len(rank_df):
            row = rank_df.iloc[idx]
            border_colors = ["#ff3300", "#ff8800", "#ffaa00"]
            with col:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #0d1628, #111e38);
                            border: 1px solid {border_colors[idx]};
                            border-top: 3px solid {border_colors[idx]};
                            border-radius: 4px; padding: 16px; text-align: center;'>
                    <div style='font-family: Share Tech Mono, monospace; font-size: 0.65rem;
                                color: #5a8ab0; letter-spacing: 2px; margin-bottom: 4px;'>
                        PRIORITY {idx+1}
                    </div>
                    <div style='font-family: Rajdhani, sans-serif; font-size: 1.2rem;
                                font-weight: 700; color: #e0f0ff; margin-bottom: 6px;'>
                        {row["Village Name"]}
                    </div>
                    <div style='font-family: Rajdhani, sans-serif; font-size: 2rem;
                                font-weight: 700; color: {border_colors[idx]};'>
                        {row["Severity Score"]}
                    </div>
                    <div style='font-family: Share Tech Mono, monospace; font-size: 0.65rem;
                                color: #5a8ab0; margin: 4px 0 10px;'>SEVERITY SCORE</div>
                    <div style='font-size: 0.85rem; color: #a0c8e0;'>
                        🚛 {row["Tankers Needed"]} tankers &nbsp;|&nbsp; {row["Risk Level"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Full ranked table ─────────────────────────────────────
    st.markdown("##### 📋 Full District Ranking — Sorted by Severity (High → Low)")

    display_cols = ["Rank", "Village Name", "Severity Score", "Tankers Needed",
                    "Risk Level", "Action", "Population", "Rainfall (mm)", "GW Depth (m)"]

    st.dataframe(
        rank_df[display_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Severity Score": st.column_config.ProgressColumn(
                "Severity Score",
                help="Composite drought severity (0–100). Higher = more critical.",
                format="%.1f",
                min_value=0,
                max_value=100,
            ),
            "Tankers Needed": st.column_config.NumberColumn(
                "🚛 Tankers",
                help="Tankers required based on ML model prediction.",
            ),
        }
    )

    # ── How this helps tanker prioritization ─────────────────
    total_tankers = rank_df["Tankers Needed"].sum()
    high_count    = (rank_df["Risk Level"].str.contains("High")).sum()

    st.markdown(f"""
    <div style='margin-top: 18px; background: linear-gradient(135deg, #071828, #0a1e30);
                border: 1px solid #1a3a5c; border-left: 4px solid #00a8ff;
                border-radius: 4px; padding: 18px 22px;'>
        <div style='font-family: Rajdhani, sans-serif; font-size: 1rem; font-weight: 700;
                    color: #7ec8ff; letter-spacing: 2px; text-transform: uppercase;
                    margin-bottom: 10px;'>
            🧠 How This Table Drives Tanker Prioritization
        </div>
        <div style='font-family: Exo 2, sans-serif; font-size: 0.88rem;
                    color: #90b8d8; line-height: 1.85;'>
            <b style='color:#c8e8ff;'>1. Severity Score replaces guesswork.</b>
            Instead of field officers making ad-hoc calls, each village gets an objective
            0–100 score combining rainfall deficit, groundwater depletion, and population
            pressure. The highest-scoring village always gets first dispatch. <br><br>
            <b style='color:#c8e8ff;'>2. Ranked order = dispatch order.</b>
            Tanker convoys should be sent top-to-bottom down this list. Right now
            <b style='color:#ffaa00;'>{high_count} village(s) are at High risk</b>
            and require immediate allocation before any Medium or Low villages are served.<br><br>
            <b style='color:#c8e8ff;'>3. Total fleet visibility.</b>
            The district currently needs <b style='color:#00ccff;'>{total_tankers} tankers</b>
            in total. If fewer are available, you can instantly see which villages to
            de-prioritize without endangering the most vulnerable populations.<br><br>
            <b style='color:#c8e8ff;'>4. Live re-ranking.</b>
            The row marked ★ reflects whatever village and parameters you set in the
            sidebar — so field teams can add a new village and instantly see where it
            ranks against existing commitments before a single tanker is dispatched.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='cmd-divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#   MAP SECTION — pydeck satellite (no extra install needed)
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-header'>
    <span>🛰️ Satellite Tanker Route Map — Nagpur District</span>
</div>
""", unsafe_allow_html=True)

import pydeck as pdk

# ── Village + HQ data ─────────────────────────────────────────
NAGPUR_LAT, NAGPUR_LON = 21.1458, 79.0882

MAP_VILLAGES = [
    {"name": "Ramtek",   "lat": 21.3942, "lon": 79.3259, "rainfall": 95,  "groundwater": 52, "population": 18000},
    {"name": "Hingna",   "lat": 21.0747, "lon": 78.8367, "rainfall": 140, "groundwater": 38, "population": 12000},
    {"name": "Parseoni", "lat": 21.3200, "lon": 79.0100, "rainfall": 60,  "groundwater": 67, "population": 8500},
]

for v in MAP_VILLAGES:
    v["tankers"] = predict_tanker_need(v["rainfall"], v["groundwater"], v["population"])
    v["risk"]    = get_drought_risk(v["rainfall"], v["groundwater"])
    # pydeck colours as [R, G, B, A]
    v["color"]   = [220, 30,  10,  230] if v["risk"] == "High" \
             else ([255, 160,  0,  220] if v["risk"] == "Medium" \
             else  [0,   200, 80,  210])
    v["radius"]  = 1800 + v["tankers"] * 200   # bigger circle = more tankers needed
    v["label"]   = (f"{v['name']} | {v['risk']} Risk | "
                    f"{v['tankers']} Tankers | Rain: {v['rainfall']}mm | GW: {v['groundwater']}m")

# ── Route lines: HQ → each village ───────────────────────────
route_data = [
    {
        "source_lat": NAGPUR_LAT, "source_lon": NAGPUR_LON,
        "target_lat": v["lat"],   "target_lon": v["lon"],
        "color": v["color"],
        "name": v["name"],
    }
    for v in MAP_VILLAGES
]

# ── HQ marker ─────────────────────────────────────────────────
hq_data = [{"lat": NAGPUR_LAT, "lon": NAGPUR_LON,
            "label": "🏠 Nagpur — Tanker Dispatch HQ",
            "color": [0, 160, 255, 240], "radius": 2200}]

# ── pydeck layers ─────────────────────────────────────────────

# 1. Satellite imagery base — Google Maps-style
# Uses ESRI World Imagery (free, no API key)
satellite_layer = pdk.Layer(
    "TileLayer",
    data=None,
    get_tile_data="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    min_zoom=0,
    max_zoom=19,
    tile_size=256,
    opacity=1.0,
)

# 2. Route arcs HQ → villages
arc_layer = pdk.Layer(
    "ArcLayer",
    data=route_data,
    get_source_position=["source_lon", "source_lat"],
    get_target_position=["target_lon", "target_lat"],
    get_source_color=[0, 160, 255, 180],
    get_target_color="color",
    get_width=4,
    pickable=True,
    auto_highlight=True,
)

# 3. Village circles — size encodes tanker demand
village_layer = pdk.Layer(
    "ScatterplotLayer",
    data=MAP_VILLAGES,
    get_position=["lon", "lat"],
    get_fill_color="color",
    get_radius="radius",
    radius_min_pixels=8,
    radius_max_pixels=40,
    pickable=True,
    auto_highlight=True,
    stroked=True,
    get_line_color=[255, 255, 255, 120],
    line_width_min_pixels=1,
)

# 4. HQ marker
hq_layer = pdk.Layer(
    "ScatterplotLayer",
    data=hq_data,
    get_position=["lon", "lat"],
    get_fill_color="color",
    get_radius="radius",
    radius_min_pixels=10,
    pickable=True,
    stroked=True,
    get_line_color=[255, 255, 255, 200],
    line_width_min_pixels=2,
)

# 5. Village name labels
text_layer = pdk.Layer(
    "TextLayer",
    data=MAP_VILLAGES,
    get_position=["lon", "lat"],
    get_text="name",
    get_size=14,
    get_color=[240, 240, 240, 230],
    get_anchor_x="'middle'",
    get_pixel_offset=[0, -28],
    billboard=True,
)

# ── View state ────────────────────────────────────────────────
view_state = pdk.ViewState(
    latitude=NAGPUR_LAT,
    longitude=NAGPUR_LON,
    zoom=8.5,
    pitch=35,        # slight 3-D tilt for depth
    bearing=0,
)

# ── Tooltip ───────────────────────────────────────────────────
tooltip = {
    "html": """
        <div style='background:#0a1628; border:1px solid #1a3a5c;
                    border-left:3px solid #00a8ff; padding:10px 14px;
                    font-family:monospace; font-size:12px; color:#c8e8ff;
                    border-radius:4px; line-height:1.7;'>
            <b style='color:#00ccff;'>{name}</b><br>
            🚨 Risk: {risk}<br>
            🚛 Tankers: {tankers}<br>
            🌧️ Rainfall: {rainfall} mm<br>
            🕳️ Groundwater: {groundwater} m<br>
            👥 Population: {population}
        </div>
    """,
    "style": {"backgroundColor": "transparent", "border": "none"},
}

deck = pdk.Deck(
    layers=[satellite_layer, arc_layer, village_layer, hq_layer, text_layer],
    initial_view_state=view_state,
    tooltip=tooltip,
    map_style=None,   # None = use our custom TileLayer instead of a mapbox style
)

st.pydeck_chart(deck, use_container_width=True)

# ── Legend ────────────────────────────────────────────────────
leg1, leg2, leg3, leg4 = st.columns(4)
for col, color, label, sublabel in [
    (leg1, "#dc1e0a", "🔴 HIGH RISK",   "Immediate dispatch"),
    (leg2, "#ffa000", "🟡 MEDIUM RISK", "Scheduled supply"),
    (leg3, "#00c850", "🟢 LOW RISK",    "Monitoring only"),
    (leg4, "#00a0ff", "🔵 HQ NAGPUR",   "Tanker dispatch hub"),
]:
    col.markdown(f"""
    <div style='background:#0a1628; border:1px solid {color};
                border-top:2px solid {color}; border-radius:4px;
                padding:10px; text-align:center;'>
        <div style='font-family:Rajdhani,sans-serif; font-weight:700;
                    font-size:0.85rem; color:{color};'>{label}</div>
        <div style='font-family:Share Tech Mono,monospace; font-size:0.65rem;
                    color:#4a7a9a; letter-spacing:1px; margin-top:3px;'>{sublabel}</div>
    </div>
    """, unsafe_allow_html=True)

st.caption("🛰️ Satellite imagery: ESRI World Imagery · Circle size = tanker demand · Hover markers for details")

# ── Footer ────────────────────────────────────────────────────
st.markdown("<hr class='cmd-divider'>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; font-family: Share Tech Mono, monospace;
            font-size: 0.65rem; color: #1e4a6a; letter-spacing: 2px; padding: 8px 0;'>
    DISTRICT WATER COMMAND CENTER &nbsp;|&nbsp; INTEGRATED DROUGHT WARNING & SMART TANKER MANAGEMENT
    &nbsp;|&nbsp; STREAMLIT + SCIKIT-LEARN
</div>
""", unsafe_allow_html=True)
