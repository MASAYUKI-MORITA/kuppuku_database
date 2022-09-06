from datetime import datetime as dt, timedelta
import create
import datetime
import pandas as pd
import show
import streamlit as st

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# 変数
# 最初に作成されるデータフレーム
main_df = pd.DataFrame
# サークルのデータフレーム
circle_df = pd.DataFrame
# 声優のデータフレーム
va_df = pd.DataFrame
# タグのデータフレーム
tag_df = pd.DataFrame

# csvファイルパス
# 最初に作成されるデータフレーム
main_path = "DLsite音声作品データ.csv"
# サークルのデータフレーム
circle_path = "circles.csv"
# 声優のデータフレーム
va_path = "voice_actors.csv"
# タグのデータフレーム
tag_path = "tags.csv"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# streamlitのレイアウトを整える
st.set_page_config(layout="wide")

# ページ内容
# タイトル
st.title("DLsite音声作品データベース")

# サイドバー
# 作品タイトル入力フォーム
title_key = st.sidebar.text_input("作品名")

# サークル入力フォーム
# 検索時、サークルのデータフレームを表示
circle_key = st.sidebar.text_input("サークル名")
if circle_key:
    circle_df = create.createSidebarDf(pd.read_csv(circle_path), circle_key, "circle")
    if len(circle_df.index) > 0:
        st.sidebar.dataframe(circle_df, height=160)

# 声優入力フォーム
# 検索時、声優のデータフレームを表示
va_key = st.sidebar.text_input("声優名")
if va_key:
    va_df = create.createSidebarDf(pd.read_csv(va_path), va_key, "voice_actor")
    if len(va_df.index) > 0:
        st.sidebar.dataframe(va_df, height=160)

# タグ入力フォーム
# 検索時、タグのデータフレームを表示
tag_key = st.sidebar.text_input("タグ")
if tag_key:
    tag_df = create.createSidebarDf(pd.read_csv(tag_path), tag_key, "tag")
    if len(tag_df.index) > 0:
        st.sidebar.dataframe(tag_df, height=160)

# 公開日入力フォーム
# 2000年1月1日～今日
limited_flag = st.sidebar.checkbox("期間指定")
if limited_flag:
    sales_date_key_from = st.sidebar.date_input("公開日", datetime.date(2000, 1, 1), max_value=(datetime.date.today()))
    sales_date_key_to = st.sidebar.date_input("～")

# 価格入力フォーム
# 以上or以下or一致ラジオボタン
price_key = st.sidebar.number_input("価格", 0, step=1)
price_radio = st.sidebar.radio("", ("以上", "以下", "一致"), horizontal=True)

# ダウンロード数入力フォーム
# 以上or以下ラジオボタン
downloads_key = st.sidebar.number_input("ダウンロード数", 0, step=1)
downloads_radio = st.sidebar.radio("", ("以上", "以下"), horizontal=True)

# 並び順
# 価格or公開日orダウンロード数ラジオボタン
# 昇順or降順ラジオボタン
sort_key = st.sidebar.radio("並び順", ("価格", "公開日", "ダウンロード数"), 2, horizontal=True)
sort_dict = {"価格": "price", "公開日": "sales_date", "ダウンロード数": "downloads"}
desc_or_asc = st.sidebar.radio("降順or昇順", ("降順", "昇順"), horizontal=True)
da_dict = {"降順": False, "昇順": True}

# 検索ボタン
search_btn = st.sidebar.button("検索")

