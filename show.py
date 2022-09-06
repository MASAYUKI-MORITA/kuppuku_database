from PIL import Image
import matplotlib.pyplot as plt
import japanize_matplotlib
import streamlit as st

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# データフレーム表示
def showDf(text, df):
    # サブヘッダーを表示
    st.subheader(text)
    # データフレームを表示
    st.dataframe(df)

# 概観表示
def showDescribe(df):
    # 概観を表示
    st.dataframe(df.describe())

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# グラフ表示
def showInitialPlot(df, ps=30):
    # 一つ目のグラフを作成
    fig, ax1 = plt.subplots(figsize=(16, 9))
    # 一つ目を棒グラフに設定
    # 「mean_downloads」カラムを反映
    ax1.vlines(df["id"], ymin=0, ymax=df["mean_downloads"], colors="red", alpha=0.4, linewidth=25)
    # 一つ目のy軸にラベルを表示
    ax1.set_ylabel("平\n均\nダ\nウ\nン\nロ\nー\nド\n数", labelpad=15, size=17, rotation=0, va="center", fontfamily="IPAexGothic")
    # y軸の最低値を0に固定
    ax1.set_ylim(ymin=0)
    # x軸に「index」を表示
    plt.xticks(df["id"], df.index, rotation=30, horizontalalignment="right", fontfamily="IPAexGothic")
    # グラフの位置を調整
    plt.subplots_adjust(left=0.1, bottom=0.2, right=0.9, top=0.9)
    # 二つ目のグラフを作成
    ax2 = ax1.twinx()
    # 二つ目を折れ線グラフに設定
    # 出演作品数「appearances」カラムを反映
    ax2.plot(df["id"], df["appearances"], linewidth=1, marker="o", color="blue", alpha=0.6)
    # 二つ目のy軸にラベルを表示
    ax2.set_ylabel("出\n演\n作\n品\n数", labelpad=15, size=20, rotation=0, va="center", fontfamily="IPAexGothic")
    # y軸の最低値を0に固定
    ax2.set_ylim(ymin=0)
    # グラフの左上にメインタイトルを表示
    plt.title("声優別平均ダウンロード数TOP20", loc="left", fontsize=30, fontfamily="IPAexGothic")
    # グラフの右上に指定した期間を表示
    plt.title(f"公開日: {ps} 日以内", loc="right", pad=10, fontsize=20, fontfamily="IPAexGothic")
    # x軸を左右反転
    ax2.invert_xaxis()
    # グリッドを非表示
    plt.grid(False)
    # x軸に余白を用意
    ax1.set_xmargin(0.02)
    # グラフを画像として保存
    plt.savefig("initial_plot.png")
    # 画像ファイル化したグラフを表示
    img = Image.open("initial_plot.png")
    st.image(img)

def showSearchResultsPlot(df, title="", circle="", va="", tag=""):
    # 一つ目のグラフを作成
    fig, ax1 = plt.subplots(figsize=(16, 9))
    # 一つ目を折れ線グラフに設定
    # 折れ線の下を塗りつぶし
    # 「mean_downloads」カラムを反映
    ax1.fill_between(df["id"], df["mean_downloads"], color="red", alpha=0.3)
    ax1.plot(df["id"], df["mean_downloads"], color="red", alpha=0.4)
    # 一つ目のy軸にラベルを表示
    ax1.set_ylabel("平\n均\nダ\nウ\nン\nロ\nー\nド\n数", labelpad=15, size=20, rotation=0, va="center", fontfamily="IPAexGothic")
    # y軸の最低値を0に固定
    ax1.set_ylim(ymin=0)
    # x軸に「index」を表示
    plt.xticks(df["id"], df["sales_date"], rotation=30, horizontalalignment="right", fontfamily="IPAexGothic")
    # グラフの位置を調整
    plt.subplots_adjust(left=0.1, bottom=0.2, right=0.9, top=0.9)
    # 二つ目のグラフを作成
    ax2 = ax1.twinx()
    # 二つ目を折れ線グラフに設定
    # 作品数「size」カラムを反映
    ax2.plot(df["id"], df["size"], linewidth=1, color="blue", alpha=0.6)
    # 二つ目のy軸にラベルを表示
    ax2.set_ylabel("作\n品\n数", labelpad=15, size=20, rotation=0, va="center", fontfamily="IPAexGothic")
    # y軸の最低値を0に固定
    ax2.set_ylim(ymin=0)
    # グラフの左上にメインタイトルを表示
    plt.title("平均ダウンロード数と作品数の推移", loc="left", pad=10, fontsize=30, fontfamily="IPAexGothic")
    # 12か月以上のデータがある場合、x軸の目盛り表示を減らす
    if len(df.index) > 12:
        for i, tick in enumerate(ax1.xaxis.get_ticklabels()):
            if i % (len(df.index) // 12) != 0:
                tick.set_visible(False)
    # グラフの下に検索内容を表示
    ax1.set_xlabel(f"作品タイトル:[ {title} ] サークル:[ {circle} ] 声優:[ {va} ] タグ:[ {tag} ]", labelpad=15, fontsize=20, fontfamily="IPAexGothic")
    # x軸を左右反転
    ax2.invert_xaxis()
    # グリッドを非表示
    plt.grid(False)
    # x軸に余白を用意
    ax1.set_xmargin(0.02)
    # グラフを画像として保存
    plt.savefig("search_results_plot.png")
    # 画像ファイル化したグラフを表示
    img = Image.open("search_results_plot.png")
    st.image(img)