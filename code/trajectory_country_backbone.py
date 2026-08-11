import pandas as pd
import numpy as np

INPUT_PATH = "/mnt/network_data/personal_workspace/siruilai/orcid_work/02_output/country_flow_year.csv"
OUTPUT_PATH = "/mnt/network_data/personal_workspace/siruilai/orcid_work/02_output/country_outflow_backbone_5year.csv"


# ----------------------------
# 1. 读取数据
# ----------------------------
df = pd.read_csv(INPUT_PATH)
# 去掉 self-loop
df = df[df["from_country"] != df["to_country"]]

# ----------------------------
# 2. 定义时间窗口
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

# 去掉不在范围内的
df = df[df["time_window"].notna()]

# ----------------------------
# 3. 5年窗口聚合
# ----------------------------
agg_df = (
    df.groupby(["time_window", "from_country", "to_country"], as_index=False)
    ["traj_count"].sum()
)

# ----------------------------
# 4. disparity filter（outflow）
# ----------------------------
# def disparity_filter_inflow(group):
def disparity_filter_outflow(group):
    result = []

    # for node, sub in group.groupby("to_country"):
    for node, sub in group.groupby("from_country"):

        k = len(sub)
        s = sub["traj_count"].sum()

        if k <= 1:
            continue

        for _, row in sub.iterrows():
            w = row["traj_count"]
            p = w / s

            # disparity filter
            alpha = (1 - p) ** (k - 1)

            result.append({
                "time_window": row["time_window"],
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
    # res = disparity_filter_inflow(group)
    res = disparity_filter_outflow(group)
    all_results.append(res)

result_df = pd.concat(all_results, ignore_index=True)

# ----------------------------
# 6. 标记显著边
# ----------------------------
result_df["significant"] = (result_df["alpha"] < 0.05).astype(int)

# ----------------------------
# 可选：去掉极小流量
# ----------------------------
# result_df = result_df[result_df["weight"] >= 5]

# ----------------------------
# 7. 保存
# ----------------------------
result_df.to_csv(OUTPUT_PATH, index=False)

print("Finished! Saved to:", OUTPUT_PATH)