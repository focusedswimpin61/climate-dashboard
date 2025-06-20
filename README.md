# climate-dashboard
Interactive Streamlit dashboard for exploring temperature, rainfall, and solar radiation trends across cities using NASA POWER data (2015–2023).
```markdown
# 🌎 Climate Trends Dashboard

**Interactive Streamlit app for exploring real-world climate data across cities using NASA POWER (2015–2023)**

---

## 📝 Project Overview

Climate Trends Dashboard is a user-friendly Streamlit web app that lets you visualize and explore key climate variables—**temperature**, **rainfall**, and **solar radiation**—for two cities: Ahmedabad and Phoenix. The app fetches public climate data directly from the [NASA POWER API](https://power.larc.nasa.gov/), providing interactive charts and data analysis from 2015 to 2023.

---

## ✨ Features

- 📊 **Visualize Climate Data**: Interactive charts (Plotly) for temperature, rainfall, and solar radiation  
- 🌐 **Global Data Source**: Uses NASA POWER’s free and public API  
- 🏙️ **City Selection**: Compare Ahmedabad and Phoenix  
- 📅 **Year Selection**: Analyze any year between 2015 and 2023  
- 📈 **Monthly Averages**: See monthly climate trends and patterns  
- 🚨 **Anomaly Detection**: Highlights months with unusual temperatures  
- 📥 **Export Data**: Download results as CSV for further analysis  
- ⚡ **Built with Modern Tools**: Streamlit, Plotly, pandas, and requests

---

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/focusedswimpin61/climate-dashboard.git
   cd climate-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**  
   Visit [http://localhost:8501](http://localhost:8501) to access the dashboard.

---

## 🖼️ Example Visualizations

> _Replace screenshots below with your own once you run the app!_

![Temperature Trends Example](docs/example-temperature.png)
![Rainfall Trends Example](docs/example-rainfall.png)

---

## 📦 Data Source

All climate data is sourced from [NASA POWER](https://power.larc.nasa.gov/), a reliable and publicly available API for global weather and solar data.  
Data is refreshed live each time you run the app.

---

## 👤 Author

- **GitHub:** [focusedswimpin61](https://github.com/focusedswimpin61)
- **Email:** s.tejas.ak@gmail.com

---

## 📄 License

This project is open-source. See [LICENSE](LICENSE) for details.

---

_Questions or suggestions? Feel free to open an issue or contact the author!_
```
