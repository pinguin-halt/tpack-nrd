"""
================================================================================
RM1 ANALYSIS: Pre-Post Comparison, N-Gain, and Effect Sizes
================================================================================

Tujuan  : Menjawab RM1 — Bagaimana perubahan kemampuan integrasi TPACK, STEM,
          dan ESD dalam RPP sebelum dan sesudah penerapan PjBL?

Input   : dataset.csv (95 responden × 42 kolom, skala 1-4)
Output  : outputs/rm1/rm1_descriptive_constructs.csv   (Tabel 1)
          outputs/rm1/rm1_descriptive_indicators.csv   (Tabel 2)
          outputs/rm1/rm1_normality.csv                (Tabel 3)
          outputs/rm1/rm1_paired_tests.csv             (Tabel 4)
          outputs/rm1/rm1_ngain_summary.csv            (Tabel 5)
          outputs/rm1/rm1_ngain_individual.csv         (N-Gain per responden)
          outputs/rm1/fig1_pre_post_comparison.png     (Figur 1)
          outputs/rm1/fig2_ngain_distribution.png      (Figur 2)

Catatan : Skor maksimum = 4 (Likert 1-4).
          N-Gain = (post - pre) / (max - pre), max = 4, Hake (1998).
          Uji paired: t-test jika difference normal, Wilcoxon jika tidak.

Jalankan: conda run -n tpack-research python scripts/analysis/rm1_analysis.py
================================================================================
"""

import pandas as pd
import numpy as np
from scipy import stats
import pingouin as pg
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path


# ================================================================================
# KONFIGURASI
# ================================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "dataset.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "rm1"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MAX_SCORE = 4.0  # skor maksimum skala Likert
ALPHA = 0.05  # taraf signifikansi
NGAIN_HIGH = 0.7  # batas bawah kategori High  (Hake, 1998)
NGAIN_MEDIUM = 0.3  # batas bawah kategori Medium (Hake, 1998)

# Pemetaan konstruk -> kolom pre & post
CONSTRUCTS = {
    "TPACK": ("TPACK_total_pre", "TPACK_total_post"),
    "STEM": ("STEM_total_pre", "STEM_total_post"),
    "ESD": ("ESD_total_pre", "ESD_total_post"),
    "RPP Integratif": ("RPPInt_total_pre", "RPPInt_total_post"),
}

# Pemetaan indikator -> kolom pre & post
INDICATORS = {
    "TK": ("TK_pre", "TK_post"),
    "PK": ("PK_pre", "PK_post"),
    "CK": ("CK_pre", "CK_post"),
    "TPK": ("TPK_pre", "TPK_post"),
    "TCK": ("TCK_pre", "TCK_post"),
    "PCK": ("PCK_pre", "PCK_post"),
    "TPACK": ("TPACK_pre", "TPACK_post"),
    "S": ("S_pre", "S_post"),
    "T": ("T_pre", "T_post"),
    "E": ("E_pre", "E_post"),
    "M": ("M_pre", "M_post"),
    "ESD_PCK": ("ESD_PCK_pre", "ESD_PCK_post"),
    "ESD_INQ": ("ESD_INQ_pre", "ESD_INQ_post"),
    "ESD_EVA": ("ESD_EVA_pre", "ESD_EVA_post"),
}


# ================================================================================
# LOAD DATA
# ================================================================================

df = pd.read_csv(DATA_PATH)
print(f"Data loaded: {df.shape[0]} responden, {df.shape[1]} kolom")


def validate_required_columns(dataframe: pd.DataFrame) -> None:
    required = {"ID"}
    required.update([c for pair in CONSTRUCTS.values() for c in pair])
    required.update([c for pair in INDICATORS.values() for c in pair])
    missing = sorted(required - set(dataframe.columns))
    if missing:
        raise ValueError(f"Kolom wajib tidak ditemukan di dataset.csv: {missing}")


validate_required_columns(df)


