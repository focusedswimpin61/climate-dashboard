import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from io import BytesIO

# ---- SETUP ----
st.set_page_config(page_title="Climate Dashboard", layout="centered")
st.title("🌍 Climate Trends Dashboard (2015–2023)")

# ---- INPUTS ----
city_coords = {
    "Ahmedabad, India": (23.0225, 72.5714),
    "Phoenix, USA": (33.4484, -112.0740)
}
city = st.selectbox("Select City", list(city_coords.keys()))
lat, lon = city_coords[city]

year = st.selectbox("Select Year", list(map(str, range(2015, 2024))))

start = f"{year}0101"
end = f"{year}1231"

# ---- NASA POWER API ----
nasa_url = (
    f"https://power.larc.nasa.gov/api/temporal/daily/point?"
    f"parameters=T2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN"
    f"&start={start}&end={end}"
    f"&latitude={lat}&longitude={lon}"
    f"&community=RE"
    f"&format=JSON"
)

response = requests.get(nasa_url)
data_json = response.json()

if "properties" not in data_json:
    st.error("❌ NASA API failed to return proper data.")
    st.json(data_json)
    st.stop()

params = data_json["properties"]["parameter"]

# ---- DATA CLEANING ----
df = pd.DataFrame({
    "date": list(params["T2M"].keys()),
    "temperature": list(params["T2M"].values()),
    "rainfall": list(params["PRECTOTCORR"].values()),
    "solar": list(params["ALLSKY_SFC_SW_DWN"].values())
})
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M").astype(str)

# ---- MONTHLY AGGREGATION ----
monthly_df = df.groupby("month").mean().reset_index()

# ---- ANOMALY DETECTION ----
mean_temp = monthly_df["temperature"].mean()
std_temp = monthly_df["temperature"].std()
monthly_df["anomaly"] = monthly_df["temperature"].apply(
    lambda x: "🔺 High" if x > mean_temp + std_temp else ("🔻 Low" if x < mean_temp - std_temp else "Normal")
)

# ---- EXPORT TO CSV ----
csv = monthly_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Export Monthly Data to CSV", data=csv, file_name=f"{city.replace(', ','_')}_{year}_climate.csv", mime="text/csv")

# ---- CHARTS ----
st.subheader(f"🌡️ Avg Max Temperature in {city} ({year})")
fig_temp = px.line(monthly_df, x="month", y="temperature", markers=True,
                   color=monthly_df["anomaly"],
                   labels={"temperature": "Temp (°C)", "month": "Month"},
                   title="Temperature with Anomaly Detection")
st.plotly_chart(fig_temp, use_container_width=True)

st.subheader(f"🌧️ Avg Rainfall in {city} ({year})")
fig_rain = px.line(monthly_df, x="month", y="rainfall", markers=True,
                   labels={"rainfall": "Rainfall (mm)", "month": "Month"},
                   title="Monthly Rainfall")
st.plotly_chart(fig_rain, use_container_width=True)

st.subheader(f"☀️ Avg Solar Radiation in {city} ({year})")
fig_solar = px.line(monthly_df, x="month", y="solar", markers=True,
                    labels={"solar": "Solar Radiation", "month": "Month"},
                    title="Monthly Solar Radiation")
st.plotly_chart(fig_solar, use_container_width=True)

# ---- FOOTER ----
st.markdown("---")
st.caption("Built with data from NASA POWER | by Tejas Sharma")
