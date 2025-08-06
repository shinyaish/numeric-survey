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
st.title("📊 数値アンケート（ヒストグラム集計）")

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
    st.subheader(f"🔢 これまでの回答（件数: {len(df)}）")

    # 各数値の出現回数をカウント＆昇順ソート
    count_series = df['value'].value_counts().sort_index()
    count_df = pd.DataFrame({'value': count_series.index, 'count': count_series.values}).set_index('value')

    st.bar_chart(count_df)
else:
    st.info("まだ回答がありません。")

# ---------------------
# 管理者モード
# ---------------------
with st.expander("🛠 管理者メニュー（教員用）"):
    password = st.text_input("パスワードを入力してください", type="password")
    if password == "santi111":
        if st.button("🧹 データを初期化する"):
            pd.DataFrame(columns=["value"]).to_csv(CSV_FILE, index=False)
            st.success("データを初期化しました。")
    elif password != "":
        st.error("パスワードが違います。")
