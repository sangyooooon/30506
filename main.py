import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기 함수
@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?export=download&id=1pwfON6doXyH5p7AOBJPfiofYlni0HVVY"
    df = pd.read_csv(url)
    return df

# 앱 제목
st.title("당뇨병 진단 데이터 시각화 웹앱")

# 데이터 로드
df = load_data()

# 데이터 미리보기
st.subheader("데이터 미리보기")
st.dataframe(df)

# 시각화 선택
st.subheader("Plotly 시각화")

x_axis = st.selectbox("X축 선택", df.columns)
y_axis = st.selectbox("Y축 선택", df.columns)
color_by = st.selectbox("색상 그룹화 기준 (선택)", ["None"] + list(df.columns))

# 산점도 그래프
if color_by != "None":
    fig = px.scatter(df, x=x_axis, y=y_axis, color=df[color_by])
else:
    fig = px.scatter(df, x=x_axis, y=y_axis)

st.plotly_chart(fig)