# ================================================================================
# TABEL 1 — Descriptive Statistics per Construct (Pre vs Post)
# ================================================================================
# Menghitung mean, SD, min, max untuk setiap konstruk pada pretest dan posttest.
# Ini menjadi gambaran umum perubahan skor sebelum dan sesudah intervensi PjBL.

rows_t1 = []
for name, (pre_col, post_col) in CONSTRUCTS.items():
    valid = df[[pre_col, post_col]].dropna()
    pre = valid[pre_col]
    post = valid[post_col]
    rows_t1.append(
        {
            "Construct": name,
            "N": len(pre),
            "Pre_Mean": round(pre.mean(), 4),
            "Pre_SD": round(pre.std(), 4),
            "Pre_Min": round(pre.min(), 4),
            "Pre_Max": round(pre.max(), 4),
            "Post_Mean": round(post.mean(), 4),
            "Post_SD": round(post.std(), 4),
            "Post_Min": round(post.min(), 4),
            "Post_Max": round(post.max(), 4),
            "Mean_Diff": round(post.mean() - pre.mean(), 4),
        }
    )

tbl1 = pd.DataFrame(rows_t1)
tbl1.to_csv(OUTPUT_DIR / "rm1_descriptive_constructs.csv", index=False)

print("\n=== Tabel 1: Descriptive Statistics per Construct ===")
print(tbl1.to_string(index=False))


# ================================================================================
# TABEL 2 — Descriptive Statistics per Indicator (Pre vs Post)
# ================================================================================
# Menghitung statistik deskriptif untuk setiap indikator (sub-dimensi) secara
# terpisah: TK, PK, CK, ..., ESD_EVA. Berguna untuk melihat indikator mana
# yang paling banyak berubah.

rows_t2 = []
for name, (pre_col, post_col) in INDICATORS.items():
    valid = df[[pre_col, post_col]].dropna()
    pre = valid[pre_col]
    post = valid[post_col]
    rows_t2.append(
        {
            "Indicator": name,
            "Pre_Mean": round(pre.mean(), 4),
            "Pre_SD": round(pre.std(), 4),
            "Post_Mean": round(post.mean(), 4),
            "Post_SD": round(post.std(), 4),
            "Mean_Diff": round(post.mean() - pre.mean(), 4),
        }
    )

tbl2 = pd.DataFrame(rows_t2)
tbl2.to_csv(OUTPUT_DIR / "rm1_descriptive_indicators.csv", index=False)

print("\n=== Tabel 2: Descriptive Statistics per Indicator ===")
print(tbl2.to_string(index=False))


# ================================================================================
# TABEL 3 — Shapiro-Wilk Normality Tests
# ================================================================================
# Menguji normalitas skor pre, post, dan selisih (difference) menggunakan
# Shapiro-Wilk (N < 100). Keputusan uji paired bergantung pada normalitas
# difference scores:
#   - Normal     -> paired t-test
#   - Tidak normal -> Wilcoxon signed-rank test

rows_t3 = []
diff_is_normal = {}

for name, (pre_col, post_col) in CONSTRUCTS.items():
    valid = df[[pre_col, post_col]].dropna()
    diff = valid[post_col] - valid[pre_col]
    sw_pre = stats.shapiro(valid[pre_col])
    sw_post = stats.shapiro(valid[post_col])
    sw_diff = stats.shapiro(diff)

    normal = sw_diff.pvalue > ALPHA
    diff_is_normal[name] = normal

    rows_t3.append(
        {
            "Construct": name,
            "SW_Pre_stat": round(sw_pre.statistic, 4),
            "SW_Pre_p": round(sw_pre.pvalue, 4),
            "Pre_Normal": "Yes" if sw_pre.pvalue > ALPHA else "No",
            "SW_Post_stat": round(sw_post.statistic, 4),
            "SW_Post_p": round(sw_post.pvalue, 4),
            "Post_Normal": "Yes" if sw_post.pvalue > ALPHA else "No",
            "SW_Diff_stat": round(sw_diff.statistic, 4),
            "SW_Diff_p": round(sw_diff.pvalue, 4),
            "Diff_Normal": "Yes" if normal else "No",
        }
    )

