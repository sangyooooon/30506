from flask import Flask, render_template, request, jsonify
import pandas as pd
import openai
import os

app = Flask(__name__)

# 환경변수 또는 직접 입력
openai.api_key = os.getenv("OPENAI_API_KEY") or "your-api-key-here"

# 데이터 로딩
df = pd.read_csv("Delivery.csv")

@app.route("/")
def index():
    locations = df.to_dict(orient="records")
    return render_template("index.html", locations=locations)

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question", "")
    sample_data = df.head(50)
    prompt = "다음은 배송 위치 데이터입니다:\n" + \
             "\n".join(f"{row.Num}, {row.Latitude}, {row.Longitude}" for _, row in sample_data.iterrows()) + \
             f"\n\n질문: {user_question}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 배송 좌표 데이터를 분석하는 도우미입니다."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