# 検索ボタン下に空白を用意（スマホだと検索ボタンが押しづらいため）
st.sidebar.title("")
st.sidebar.title("")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# 最初のデータフレームを生成
main_df = create.createMainDf(pd.read_csv(main_path))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# 検索実行
if search_btn:
    # 作品タイトル
    if title_key:
        main_df = main_df[main_df["title"].str.contains(title_key)]
    # タイトルの検索フォームに何かが入力されている場合、フラッグをTrueに
    title_flag = title_key != ""

    # サークル
    if circle_key:
        main_df = main_df[main_df["circle"].str.contains(circle_key)]
    # サークルの検索結果がユニークな場合、フラッグをTrueに
    circle_flag = circle_key and circle_df["circle"].str.contains(circle_key).sum() == 1

    # 声優
    if va_key:
        main_df = main_df[main_df["voice_actor"].str.contains(va_key)]
    # 声優の検索結果がユニークな場合、フラッグをTrueに
    va_flag = va_key and va_df["voice_actor"].str.contains(va_key).sum() == 1

    # タグ
    if tag_key:
        main_df = main_df[main_df["tag"].str.contains(tag_key)]
    # タグの検索結果がユニークな場合、フラッグをTrueに
    tag_flag = tag_key and tag_df["tag"].str.contains(tag_key).sum() == 1

    # 公開日
    if limited_flag:
        main_df = main_df[(main_df["sales_date"] >= sales_date_key_from) & (main_df["sales_date"] <= sales_date_key_to)]

    # 価格
    if price_radio == "以上":
        main_df = main_df[main_df["price"] >= price_key]
    elif price_radio == "以下":
        main_df = main_df[main_df["price"] <= price_key]
    else:
        main_df = main_df[main_df["price"] == price_key]

    # ダウンロード数
    if downloads_radio == "以上":
        main_df = main_df[main_df["downloads"] >= downloads_key]
    elif downloads_radio == "以下":
        main_df = main_df[main_df["downloads"] <= downloads_key]
    else:
        main_df = main_df[main_df["downloads"] == downloads_key]

    # 並び順
    main_df = main_df.sort_values(sort_dict[sort_key], ascending=da_dict[desc_or_asc])

    # 三種のフラグのいずれかがTrueな場合、「平均ダウンロード数と作品数の推移」を表示
    if title_flag or circle_flag or va_flag or tag_flag:
        # 「平均ダウンロード数と作品数の推移」を作成
        search_results_df = create.createSearchResultsDf(main_df)

        # 検索結果がユニークなものは、キーをデータフレームから参照
        if circle_flag:
            circle_key = circle_df[circle_df["circle"].str.contains(circle_key)].loc[:, "circle"].iloc[-1]
        if va_flag:
            va_key = va_df[va_df["voice_actor"].str.contains(va_key)].loc[:, "voice_actor"].iloc[-1]
        if tag_flag:
            tag_key = tag_df[tag_df["tag"].str.contains(tag_key)].loc[:, "tag"].iloc[-1]
        # グラフを表示
        # 引数に検索フォームの内容を設置
        show.showSearchResultsPlot(search_results_df, title=title_key, circle=circle_key, va=va_key, tag=tag_key)
        # データフレームを表示
        show.showDf("平均ダウンロード数と作品数の推移", search_results_df)

    # 検索結果をデータフレームで表示
    show.showDf("検索結果", main_df)
    # 検索結果の概観を表示
    show.showDescribe(main_df)

# 何も検索していない場合に表示される、初期のグラフとデータフレーム
else:
    # 作品公開日の期間を指定するスライダー
    period_slider = st.select_slider(
        "平均ダウンロード数 / n日",
        options=[30, 60, 90, 180, 365, 730, 1095]
    )

    # スライダーで指定された期間にデータフレームを絞る
    period = (datetime.datetime.now() - timedelta(days=period_slider)).date()
    main_df = main_df[main_df["sales_date"] >= period]
    # ダウンロード数順に並び替え
    main_df = main_df.sort_values("downloads", ascending=False)

    # 「声優別平均ダウンロード数TOP20」を作成
    top20 = create.createInitialDf(main_df, ps=period_slider)

    # グラフを表示（TOP20）
    show.showInitialPlot(top20, ps=period_slider)
    # データフレームを表示（TOP20）
    show.showDf(f"公開日: {period_slider} 日以内\n声優別平均ダウンロード数TOP20（出演頻度1作品/30日以上の方のみ抜粋）", top20)
    # グラフを表示（期間内に公開された全作品）
    show.showDf("期間内に公開された作品", main_df)
    # 概観を表示
    show.showDescribe(main_df)