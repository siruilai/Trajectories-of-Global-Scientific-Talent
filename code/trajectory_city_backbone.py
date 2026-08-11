import pandas as pd
import numpy as np

INPUT_PATH = "/mnt/network_data/personal_workspace/siruilai/orcid_work/02_output/trajectory_city_month_flows.csv"
OUTPUT_PATH = "/mnt/network_data/personal_workspace/siruilai/orcid_work/02_output/city_inflow_backbone_5year.csv"


# ----------------------------
# 1. 读取数据
# ----------------------------
df = pd.read_csv(INPUT_PATH)

# 去掉 self-loop（同城市）
df = df[df["from_city"] != df["to_city"]]


# ✅ 保留 city → country 映射
city_country_map_from = df[["from_city", "from_country"]].drop_duplicates()
city_country_map_to = df[["to_city", "to_country"]].drop_duplicates()


# ----------------------------
# 2. 定义时间窗口（按 year）
# ----------------------------
def assign_time_window(year):
    if 1980 <= year <= 1985:
        return "1980-1985"
    elif 1986 <= year <= 1990:
        return "1986-1990"
    elif 1991 <= year <= 1995:
        return "1991-1995"
    elif 1996 <= year <= 2000:
        return "1996-2000"
    elif 2001 <= year <= 2005:
        return "2001-2005"
    elif 2006 <= year <= 2010:
        return "2006-2010"
    elif 2011 <= year <= 2015:
        return "2011-2015"
    elif 2016 <= year <= 2020:
        return "2016-2020"
    elif 2021 <= year <= 2025:
        return "2021-2025"
    else:
        return None


df["time_window"] = df["year"].apply(assign_time_window)
df = df[df["time_window"].notna()]


# ----------------------------
# 3. 5年窗口聚合（保留country！）
# ----------------------------
agg_df = (
    df.groupby(
        ["time_window", "from_city", "to_city", "from_country", "to_country"],
        as_index=False
    )["traj_flow"].sum()
)


# ----------------------------
# 4. disparity filter（outflow）
# ----------------------------
def disparity_filter_inflow(group):   # inflow版本（按 to_city）
# def disparity_filter_outflow(group):    # outflow版本
    result = []

    for node, sub in group.groupby("to_city"):   # inflow
    # for node, sub in group.groupby("from_city"):  # outflow

        k = len(sub)
        s = sub["traj_flow"].sum()

        if k <= 1:
            continue

        for _, row in sub.iterrows():
            w = row["traj_flow"]
            p = w / s

            alpha = (1 - p) ** (k - 1)

            result.append({
                "time_window": row["time_window"],

                # ✅ city
                "from_city": row["from_city"],
                "to_city": row["to_city"],

                # ✅ country（新增保留）
                "from_country": row["from_country"],
                "to_country": row["to_country"],

                "weight": w,
                "degree": k,
                "strength": s,
                "p": p,
                "alpha": alpha
            })

    return pd.DataFrame(result)


# ----------------------------
# 5. 每个时间窗口运行
# ----------------------------
all_results = []

for tw, group in agg_df.groupby("time_window"):
    print(f"Processing {tw}...")

    res = disparity_filter_inflow(group)   # inflow
    # res = disparity_filter_outflow(group)    # outflow

    all_results.append(res)


result_df = pd.concat(all_results, ignore_index=True)


# ----------------------------
# 6. 标记显著边
# ----------------------------
result_df["significant"] = (result_df["alpha"] < 0.05).astype(int)


# ----------------------------
# 可选：过滤小流量（强烈建议 city）
# ----------------------------
# result_df = result_df[result_df["weight"] >= 3]


# ----------------------------
# 7. 保存
# ----------------------------
result_df.to_csv(OUTPUT_PATH, index=False)

print("✅ Finished! Saved to:", OUTPUT_PATH)