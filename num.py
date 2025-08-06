import streamlit as st
import pandas as pd
import os

CSV_FILE = "responses.csv"

# ---------------------
# 初期化（ファイルなければ作成）
# ---------------------
if not os.path.exists(CSV_FILE) or os.stat(CSV_FILE).st_size == 0:
    pd.DataFrame(columns=["value"]).to_csv(CSV_FILE, index=False)

# ---------------------
# アプリ本体
# ---------------------
st.title("📊 数値アンケート（リアルタイム集計）")

# ユーザー入力
with st.form("vote_form"):
    num = st.number_input("あなたの数値を入力してください（例：0～100）", min_value=0, max_value=1000, step=1)
    submitted = st.form_submit_button("送信する")

    if submitted:
        new = pd.DataFrame({"value": [num]})
        new.to_csv(CSV_FILE, mode="a", header=False, index=False)
        st.success("✅ 回答ありがとうございました！")

# データの読み込みと可視化
df = pd.read_csv(CSV_FILE)
if len(df) > 0:
    st.subheader("🔢 これまでの回答（件数: " + str(len(df)) + "）")
    st.bar_chart(df["value"])
else:
    st.info("まだ回答がありません。")

# ---------------------
# 管理者モード
# ---------------------
with st.expander("🛠 管理者メニュー（教員用）"):
    password = st.text_input("パスワードを入力してください", type="password")
    if password == "santi111":  # ←必要に応じて変更
        if st.button("🧹 データを初期化する"):
            pd.DataFrame(columns=["value"]).to_csv(CSV_FILE, index=False)
            st.success("データを初期化しました。")
    elif password != "":
        st.error("パスワードが違います。")

