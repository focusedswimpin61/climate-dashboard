import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

# ---------------- NOAA SETUP ---------------- #
NOAA_TOKEN = os.getenv("NOAA_TOKEN")
headers = {"token": NOAA_TOKEN}

noaa_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
params = {
    "datasetid": "GHCND",
    "datatypeid": "TMAX",
    "stationid": "GHCND:USW00023183",  # Phoenix Sky Harbor
    "startdate": "2022-01-01",
    "enddate": "2022-12-31",
    "units": "metric",
    "limit": 1000
}

response = requests.get(noaa_url, headers=headers, params=params)
data = response.json().get("results", [])

# NOAA → DataFrame
df_temp = pd.DataFrame(data)[["date", "value"]]
df_temp["value"] = df_temp["value"] / 10          # tenths → °C
df_temp["date"]  = pd.to_datetime(df_temp["date"])

# ---------------- NASA POWER SETUP ---------------- #
lat, lon = 33.4484, -112.0740   # Phoenix coordinates
nasa_url = (
    f"https://power.larc.nasa.gov/api/temporal/daily/point?"
    f"parameters=ALLSKY_SFC_SW_DWN"
    f"&start=20220101&end=20221231"
    f"&latitude={lat}&longitude={lon}"
    f"&community=RE"                 # required parameter
    f"&format=JSON"
)

nasa_response = requests.get(nasa_url)
nasa_json = nasa_response.json()

if "properties" in nasa_json and "parameter" in nasa_json["properties"]:
    solar_data = nasa_json["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]

    # NASA → DataFrame
    df_solar = (
        pd.DataFrame.from_dict(solar_data, orient="index", columns=["solar_rad"])
          .reset_index()
          .rename(columns={"index": "date"})
    )
    df_solar["date"] = pd.to_datetime(df_solar["date"])

    # ---------------- MERGE & PLOT ---------------- #
    df_merged = pd.merge(df_temp, df_solar, on="date")

    fig, ax1 = plt.subplots(figsize=(11, 5))

    # Temperature (left axis)
    ax1.plot(df_merged["date"], df_merged["value"],
             color="tab:red", label="Max Temp (°C)")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Temperature (°C)", color="tab:red")

    # Solar radiation (right axis)
    ax2 = ax1.twinx()
    ax2.plot(df_merged["date"], df_merged["solar_rad"],
             color="tab:blue", label="Solar Radiation")
    ax2.set_ylabel("Solar Radiation (kWh/m²/day)", color="tab:blue")

    plt.title("Phoenix: Daily Max Temperature vs. Solar Radiation (2022)")
    fig.tight_layout()
    plt.show()

else:
    print("⚠️ NASA API did not return expected data. Full response:")
    print(nasa_json)