tbl3 = pd.DataFrame(rows_t3)
tbl3.to_csv(OUTPUT_DIR / "rm1_normality.csv", index=False)

print("\n=== Tabel 3: Shapiro-Wilk Normality Tests ===")
print(tbl3.to_string(index=False))

print("\nKeputusan uji:")
for name, normal in diff_is_normal.items():
    test = "Paired t-test" if normal else "Wilcoxon signed-rank"
    print(f"  {name}: {test}")


# ================================================================================
# TABEL 4 — Paired Tests + Effect Size
# ================================================================================
# Melakukan uji beda berpasangan (pre vs post) untuk setiap konstruk.
# - Paired t-test jika difference scores normal.
# - Wilcoxon signed-rank jika tidak normal.
# Effect size: Cohen's d = mean_diff / SD_diff (interpretasi Cohen, 1988).
# CI 95% dilaporkan untuk t-test.


def interpret_cohens_d(d: float) -> str:
    """Klasifikasi effect size menurut Cohen (1988)."""
    if pd.isna(d):
        return "NA"
    d = abs(d)
    if d < 0.20:
        return "Negligible"
    if d < 0.50:
        return "Small"
    if d < 0.80:
        return "Medium"
    return "Large"


def cohens_d_paired(diff: pd.Series) -> float:
    sd = diff.std(ddof=1)
    if pd.isna(sd) or sd <= 1e-12:
        return np.nan
    return float(diff.mean() / sd)


rows_t4 = []
for name, (pre_col, post_col) in CONSTRUCTS.items():
    valid = df[[pre_col, post_col]].dropna()
    pre = valid[pre_col]
    post = valid[post_col]
    diff = post - pre
    n = len(pre)
    rbc = np.nan

    # Cohen's d selalu dihitung untuk komparabilitas antar konstruk
    cohens_d = cohens_d_paired(diff)

    if diff_is_normal[name]:
        # --- Paired t-test (pingouin) ---
        res = pg.ttest(post, pre, paired=True)
        stat_label = "t"
        stat_val = round(res["T"].values[0], 4)
        p_val = res["p-val"].values[0]
        ci = res["CI95%"].values[0]
        ci_str = f"[{ci[0]:.4f}, {ci[1]:.4f}]"
        test_name = "Paired t-test"
    else:
        # --- Wilcoxon signed-rank test (pingouin) ---
        res = pg.wilcoxon(post, pre, alternative="two-sided")
        stat_label = "W"
        stat_val = round(res["W-val"].values[0], 4)
        p_val = res["p-val"].values[0]
        ci_str = "N/A"
        test_name = "Wilcoxon"
        rbc = (
            float(res["RBC"].values[0])
            if "RBC" in res.columns and pd.notna(res["RBC"].values[0])
            else np.nan
        )

    p_str = f"{p_val:.6f}" if p_val >= 1e-6 else "<0.000001"

    rows_t4.append(
        {
            "Construct": name,
            "Test": test_name,
            "N": n,
            "Mean_Pre": round(pre.mean(), 4),
            "Mean_Post": round(post.mean(), 4),
            "Mean_Diff": round(diff.mean(), 4),
            "Statistic_Label": stat_label,
            "Statistic": stat_val,
            "p_value": p_str,
            "Significant": "Yes" if p_val < ALPHA else "No",
            "Cohens_d": round(cohens_d, 4),
            "Effect_Size_Interp": interpret_cohens_d(cohens_d),
            "Wilcoxon_RBC": round(rbc, 4) if test_name == "Wilcoxon" else np.nan,
            "CI_95": ci_str,
        }
    )

tbl4 = pd.DataFrame(rows_t4)
tbl4.to_csv(OUTPUT_DIR / "rm1_paired_tests.csv", index=False)

