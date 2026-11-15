import os
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Bike Sharing Insights", page_icon="🚲", layout="wide")
st.title("🚲 Bike Sharing Insights")
st.caption("Eksplorasi pola penyewaan sepeda Washington D.C. | Data 2011–2012")

HERE = Path(__file__).resolve().parent
day_path = HERE / "day_data.csv"
hour_path = HERE / "main_data.csv"
if not day_path.exists():
    day_path = HERE.parent / "data" / "day.csv"
if not hour_path.exists():
    hour_path = HERE.parent / "data" / "hour.csv"

SEASON_LABELS = {1: "Musim Dingin", 2: "Musim Semi", 3: "Musim Panas", 4: "Musim Gugur"}
WEATHER_LABELS = {1: "Cerah / sedikit awan", 2: "Berawan / berkabut", 3: "Hujan ringan / salju ringan"}
DAY_COLORS = {"Hari kerja": "#2563EB", "Akhir pekan/libur": "#F59E0B"}


def show(fig):
    """Tampilkan grafik Plotly; kompatibel dengan versi Streamlit lama maupun baru."""
    try:
        st.plotly_chart(fig, width="stretch")
    except TypeError:
        st.plotly_chart(fig, use_container_width=True)


@st.cache_data
def load_data():
    day = pd.read_csv(day_path, parse_dates=["dteday"])
    hour = pd.read_csv(hour_path, parse_dates=["dteday"])
    day["season_label"] = day["season"].map(SEASON_LABELS)
    day["weather_label"] = day["weathersit"].map(WEATHER_LABELS)
    hour["day_type"] = hour["workingday"].map({1:"Hari kerja",0:"Akhir pekan/libur"})
    return day, hour

day, hour = load_data()
min_date, max_date = day.dteday.min().date(), day.dteday.max().date()
with st.sidebar:
    st.header("Filter")
    date_range = st.date_input("Rentang tanggal", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    season_options = ["Semua"] + [SEASON_LABELS[k] for k in sorted(day.season.unique())]
    selected_season = st.selectbox("Musim", season_options)
    weather_options = ["Semua"] + [WEATHER_LABELS[k] for k in sorted(day.weathersit.unique()) if k in WEATHER_LABELS]
    selected_weather = st.selectbox("Cuaca", weather_options)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered = day[(day.dteday.dt.date >= start_date) & (day.dteday.dt.date <= end_date)].copy()
if selected_season != "Semua":
    filtered = filtered[filtered.season_label == selected_season]
if selected_weather != "Semua":
    filtered = filtered[filtered.weather_label == selected_weather]

if filtered.empty:
    st.warning("Tidak ada data untuk kombinasi filter ini.")
    st.stop()

total = int(filtered.cnt.sum())
avg = float(filtered.cnt.mean())
best_day = filtered.loc[filtered.cnt.idxmax()]
c1,c2,c3 = st.columns(3)
c1.metric("Total penyewaan", f"{total:,}")
c2.metric("Rata-rata per hari", f"{avg:,.0f}")
c3.metric("Hari dengan permintaan tertinggi", best_day.dteday.strftime("%d %b %Y"), f"{int(best_day.cnt):,} sewa")

st.subheader("Tren penyewaan harian")
daily = filtered.groupby("dteday", as_index=False).cnt.sum()
fig = px.line(daily, x="dteday", y="cnt", markers=True, labels={"dteday":"Tanggal","cnt":"Jumlah sewa"})
show(fig)

left,right = st.columns(2)
with left:
    st.subheader("Rata-rata menurut musim")
    by_season = filtered.groupby(["season", "season_label"], as_index=False).cnt.mean().sort_values("season")
    fig = px.bar(by_season, x="season_label", y="cnt", text_auto=",.0f",
                 labels={"season_label":"Musim","cnt":"Rata-rata sewa/hari"})
    fig.update_traces(marker_color="#2563EB")
    show(fig)
with right:
    st.subheader("Rata-rata menurut cuaca")
    by_weather = filtered.groupby(["weathersit", "weather_label"], as_index=False).cnt.mean().sort_values("weathersit")
    fig = px.bar(by_weather, x="weather_label", y="cnt", text_auto=",.0f",
                 labels={"weather_label":"Cuaca","cnt":"Rata-rata sewa/hari"})
    fig.update_traces(marker_color="#0F766E")
    fig.update_layout(xaxis_tickangle=-20)
    show(fig)

st.subheader("Pola penyewaan per jam")
# Data per jam mengikuti seluruh filter (tanggal, musim, cuaca) melalui tanggal pada data harian terfilter
hour_filtered = hour[hour.dteday.isin(filtered.dteday)].copy()
hour_filtered["day_type"] = hour_filtered["workingday"].map({1:"Hari kerja",0:"Akhir pekan/libur"})
hourly = hour_filtered.groupby(["hr","day_type"], as_index=False).cnt.mean()
fig = px.line(hourly, x="hr", y="cnt", color="day_type", markers=True, color_discrete_map=DAY_COLORS,
              labels={"hr":"Jam","cnt":"Rata-rata sewa/jam","day_type":"Tipe hari"})
fig.update_xaxes(dtick=2)
show(fig)

with st.expander("Lihat data harian terfilter"):
    try:
        st.dataframe(filtered, width="stretch")
    except TypeError:
        st.dataframe(filtered, use_container_width=True)
st.caption("Catatan: hubungan cuaca/musim dan penyewaan bersifat deskriptif, bukan bukti sebab-akibat.")
