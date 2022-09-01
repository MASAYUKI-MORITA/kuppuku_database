from datetime import datetime as dt, timedelta
import pandas as pd
import streamlit as st
import datetime

# 声優ランキング表示の有無を決定するフラッグ
flag_dict = {"period": True, "search": False}
flag = flag_dict["period"]

st.set_page_config(layout="wide")
st.title("DLsite音声作品データベース")

# チャート表示
# def show_plot(df):

# データフレーム表示
def show_df(text, df):
    st.subheader(text)
    st.dataframe(df)

# 概観表示
def show_describe(df):
    st.write(df.describe(datetime_is_numeric=True))

# csvファイル読み込み
file_path = "DLsite音声作品データ.csv"
df = pd.read_csv(file_path)

# データフレームを変形
df = df.reindex(
    ["title", "circle", "voice_actor", "tag", "sales_date", "price", "downloads"],
    axis=1
)
df = df.fillna({"voice_actor": "不明", "tag": "なし", "sales_date": "2000-01-01", "downloads": 0})
df["sales_date"] = pd.to_datetime(df["sales_date"]).dt.date
df["price"] = df["price"].astype("int")
df["downloads"] = df["downloads"].str.replace("^<li[\s\S]*", "0", regex=True)
df["downloads"] = df["downloads"].astype("int")

# 作品検索
title_key = st.sidebar.text_input("作品名")

# サークル検索
circle_key = st.sidebar.text_input("サークル名")
circle_file_path = "circles.csv"
circle_df = pd.read_csv(circle_file_path)
if circle_key:
    st.sidebar.dataframe(
        circle_df[circle_df["circle"].astype(str).str.contains(circle_key, case=False)],
        height=160
    )

# 声優検索
va_key = st.sidebar.text_input("声優名")
va_file_path = "voice_actors.csv"
va_df = pd.read_csv(va_file_path)
if va_key:
    st.sidebar.dataframe(
        va_df[va_df["voice_actor"].astype(str).str.contains(va_key, case=False)],
        height=160
    )

# タグ検索
tag_key = st.sidebar.text_input("タグ")
tag_file_path = "tags.csv"
tag_df = pd.read_csv(tag_file_path)
if tag_key:
    st.sidebar.dataframe(
        tag_df[tag_df["tag"].astype(str).str.contains(tag_key, case=False)],
        height=160
    )

# 公開日
sales_date_key_from = st.sidebar.date_input("公開日", datetime.date(2000, 1, 1))
sales_date_key_to = st.sidebar.date_input("～")

# 価格検索
price_key = st.sidebar.number_input("価格", 0, step=1)
price_radio = st.sidebar.radio("", ("以上", "以下", "一致"), horizontal=True)

# ダウンロード数検索
downloads_key = st.sidebar.number_input("ダウンロード数", 0, step=1)
downloads_radio = st.sidebar.radio("", ("以上", "以下"), horizontal=True)

# 並び順
sort_key = st.sidebar.radio("並び順", ("価格", "公開日", "ダウンロード数"), 2, horizontal=True)
sort_dict = {"価格": "price", "公開日": "sales_date", "ダウンロード数": "downloads"}
desc_or_asc = st.sidebar.radio("降順or昇順", ("降順", "昇順"), horizontal=True)
da_dict = {"降順": False, "昇順": True}

# 検索ボタン
if st.sidebar.button("検索"):
    if title_key:
        df = df[df["title"].str.contains(title_key)]

    if circle_key:
        df = df[df["circle"].str.contains(circle_key)]

    if va_key:
        df = df[df["voice_actor"].str.contains(va_key)]

    if tag_key:
        df = df[df["tag"].str.contains(tag_key)]

    df = df[(df["sales_date"] >= sales_date_key_from) & (df["sales_date"] <= sales_date_key_to)]

    if price_radio == "以上":
        df = df[df["price"] >= price_key]
    elif price_radio == "以下":
        df = df[df["price"] <= price_key]
    else:
        df = df[df["price"] == price_key]

    if downloads_radio == "以上":
        df = df[df["downloads"] >= downloads_key]
    elif downloads_radio == "以下":
        df = df[df["downloads"] <= downloads_key]
    else:
        df = df[df["downloads"] == downloads_key]

    df = df.sort_values(sort_dict[sort_key], ascending=da_dict[desc_or_asc])

    show_df("検索結果:", df)
    show_describe(df)

    flag = flag_dict["search"]

# 期間
if flag:
    period_slider = st.select_slider(
        "Select a period of sales_date",
        options=[30, 60, 90, 180, 365, 730, 1095]
    )

    # デフォルトの表示内容
    def_df = df.sort_values("sales_date", ascending=False)
    period = (datetime.datetime.now() - timedelta(days=period_slider)).date()
    def_df = def_df[def_df["sales_date"] >= period]
    def_df = def_df.sort_values("downloads", ascending=False)

    top10 = def_df.groupby(["voice_actor"]).mean()
    top10["size"] = def_df.groupby(["voice_actor"]).size()
    top10["total"] = def_df.groupby(["voice_actor"])["downloads"].sum()
    top10 = top10[top10["size"] >= period_slider // 30]
    top10 = top10.sort_values("downloads", ascending=False)
    top10 = top10.iloc[:10, :]
    top10 = top10.sort_values("downloads", ascending=True)
    top10["id"] = pd.RangeIndex(start=1, stop=len(top10.index) + 1, step=1)
    top10 = top10.reindex(
        ["id", "price", "downloads", "size", "total"],
        axis=1
    )

    # show_plot(top10)
    show_df(f"公開日:{period_slider:>4d}日以内\n声優別\"平均\"ダウンロード数（30日につき1作品以上の出演がある方のみ）", top10)

    show_df(f"公開日:{period_slider:>4d}日以内", def_df)
    show_describe(def_df)