print("\n=== Tabel 4: Paired Tests Results ===")
for _, r in tbl4.iterrows():
    print(f"\n{r['Construct']}:")
    print(f"  Test: {r['Test']}")
    print(f"  Pre: {r['Mean_Pre']} -> Post: {r['Mean_Post']} (Diff: {r['Mean_Diff']})")
    print(
        f"  {r['Statistic_Label']} = {r['Statistic']}, p = {r['p_value']}, Sig: {r['Significant']}"
    )
    print(f"  Cohen's d = {r['Cohens_d']} ({r['Effect_Size_Interp']})")
    print(f"  95% CI: {r['CI_95']}")


# ================================================================================
# TABEL 5 — N-Gain per Construct + Kategori Hake (1998)
# ================================================================================
# N-Gain = (post - pre) / (max - pre), max = 4.
# Kategori Hake (1998):
#   High   : g >= 0.7
#   Medium : 0.3 <= g < 0.7
#   Low    : g < 0.3
#
# Dihitung per responden, lalu dirangkum per konstruk (mean, SD, distribusi).


def hake_category(g: float) -> str:
    """Klasifikasi N-Gain menurut Hake (1998)."""
    if g >= NGAIN_HIGH:
        return "High"
    if g >= NGAIN_MEDIUM:
        return "Medium"
    return "Low"


# Hitung N-Gain per responden per konstruk
ngain_df = pd.DataFrame({"ID": df["ID"]})

for name, (pre_col, post_col) in CONSTRUCTS.items():
    pre = df[pre_col]
    post = df[post_col]
    denom = MAX_SCORE - pre
    ngain = np.where(denom > 0, (post - pre) / denom, np.nan)
    ngain = np.where(pd.notna(pre) & pd.notna(post), ngain, np.nan)
    ngain_df[f"NGain_{name}"] = ngain

ngain_df.to_csv(OUTPUT_DIR / "rm1_ngain_individual.csv", index=False)

for name in CONSTRUCTS:
    vals = ngain_df[f"NGain_{name}"].dropna()
    outside = int(((vals < 0) | (vals > 1)).sum())
    if outside > 0:
        print(
            f"Peringatan: {outside} nilai N-Gain di luar rentang [0, 1] pada konstruk {name}."
        )

# Rangkuman per konstruk
rows_t5 = []
for name in CONSTRUCTS:
    pre_col, _ = CONSTRUCTS[name]
    col = f"NGain_{name}"
    vals = ngain_df[col].dropna()
    cats = vals.apply(hake_category)
    n_high = (cats == "High").sum()
    n_med = (cats == "Medium").sum()
    n_low = (cats == "Low").sum()
    n_total = len(vals)
    n_premax = int((df[pre_col] >= MAX_SCORE).sum())

    rows_t5.append(
        {
            "Construct": name,
            "N": n_total,
            "N_Excluded_PreMax": n_premax,
            "NGain_Mean": round(vals.mean(), 4),
            "NGain_SD": round(vals.std(), 4),
            "NGain_Min": round(vals.min(), 4),
            "NGain_Max": round(vals.max(), 4),
            "Category": hake_category(vals.mean()),
            "n_High": n_high,
            "pct_High": round(n_high / n_total * 100, 1),
            "n_Medium": n_med,
            "pct_Medium": round(n_med / n_total * 100, 1),
            "n_Low": n_low,
            "pct_Low": round(n_low / n_total * 100, 1),
        }
    )

tbl5 = pd.DataFrame(rows_t5)
tbl5.to_csv(OUTPUT_DIR / "rm1_ngain_summary.csv", index=False)

print("\n=== Tabel 5: N-Gain Summary ===")
print(tbl5.to_string(index=False))


# ================================================================================
# FIGUR 1 — Bar Chart Pre-test vs Post-test per Construct
# ================================================================================
# Grouped bar chart membandingkan mean skor pre dan post untuk keempat konstruk.
# Error bar = 1 SD.

construct_names = list(CONSTRUCTS.keys())
pre_means = [df[CONSTRUCTS[c][0]].mean() for c in construct_names]
post_means = [df[CONSTRUCTS[c][1]].mean() for c in construct_names]
pre_sds = [df[CONSTRUCTS[c][0]].std() for c in construct_names]
post_sds = [df[CONSTRUCTS[c][1]].std() for c in construct_names]

