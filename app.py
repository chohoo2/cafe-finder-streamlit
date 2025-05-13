import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta

# -------------------------------
# 1. Sample Data (수동 입력 or 추후 크롤링 연동 가능)
# -------------------------------
data = [
    {
        "카페명": "카페 루프",
        "주소": "서울 마포구 연남동",
        "업로드날짜": "2025-04-10",
        "해시태그": "#신상카페 #연남동카페",
        "링크": "https://instagram.com/p/abc123",
        "위도": 37.5665,
        "경도": 126.9780
    },
    {
        "카페명": "카페 브루잉",
        "주소": "부산 해운대구",
        "업로드날짜": "2025-03-15",
        "해시태그": "#오픈카페 #바다뷰",
        "링크": "https://instagram.com/p/def456",
        "위도": 35.1587,
        "경도": 129.1604
    },
]

# -------------------------------
# 2. 필터링
# -------------------------------
df = pd.DataFrame(data)
df["업로드날짜"] = pd.to_datetime(df["업로드날짜"])
recent_threshold = datetime.today() - timedelta(days=60)
df = df[df["업로드날짜"] >= recent_threshold]

# -------------------------------
# 3. Streamlit UI
# -------------------------------
st.set_page_config(layout="wide")
st.title("📍 신상 카페 리스트 (최근 2개월 기준)")

with st.expander("📋 데이터 테이블 보기"):
    st.dataframe(df[["카페명", "주소", "업로드날짜", "해시태그", "링크"]])

# -------------------------------
# 4. 지도 시각화
# -------------------------------
st.subheader("🗺 지도에서 보기")
m = folium.Map(location=[36.5, 127.5], zoom_start=6)

for _, row in df.iterrows():
    folium.Marker(
        location=[row["위도"], row["경도"]],
        popup=f"{row['카페명']}<br><a href='{row['링크']}' target='_blank'>인스타 링크</a>",
        tooltip=row["카페명"]
    ).add_to(m)

st_folium(m, width=1000, height=600)
