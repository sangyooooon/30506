import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="당뇨병 데이터 시각화", layout="wide")

# 데이터 불러오기 함수
@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?export=download&id=1pwfON6doXyH5p7AOBJPfiofYlni0HVVY"
    df = pd.read_csv(url)
    return df

# 앱 제목
st.title("🩺 당뇨병 진단 데이터 시각화 웹앱")

# 데이터 로딩
df = load_data()

# 데이터 정보 출력
st.subheader("📊 데이터 미리보기")
st.dataframe(df)

# 시각화 섹션
st.subheader("📈 Plotly를 이용한 데이터 시각화")

# 컬럼 선택
cols = df.columns.tolist()
col1, col2, col3 = st.columns(3)
with col1:
    x_axis = st.selectbox("X축 선택", cols)
with col2:
    y_axis = st.selectbox("Y축 선택", cols)
with col3:
    color_by = st.selectbox("색상 기준 (선택)", ["None"] + cols)

# 그래프 생성
if color_by != "None":
    fig = px.scatter(df, x=x_axis, y=y_axis, color=df[color_by], title="산점도 시각화")
else:
    fig = px.scatter(df, x=x_axis, y=y_axis, title="산점도 시각화")

# 출력
st.plotly_chart(fig, use_container_width=True)

# 앱 정보
st.markdown("""
---
✅ 데이터 출처: Google Drive  
✅ 기술 스택: Streamlit + Plotly + Pandas  
""")