x = np.arange(len(construct_names))
width = 0.35

fig1, ax1 = plt.subplots(figsize=(8, 5))

bars_pre = ax1.bar(
    x - width / 2,
    pre_means,
    width,
    yerr=pre_sds,
    label="Pre-test",
    color="#56B4E9",  # Okabe-Ito Sky Blue (Pre-test)
    edgecolor="white",
    capsize=4,
    alpha=0.9,
)
bars_post = ax1.bar(
    x + width / 2,
    post_means,
    width,
    yerr=post_sds,
    label="Post-test",
    color="#0072B2",  # Okabe-Ito Blue (Post-test)
    edgecolor="white",
    capsize=4,
    alpha=0.9,
)

ax1.set_ylabel("Mean Score (1–4 Scale)", fontsize=11)
ax1.set_title(
    "Pre-test vs Post-test Mean Scores by Construct", fontsize=13, fontweight="bold"
)
ax1.set_xticks(x)
ax1.set_xticklabels(construct_names, fontsize=10)
ax1.set_ylim(0, 4.5)
ax1.legend(fontsize=10)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

for bar in bars_pre:
    h = bar.get_height()
    ax1.annotate(
        f"{h:.2f}",
        xy=(bar.get_x() + bar.get_width() / 2, h),
        xytext=(0, 3),
        textcoords="offset points",
        ha="center",
        fontsize=8,
    )
for bar in bars_post:
    h = bar.get_height()
    ax1.annotate(
        f"{h:.2f}",
        xy=(bar.get_x() + bar.get_width() / 2, h),
        xytext=(0, 3),
        textcoords="offset points",
        ha="center",
        fontsize=8,
    )

fig1.tight_layout()
fig1.savefig(OUTPUT_DIR / "fig1_pre_post_comparison.png", dpi=300, bbox_inches="tight")
plt.close(fig1)
print(f"\nFigur 1 saved: {OUTPUT_DIR / 'fig1_pre_post_comparison.png'}")


# ================================================================================
# FIGUR 2 — Stacked Bar Chart Distribusi Kategori N-Gain
# ================================================================================
# Menampilkan proporsi (%) responden di kategori High, Medium, Low untuk setiap
# konstruk. Memudahkan pembaca melihat pola diferensial antar konstruk.

fig2, ax2 = plt.subplots(figsize=(8, 5))

categories = ["High", "Medium", "Low"]
colors = [
    "#009E73",
    "#E69F00",
    "#D55E00",
]  # Okabe-Ito: Green (High), Orange (Medium), Vermillion (Low)
bottom = np.zeros(len(construct_names))

for cat, color in zip(categories, colors):
    pcts = tbl5[f"pct_{cat}"].values
    ax2.bar(
        construct_names,
        pcts,
        bottom=bottom,
        label=cat,
        color=color,
        edgecolor="white",
        alpha=0.9,
    )
    for i, (p, b) in enumerate(zip(pcts, bottom)):
        if p > 5:
            ax2.text(
                i,
                b + p / 2,
                f"{p:.1f}%",
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
                color="white",
            )
    bottom += pcts

ax2.set_ylabel("Percentage of Students (%)", fontsize=11)
ax2.set_title(
    "N-Gain Category Distribution by Construct", fontsize=13, fontweight="bold"
)
ax2.legend(title="N-Gain Category", fontsize=10, loc="upper right")
ax2.set_ylim(0, 110)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

fig2.tight_layout()
fig2.savefig(OUTPUT_DIR / "fig2_ngain_distribution.png", dpi=300, bbox_inches="tight")
plt.close(fig2)
print(f"Figur 2 saved: {OUTPUT_DIR / 'fig2_ngain_distribution.png'}")


# ================================================================================
# SELESAI
# ================================================================================
print("\n" + "=" * 60)
print(f"RM1 analysis complete. Semua output tersimpan di {OUTPUT_DIR}")
print("=" * 60)
