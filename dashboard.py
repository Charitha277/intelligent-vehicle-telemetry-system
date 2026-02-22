import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(layout="wide")

# Auto refresh every 3 seconds
st_autorefresh(interval=3000, key="datarefresh")

# -----------------------------
# Beautiful UI Styling
# -----------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #141E30, #243B55);
    color: white;
}

.title {
    font-size: 40px;
    font-weight: bold;
    text-align: center;
    background: -webkit-linear-gradient(#00f5ff, #ff00c8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 30px;
}

.metric-card {
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
    font-size: 18px;
    font-weight: bold;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.5);
}

.healthy {
    background: linear-gradient(135deg, #00b09b, #96c93d);
}

.warning {
    background: linear-gradient(135deg, #f7971e, #ffd200);
}

.critical {
    background: linear-gradient(135deg, #ff416c, #ff4b2b);
}

.alert-box {
    padding: 20px;
    border-radius: 12px;
    font-size: 20px;
    font-weight: bold;
    text-align: center;
    animation: blink 1.2s infinite;
}

@keyframes blink {
    50% { opacity: 0.6; }
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🚗 Intelligent Vehicle Telemetry & Anomaly Detection System</div>', unsafe_allow_html=True)

# -----------------------------
# Fetch Data
# -----------------------------
try:
    response = requests.get("http://127.0.0.1:8000/api/telemetry/")
    data = response.json()

    if len(data) == 0:
        st.warning("No telemetry data available.")
        st.stop()

    df = pd.DataFrame(data)
    latest = df.iloc[-1]

    severity = latest["severity"]
    health_score = latest["health_score"]

    # Dynamic color selection
    if severity == "Healthy":
        card_class = "healthy"
        gauge_color = "green"
    elif severity == "Warning":
        card_class = "warning"
        gauge_color = "orange"
    else:
        card_class = "critical"
        gauge_color = "red"

    # -----------------------------
    # Metric Cards
    # -----------------------------
    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(f'<div class="metric-card {card_class}">Speed<br>{latest["speed"]} km/h</div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric-card {card_class}">Fuel<br>{latest["fuel_level"]}%</div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="metric-card {card_class}">Temperature<br>{latest["temperature"]} °C</div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="metric-card {card_class}">Health Score<br>{health_score}</div>', unsafe_allow_html=True)

    st.markdown("<br><hr style='border: 1px solid #444;'><br>", unsafe_allow_html=True)

    # -----------------------------
    # Gauge + Speed Chart
    # -----------------------------
    col_left, col_right = st.columns([1, 2])

    with col_left:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=health_score,
            title={'text': "Vehicle Health"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': gauge_color},
                'steps': [
                    {'range': [0, 50], 'color': "#ff4b2b"},
                    {'range': [50, 80], 'color': "#ffd200"},
                    {'range': [80, 100], 'color': "#96c93d"},
                ],
            }
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_right:
        fig_speed = px.line(df, x="timestamp", y="speed", title="📈 Speed Over Time")
        st.plotly_chart(fig_speed, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------
    # Temperature Chart
    # -----------------------------
    fig_temp = px.line(df, x="timestamp", y="temperature", title="🌡 Temperature Over Time")
    st.plotly_chart(fig_temp, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------
    # Severity Distribution
    # -----------------------------
    severity_count = df["severity"].value_counts().reset_index()
    severity_count.columns = ["severity", "count"]

    fig_pie = px.pie(severity_count, names="severity", values="count", title="📊 System Status Distribution")
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------
    # Live Map
    # -----------------------------
    st.markdown("## 🗺 Live Vehicle Location")

    map_df = pd.DataFrame({
        "lat": [latest["latitude"]],
        "lon": [latest["longitude"]]
    })

    st.map(map_df, zoom=10)

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------
    # Alert Box
    # -----------------------------
    st.markdown("### 🚨 Latest Vehicle Status")

    if severity == "Healthy":
        st.markdown('<div class="alert-box healthy">🟢 VEHICLE HEALTHY</div>', unsafe_allow_html=True)
    elif severity == "Warning":
        st.markdown(f'<div class="alert-box warning">🟡 WARNING: {latest["anomaly_reason"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert-box critical">🔴 CRITICAL ALERT: {latest["anomaly_reason"]}</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error connecting to backend: {e}")