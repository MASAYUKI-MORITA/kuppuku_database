import pandas as pd

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# 最初に作成されるデータフレームを生成
def createMainDf(df):
    # データフレームを編集する前にコピー
    result = df.copy()
    # カラムを並び替え
    result = result.reindex(
        ["title", "circle", "voice_actor", "tag", "sales_date", "price", "downloads"],
        axis=1
    )
    # 欠損値セルを埋める
    result = result.fillna({"voice_actor": "不明", "tag": "なし", "sales_date": "2000-01-01", "downloads": 0})
    # 「sales_date」カラムを「date型」に変換
    result["sales_date"] = pd.to_datetime(result["sales_date"]).dt.date
    # 「price」カラムを「int型」に変換
    result["price"] = result["price"].astype("int")
    # 「downloads」カラムのセルに謎の「<li...」が入ることがあるので、該当セルの値を「0」にする
    result["downloads"] = result["downloads"].str.replace("^<li[\s\S]*", "0", regex=True)
    # 「downloads」カラムを「int型」に変換
    result["downloads"] = result["downloads"].astype("int")

    return result

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# サイドバーのデータフレームを作成
# （サークルor声優orタグ）
def createSidebarDf(df, key, column):
    # データフレームを編集する前にコピー
    result = df.copy()
    # フォームに入力された内容が含まれているセルを検索
    result = result[result[column].astype(str).str.contains(key, case=False)]

    return result

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# グラフ表示用のデータフレームを作成
# 初期
# 作成するデータフレームは「声優別平均ダウンロード数TOP20」
def createInitialDf(df, ps=30):
    # データフレームを編集する前にコピー
    result = df.copy()
    # データフレームをグループ化する前にコピー
    alt_df = result.copy()
    # 「voice_actor」基準でグループ化
    result = result.groupby(["voice_actor"]).mean()
    # 「downloads」カラムを「mean_downloads」（平均ダウンロード数）カラムに名称変更
    result = pd.DataFrame(result)
    result = result.rename(columns={"downloads": "mean_downloads"})
    # 「price」カラムを「mean_price」（平均価格）カラムに名称変更
    result = result.rename(columns={"price": "mean_price"})
    # 「voice_actor」ごとに出演作品数を「appearances」カラムに格納
    result["appearances"] = alt_df.groupby(["voice_actor"]).size()
    # 「voice_actor」ごとに「downloads」の合計を「total」カラムに格納
    result["total"] = alt_df.groupby(["voice_actor"])["downloads"].sum()
    # 「appearances」が「30日につき1本以上」な声優のみに絞る
    result = result[result["appearances"] >= ps // 30]
    # 「mean_downloads」を基準に降順に並び替え
    result = result.sort_values("mean_downloads", ascending=False)
    # 「mean_downloads」を基準に上位20位のみに絞る
    if len(result) > 20:
        result = result.iloc[:20, :]
    # 「total」を基準に降順へ並び替え
    result = result.sort_values("total", ascending=False)
    # 「sales_date」をカラムに戻すため、indexを新規作成
    result.reset_index(inplace=True)
    # 「index」としてカラムに戻った「voice_actor」のカラム名を元に戻す
    result = result.rename(columns={"index": "voice_actor"})
    # カラムを並び替え
    result = result.reindex(
        ["voice_actor", "mean_price", "mean_downloads", "appearances", "total"],
        axis=1
    )

    return result

# 検索時
# 作成するデータフレームは「月ごとの平均ダウンロード数および作品公開数の推移」
def createSearchResultsDf(df):
    # データフレームを編集する前にコピー
    alt_df = df.copy()
    # 「sales_date」カラムを「datetime型」に変換
    alt_df["sales_date"] = pd.to_datetime(alt_df["sales_date"])
    # 「sales_date」カラムをindexに配置
    alt_df.set_index("sales_date", inplace=True)
    # 「sales_date」を基準に、月ごとのデータを戻り値のデータフレームに格納
    result = pd.DataFrame({
        # 平均ダウンロード数
        "downloads": alt_df["downloads"].resample("M").mean(),
        # 作品数
        "size": alt_df["downloads"].resample("M").count(),
        # 累計ダウンロード数
        "total": alt_df["downloads"].resample("M").sum()
    })
    # 「downloads」カラムを「mean_downloads」（平均ダウンロード数）カラムに名称変更
    result = pd.DataFrame(result).rename(columns={"downloads": "mean_downloads"})
    # 「sales_date」をカラムに戻すため、「index」を振り直し
    result.reset_index(inplace=True)
    # 「index」としてカラムに戻った「sales_date」のカラム名を元に戻す
    result = pd.DataFrame(result).rename(columns={"index": "sales_date"})
    # 「sales_date」カラムを「datetime型」に変換し、「YYYY-mm」形式で表示
    result["sales_date"] = pd.to_datetime(result["sales_date"]).dt.strftime("%Y-%m")
    # 「sales_date」を基準に降順に並び替え
    result = result.sort_values("sales_date", ascending=False)
    # 空のセルに「0」を埋める
    result = result.fillna(0)
    # カラムを並び替え
    result = result.reindex(
        ["sales_date", "mean_downloads", "size", "total"],
        axis=1
    )
    # 「index」を振り直し
    result = result.reset_index(drop=True)

    return result