import streamlit as st
import pandas as pd
import openai
import folium
from streamlit_folium import st_folium
import os

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY") or "your-api-key-here"

# CSV 불러오기
df = pd.read_csv("Delivery.csv")

st.set_page_config(layout="wide")
st.title("📍 배송지 시각화 + GPT 분석")

# 지도 표시
m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=11)
for _, row in df.iterrows():
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=f"배송지 #{row['Num']}",
        icon=folium.Icon(color="blue")
    ).add_to(m)

st_folium(m, width=700, height=500)

# GPT 질문 입력
st.subheader("💬 GPT-4에게 배송 데이터를 질문해보세요")
question = st.text_area("질문을 입력하세요 (예: 배송지 분포가 특정 지역에 몰려 있나요?)")

if st.button("GPT에게 질문하기") and question:
    with st.spinner("GPT가 분석 중입니다..."):
        sample_data = df.head(50)
        prompt = "다음은 배송 위치 데이터입니다:\n" + \
                 "\n".join(f"{row.Num}, {row.Latitude}, {row.Longitude}" for _, row in sample_data.iterrows()) + \
                 f"\n\n질문: {question}"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "당신은 배송 좌표 데이터를 분석하는 도우미입니다."},
                    {"role": "user", "content": prompt}
                ]
            )
            answer = response.choices[0].message.content
            st.success("✅ GPT 응답:")
            st.markdown(answer)
        except Exception as e:
            st.error(f"❌ 오류 발생: {e}")
