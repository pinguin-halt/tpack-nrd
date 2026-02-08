"""RM2-RM5: PLS-SEM Analysis with Single Unified Bootstrap.

Strategi performa:
- plspm built-in bootstrap dimatikan (bootstrap=False).
- Satu loop manual bootstrap (N_BOOTSTRAP iterasi) dijalankan sekali.
  Dari setiap resample, kita kumpulkan:
    (a) path coefficients  -> untuk t-stat dan CI jalur langsung
    (b) indirect effects   -> untuk CI mediasi (RM5)
- Sobel test ditambahkan sebagai cross-check mediasi.

Target waktu eksekusi: menyesuaikan jumlah bootstrap (default 5000 iterasi).
"""

from __future__ import annotations

import time
import warnings
from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from plspm.config import Config, MV, Structure
from plspm.mode import Mode
from plspm.plspm import Plspm
from scipy.stats import norm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold

try:
    from tqdm.auto import tqdm
except Exception:  # fallback jika tqdm belum terpasang
    tqdm = None

# ========================
# KONFIGURASI GLOBAL
# ========================
warnings.filterwarnings("ignore", category=RuntimeWarning)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "dataset.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "rm2_rm5"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

N_BOOTSTRAP = 5000  # Rekomendasi pelaporan final mediasi/path SEM-PLS
RANDOM_SEED = 42

# ========================
# DEFINISI KONSTRUK & INDIKATOR
# ========================
BLOCKS: dict[str, list[str]] = {
    # PjBL05 dihapus karena variansi nol (konstan)
    "PjBL": ["PjBL01", "PjBL02", "PjBL03", "PjBL04"],
    "TPACK": [
        "TK_post",
        "PK_post",
        "CK_post",
        "TPK_post",
        "TCK_post",
        "PCK_post",
        "TPACK_post",
    ],
    "STEM": ["S_post", "T_post", "E_post", "M_post"],
    "ESD": ["ESD_PCK_post", "ESD_INQ_post", "ESD_EVA_post"],
    # Outcome kualitas RPP integratif (single-indicator construct)
    "RPP": ["RPPInt_total_post"],
}

STRUCTURAL_EDGES: list[tuple[str, str]] = [
    ("PjBL", "TPACK"),
    ("PjBL", "STEM"),
    ("PjBL", "ESD"),
    ("PjBL", "RPP"),
    ("TPACK", "RPP"),
    ("STEM", "RPP"),
    ("ESD", "RPP"),
]

ENDOGENOUS = ["TPACK", "STEM", "ESD", "RPP"]
MEDIATORS = ["TPACK", "STEM", "ESD"]


# ========================
# FUNGSI BANTU: MODEL PLS
# ========================
def build_structure(edges: list[tuple[str, str]]) -> pd.DataFrame:
    structure = Structure()
    grouped: dict[str, list[str]] = {}
    for src, tgt in edges:
        grouped.setdefault(src, []).append(tgt)
    for src, tgts in grouped.items():
        structure.add_path([src], tgts)
    return structure.path()


def build_config(path_matrix: pd.DataFrame) -> Config:
    config = Config(path_matrix)
    for lv, indicators in BLOCKS.items():
        config.add_lv(lv, Mode.A, *[MV(col) for col in indicators])
    return config


def fit_pls(
    data: pd.DataFrame,
    edges: list[tuple[str, str]],
    bootstrap: bool = False,
    bootstrap_iterations: int = 100,
) -> Plspm:
    path_matrix = build_structure(edges)
    config = build_config(path_matrix)
    return Plspm(
        data,
        config,
        bootstrap=bootstrap,
        bootstrap_iterations=bootstrap_iterations,
        processes=1,
    )


def path_matrix_to_long(path_df: pd.DataFrame) -> pd.DataFrame:
    """Konversi path coefficient matrix ke long format."""
    rows: list[dict[str, float | str]] = []
    for target in path_df.index:
        for source in path_df.columns:
            coef = float(path_df.loc[target, source])
            if coef != 0:
                rows.append(
                    {
                        "Path": f"{source} -> {target}",
                        "Source": source,
                        "Target": target,
                        "Beta": coef,
                    }
                )
    return pd.DataFrame(rows)


def build_loading_table(outer_model: pd.DataFrame) -> pd.DataFrame:
    indicator_to_construct = {
        indicator: construct
        for construct, indicators in BLOCKS.items()
        for indicator in indicators
    }
    out = outer_model.copy().reset_index().rename(columns={"index": "Indicator"})
    out["Construct"] = out["Indicator"].map(indicator_to_construct)
    out = out[
        [
            "Construct",
            "Indicator",
            "loading",
            "weight",
            "communality",
            "redundancy",
        ]
    ]
    out = out.rename(
        columns={
            "loading": "Loading",
            "weight": "Weight",
            "communality": "Communality",
            "redundancy": "Redundancy",
        }
    )
    return out.sort_values(["Construct", "Indicator"]).reset_index(drop=True)


# ========================
# DISKRIMINANT: HTMT & FORNELL-LARCKER
# ========================
def compute_htmt(data: pd.DataFrame, blocks: dict[str, list[str]]) -> pd.DataFrame:
    constructs = list(blocks.keys())
    corr = data.corr(numeric_only=True)
    htmt = pd.DataFrame(np.eye(len(constructs)), index=constructs, columns=constructs)

    def safe_mean_abs(values: list[float]) -> float:
        if len(values) == 0:
            return np.nan
        return float(np.mean(np.abs(values)))

    for i, a in enumerate(constructs):
        for j, b in enumerate(constructs):
            if i >= j:
                continue
            a_inds, b_inds = blocks[a], blocks[b]
            hetero = [corr.loc[x, y] for x in a_inds for y in b_inds]
            mono_a = [
                corr.loc[x, y]
                for idx, x in enumerate(a_inds)
                for y in a_inds[idx + 1 :]
            ]
            mono_b = [
                corr.loc[x, y]
                for idx, x in enumerate(b_inds)
                for y in b_inds[idx + 1 :]
            ]

            hetero_mean = safe_mean_abs(hetero)
            mono_a_mean = safe_mean_abs(mono_a)
            mono_b_mean = safe_mean_abs(mono_b)

            if (
                np.isnan(mono_a_mean)
                or np.isnan(mono_b_mean)
                or mono_a_mean <= 0
                or mono_b_mean <= 0
            ):
                value = np.nan
            else:
                value = hetero_mean / np.sqrt(mono_a_mean * mono_b_mean)

            htmt.loc[a, b] = value
            htmt.loc[b, a] = value

    return htmt


def compute_fornell_larcker(
    inner_summary: pd.DataFrame, scores: pd.DataFrame
) -> pd.DataFrame:
    constructs = list(BLOCKS.keys())
    latent_corr = scores[constructs].corr()
    fl = latent_corr.copy()
    for lv in constructs:
        ave = float(inner_summary.loc[lv, "ave"])
        fl.loc[lv, lv] = np.sqrt(max(ave, 0.0))
    return fl


# ========================
# f² EFFECT SIZE (omission technique, no bootstrap)
# ========================
def compute_f2(data: pd.DataFrame, full_model: Plspm) -> pd.DataFrame:
    full_r2 = full_model.inner_summary()["r_squared"].to_dict()
    f2_rows: list[dict[str, float | str]] = []

    for source, target in STRUCTURAL_EDGES:
        if target not in ENDOGENOUS:
            continue
        reduced_edges = [
            (s, t) for (s, t) in STRUCTURAL_EDGES if not (s == source and t == target)
        ]
        reduced_model = fit_pls(data=data, edges=reduced_edges)
        r2_incl = float(full_r2.get(target, np.nan))
        r2_excl = float(reduced_model.inner_summary().loc[target, "r_squared"])
        denom = 1.0 - r2_incl
        f2 = np.nan if denom <= 1e-12 else (r2_incl - r2_excl) / denom

        if np.isnan(f2):
            interp = "NA"
        elif f2 < 0.02:
            interp = "Negligible"
        elif f2 < 0.15:
            interp = "Small"
        elif f2 < 0.35:
            interp = "Medium"
        else:
            interp = "Large"

        f2_rows.append(
            {
                "Path": f"{source} -> {target}",
                "Source": source,
                "Target": target,
                "R2_included": r2_incl,
                "R2_excluded": r2_excl,
                "f2": f2,
                "f2_interpretation": interp,
            }
        )

    return pd.DataFrame(f2_rows)


# ========================
# Q² PREDICTIVE RELEVANCE (cross-validated latent scores)
# ========================
def compute_q2_scores(
    scores: pd.DataFrame, edges: list[tuple[str, str]]
) -> pd.DataFrame:
    edge_lookup: dict[str, list[str]] = {}
    for src, tgt in edges:
        edge_lookup.setdefault(tgt, []).append(src)

    q2_rows: list[dict[str, float | str]] = []
    kf = KFold(n_splits=10, shuffle=True, random_state=RANDOM_SEED)

    for target in ENDOGENOUS:
        predictors = edge_lookup.get(target, [])
        if len(predictors) == 0:
            continue
        x = scores[predictors].to_numpy(dtype=float)
        y = scores[target].to_numpy(dtype=float)

        press = 0.0
        for tr_idx, te_idx in kf.split(x):
            model = LinearRegression()
            model.fit(x[tr_idx], y[tr_idx])
            y_pred = model.predict(x[te_idx])
            press += float(np.sum((y[te_idx] - y_pred) ** 2))

        sso = float(np.sum((y - np.mean(y)) ** 2))
        q2 = np.nan if sso <= 1e-12 else 1.0 - (press / sso)
        q2_rows.append(
            {
                "Construct": target,
                "Predictors": ", ".join(predictors),
                "PRESS": press,
                "SSO": sso,
                "Q2": q2,
                "Q2_positive": "Yes" if pd.notna(q2) and q2 > 0 else "No",
            }
        )

    return pd.DataFrame(q2_rows)


# ========================
# UNIFIED BOOTSTRAP: paths + indirect effects sekaligus
# ========================
def unified_bootstrap(data: pd.DataFrame, n_boot: int) -> dict[str, pd.DataFrame]:
    """Satu loop bootstrap menghasilkan distribusi untuk:
    - Setiap path coefficient (untuk t-stat dan CI)
    - Setiap indirect effect (untuk mediasi RM5)
    """
    rng = np.random.default_rng(RANDOM_SEED)
    n = len(data)

    path_records: list[dict[str, float]] = []
    indirect_records: list[dict[str, float]] = []
    failed = 0

    t0 = time.time()
    iterator = range(n_boot)
    use_tqdm = tqdm is not None
    if use_tqdm:
        iterator = tqdm(
            iterator,
            total=n_boot,
            desc="Bootstrap",
            unit="iter",
            file=sys.stdout,
            dynamic_ncols=True,
            mininterval=0.2,
            leave=True,
        )
        print("  Progress bar: tqdm aktif")
    else:
        print("  Progress bar: tqdm tidak tersedia, fallback ke progress teks")

    for i in iterator:
        if not use_tqdm and ((i + 1) % 100 == 0 or (i + 1) == n_boot):
            elapsed = time.time() - t0
            print(f"  Progress {i + 1}/{n_boot} ({elapsed:.1f}s)")
        idx = rng.integers(0, n, n)
        sample = data.iloc[idx].reset_index(drop=True)
        try:
            model = fit_pls(sample, STRUCTURAL_EDGES)
            path_df = model.path_coefficients()

            # Kumpulkan semua path coefficients
            path_rec: dict[str, float] = {}
            for target in path_df.index:
                for source in path_df.columns:
                    coef = float(path_df.loc[target, source])
                    if coef != 0 or f"{source} -> {target}" in [
                        f"{s} -> {t}" for s, t in STRUCTURAL_EDGES
                    ]:
                        path_rec[f"{source} -> {target}"] = coef
            path_records.append(path_rec)

            # Kumpulkan indirect effects
            a_tpack = float(path_df.loc["TPACK", "PjBL"])
            a_stem = float(path_df.loc["STEM", "PjBL"])
            a_esd = float(path_df.loc["ESD", "PjBL"])
            b_tpack = float(path_df.loc["RPP", "TPACK"])
            b_stem = float(path_df.loc["RPP", "STEM"])
            b_esd = float(path_df.loc["RPP", "ESD"])
            c_direct = float(path_df.loc["RPP", "PjBL"])

            ind_tpack = a_tpack * b_tpack
            ind_stem = a_stem * b_stem
            ind_esd = a_esd * b_esd
            ind_total = ind_tpack + ind_stem + ind_esd
            total = c_direct + ind_total

            indirect_records.append(
                {
                    "ind_tpack": ind_tpack,
                    "ind_stem": ind_stem,
                    "ind_esd": ind_esd,
                    "ind_total": ind_total,
                    "direct": c_direct,
                    "total": total,
                }
            )
        except Exception:
            failed += 1
            continue

    elapsed = time.time() - t0
    print(f"  Bootstrap selesai: {n_boot - failed}/{n_boot} sukses ({elapsed:.1f}s)")

    return {
        "paths": pd.DataFrame(path_records),
        "indirect": pd.DataFrame(indirect_records),
    }


def summarize_boot_series(series: pd.Series) -> dict[str, float]:
    arr = series.dropna().to_numpy(dtype=float)
    if len(arr) == 0:
        return {
            "Boot_Mean": np.nan,
            "Std_Error": np.nan,
            "t_value": np.nan,
            "p_value": np.nan,
            "CI_2.5%": np.nan,
            "CI_97.5%": np.nan,
        }
    mean_val = float(np.mean(arr))
    se = float(np.std(arr, ddof=1))
    lci = float(np.quantile(arr, 0.025))
    uci = float(np.quantile(arr, 0.975))
    t_stat = np.nan if se <= 1e-12 else mean_val / se
    p_val = np.nan if np.isnan(t_stat) else 2 * (1 - norm.cdf(abs(t_stat)))
    return {
        "Boot_Mean": mean_val,
        "Std_Error": se,
        "t_value": t_stat,
        "p_value": p_val,
        "CI_2.5%": lci,
        "CI_97.5%": uci,
    }


# ========================
# SOBEL TEST (cross-check mediasi, tidak butuh bootstrap)
# ========================
def sobel_test(a: float, b: float, se_a: float, se_b: float) -> dict[str, float]:
    """Sobel test untuk signifikansi indirect effect a*b."""
    indirect = a * b
    se_indirect = np.sqrt(b**2 * se_a**2 + a**2 * se_b**2)
    z = np.nan if se_indirect <= 1e-12 else indirect / se_indirect
    p = np.nan if np.isnan(z) else 2 * (1 - norm.cdf(abs(z)))
    return {
        "indirect": indirect,
        "se_sobel": se_indirect,
        "z_sobel": z,
        "p_sobel": p,
    }


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    t_start = time.time()

    # ========================
    # LOAD DATA
    # ========================
    data = pd.read_csv(DATA_PATH)
    all_cols = [col for cols in BLOCKS.values() for col in cols]
    df = data[all_cols].dropna().copy()

    print(f"Data untuk RM2-RM5: {df.shape[0]} baris, {df.shape[1]} indikator")

    # ========================
    # FIT MODEL UTAMA (TANPA bootstrap bawaan plspm)
    # ========================
    print("Fitting model utama (tanpa bootstrap bawaan) ...")
    pls_model = fit_pls(data=df, edges=STRUCTURAL_EDGES)
    print("  Model PLS selesai diestimasi")

    # ========================
    # UNIFIED BOOTSTRAP (1 loop untuk paths + indirect)
    # ========================
    print(f"Running unified bootstrap ({N_BOOTSTRAP} iterasi) ...")
    boot_results = unified_bootstrap(df, n_boot=N_BOOTSTRAP)
    boot_paths_df = boot_results["paths"]
    boot_indirect_df = boot_results["indirect"]

    # ========================
    # TABLE 6: LOADINGS (outer model)
    # ========================
    outer_model = pls_model.outer_model()
    table6_loadings = build_loading_table(outer_model)
    table6_loadings["Loading_OK_0.708"] = table6_loadings["Loading"].apply(
        lambda x: "Yes" if x >= 0.708 else "No"
    )
    table6_loadings.to_csv(OUTPUT_DIR / "sem_table6_loadings.csv", index=False)
    print("  Table 6 (loadings) saved")

    # ========================
    # TABLE 7: VALIDITAS & RELIABILITAS (AVE, CR, Alpha)
    # ========================
    inner_summary = pls_model.inner_summary()
    uni = (
        pls_model.unidimensionality()
        .reset_index()
        .rename(columns={"index": "Construct"})
    )
    uni = uni.rename(
        columns={
            "cronbach_alpha": "Cronbach_Alpha",
            "dillon_goldstein_rho": "Composite_Reliability",
        }
    )

    table7 = pd.DataFrame(
        {
            "Construct": inner_summary.index,
            "AVE": inner_summary["ave"].values,
        }
    ).merge(
        uni[["Construct", "Cronbach_Alpha", "Composite_Reliability"]],
        on="Construct",
        how="left",
    )
    table7["AVE_OK_0.50"] = table7["AVE"].apply(lambda x: "Yes" if x >= 0.5 else "No")
    table7["CR_OK_0.70"] = table7["Composite_Reliability"].apply(
        lambda x: "Yes" if pd.notna(x) and x >= 0.7 else "No"
    )
    table7["Alpha_OK_0.70"] = table7["Cronbach_Alpha"].apply(
        lambda x: "Yes" if pd.notna(x) and x >= 0.7 else "No"
    )
    table7.to_csv(OUTPUT_DIR / "sem_table7_ave_cr.csv", index=False)

    # HTMT
    htmt = compute_htmt(df, BLOCKS)
    htmt.to_csv(OUTPUT_DIR / "sem_htmt_matrix.csv", index=True)

    # Fornell-Larcker
    scores = pls_model.scores()
    fornell = compute_fornell_larcker(inner_summary, scores)
    fornell.to_csv(OUTPUT_DIR / "sem_fornell_larcker.csv", index=True)
    print("  Table 7 (AVE/CR), HTMT, Fornell-Larcker saved")

    # ========================
    # TABLE 8: DIRECT EFFECTS (paths + bootstrap CI dari unified bootstrap)
    # ========================
    path_long = path_matrix_to_long(pls_model.path_coefficients())

    # Gabungkan bootstrap stats per path
    boot_stats_rows = []
    for _, row in path_long.iterrows():
        path_label = row["Path"]
        if path_label in boot_paths_df.columns:
            stats = summarize_boot_series(boot_paths_df[path_label])
        else:
            stats = summarize_boot_series(pd.Series(dtype=float))
        boot_stats_rows.append({"Path": path_label, **stats})

    boot_stats_table = pd.DataFrame(boot_stats_rows)
    table8 = path_long.merge(boot_stats_table, on="Path", how="left")
    table8["Significant_0.05"] = table8["p_value"].apply(
        lambda p: "Yes" if pd.notna(p) and p < 0.05 else "No"
    )

    # f² effect size
    print("  Computing f² effect size ...")
    f2_df = compute_f2(df, pls_model)
    table8 = table8.merge(
        f2_df[["Path", "f2", "f2_interpretation"]], on="Path", how="left"
    )
    table8.to_csv(OUTPUT_DIR / "sem_table8_paths.csv", index=False)
    print("  Table 8 (path coefficients + f²) saved")

    # ========================
    # TABLE 9: RM3 COMPARISON (PjBL -> TPACK/STEM/ESD)
    # ========================
    table9 = table8[
        (table8["Source"] == "PjBL") & (table8["Target"].isin(["TPACK", "STEM", "ESD"]))
    ].copy()
    table9 = table9.sort_values("Beta", ascending=False).reset_index(drop=True)
    table9["Rank"] = np.arange(1, len(table9) + 1)
    table9.to_csv(OUTPUT_DIR / "sem_table9_r2.csv", index=False)
    table9.to_csv(OUTPUT_DIR / "sem_table10_comparison.csv", index=False)
    table9.to_csv(OUTPUT_DIR / "sem_rm3_path_comparison.csv", index=False)

    # ========================
    # TABLE 10/11: RM4 — R² & HOC (paths ke RPP)
    # ========================
    r2_table = pd.DataFrame(
        {
            "Construct": inner_summary.index,
            "R2": inner_summary["r_squared"].values,
            "Communality": inner_summary["block_communality"].values,
            "Redundancy": inner_summary["mean_redundancy"].values,
            "AVE": inner_summary["ave"].values,
        }
    )
    r2_table.to_csv(OUTPUT_DIR / "sem_r2.csv", index=False)

    table11_hoc = table8[
        (table8["Target"] == "RPP")
        & (table8["Source"].isin(["TPACK", "STEM", "ESD", "PjBL"]))
    ].copy()
    table11_hoc.to_csv(OUTPUT_DIR / "sem_table11_hoc.csv", index=False)
    table11_hoc.to_csv(OUTPUT_DIR / "sem_rm4_hoc_paths.csv", index=False)
    print("  Table 9-11 (RM3, R², HOC) saved")

    # ========================
    # TABLE 12: RM5 MEDIATION (bootstrap CI + Sobel)
    # ========================
    path_mat = pls_model.path_coefficients()
    a_tpack = float(path_mat.loc["TPACK", "PjBL"])
    a_stem = float(path_mat.loc["STEM", "PjBL"])
    a_esd = float(path_mat.loc["ESD", "PjBL"])
    b_tpack = float(path_mat.loc["RPP", "TPACK"])
    b_stem = float(path_mat.loc["RPP", "STEM"])
    b_esd = float(path_mat.loc["RPP", "ESD"])
    c_direct = float(path_mat.loc["RPP", "PjBL"])

    ind_tpack = a_tpack * b_tpack
    ind_stem = a_stem * b_stem
    ind_esd = a_esd * b_esd
    ind_total = ind_tpack + ind_stem + ind_esd
    total_effect = c_direct + ind_total

    # Sobel test per mediator (butuh SE dari bootstrap paths)
    def get_path_se(path_label: str) -> float:
        if path_label in boot_paths_df.columns:
            return float(boot_paths_df[path_label].std(ddof=1))
        return np.nan

    sobel_tpack = sobel_test(
        a_tpack, b_tpack, get_path_se("PjBL -> TPACK"), get_path_se("TPACK -> RPP")
    )
    sobel_stem = sobel_test(
        a_stem, b_stem, get_path_se("PjBL -> STEM"), get_path_se("STEM -> RPP")
    )
    sobel_esd = sobel_test(
        a_esd, b_esd, get_path_se("PjBL -> ESD"), get_path_se("ESD -> RPP")
    )

    # Bootstrap CI untuk indirect effects
    med_rows = []
    sobel_lookup = {
        "ind_tpack": sobel_tpack,
        "ind_stem": sobel_stem,
        "ind_esd": sobel_esd,
    }
    for label, key, estimate in [
        ("PjBL -> TPACK -> RPP", "ind_tpack", ind_tpack),
        ("PjBL -> STEM -> RPP", "ind_stem", ind_stem),
        ("PjBL -> ESD -> RPP", "ind_esd", ind_esd),
        ("Total indirect", "ind_total", ind_total),
        ("Direct effect", "direct", c_direct),
        ("Total effect", "total", total_effect),
    ]:
        stats = summarize_boot_series(boot_indirect_df[key])

        vaf = np.nan
        mediation_type = "NA"
        z_sobel = np.nan
        p_sobel = np.nan

        if "ind_" in key and key != "ind_total":
            vaf = np.nan if abs(total_effect) <= 1e-12 else estimate / total_effect
            if np.isnan(vaf):
                mediation_type = "NA"
            elif vaf < 0.2:
                mediation_type = "No mediation"
            elif vaf <= 0.8:
                mediation_type = "Partial mediation"
            else:
                mediation_type = "Full mediation"

            if key in sobel_lookup:
                z_sobel = sobel_lookup[key]["z_sobel"]
                p_sobel = sobel_lookup[key]["p_sobel"]

        med_rows.append(
            {
                "Indirect_Path": label,
                "Estimate_Original": estimate,
                **stats,
                "VAF": vaf,
                "Mediation_Type": mediation_type,
                "z_Sobel": z_sobel,
                "p_Sobel": p_sobel,
            }
        )

    table12 = pd.DataFrame(med_rows)
    table12.to_csv(OUTPUT_DIR / "sem_table12_mediation.csv", index=False)
    table12.to_csv(OUTPUT_DIR / "sem_rm5_mediation.csv", index=False)
    print("  Table 12 (mediation) saved")

    # ========================
    # METRIK TAMBAHAN
    # ========================
    q2_df = compute_q2_scores(scores, STRUCTURAL_EDGES)
    q2_df.to_csv(OUTPUT_DIR / "sem_q2_predictive_relevance.csv", index=False)
    print("  Q² predictive relevance saved")

    effects_df = pls_model.effects().reset_index().rename(columns={"index": "Path"})
    effects_df.to_csv(OUTPUT_DIR / "sem_effects_direct_indirect_total.csv", index=False)

    # Bootstrap paths summary (dari unified bootstrap)
    boot_summary_rows = []
    for col in boot_paths_df.columns:
        stats = summarize_boot_series(boot_paths_df[col])
        boot_summary_rows.append({"Path": col, **stats})
    boot_summary = pd.DataFrame(boot_summary_rows)
    boot_summary.to_csv(OUTPUT_DIR / "sem_bootstrap_paths.csv", index=False)
    print("  Bootstrap path summary saved")

    # ========================
    # FIGURES 3-5
    # ========================
    rm3_plot = table9.copy()
    plt.figure(figsize=(8, 5))
    plt.bar(
        rm3_plot["Target"],
        rm3_plot["Beta"],
        color=["#0072B2", "#E69F00", "#009E73"],  # Okabe-Ito: TPACK, STEM, ESD
    )
    plt.xlabel("Dimension")
    plt.ylabel("Path Coefficient (β)")
    plt.title("Path Coefficients from PjBL to Mediating Constructs")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "fig3_sem_rm3_paths.png", dpi=300)
    plt.close()

    rpp_paths = table11_hoc.sort_values("Beta", ascending=False)
    plt.figure(figsize=(8, 5))
    # Color mapping for predictors (sorted by Beta descending: STEM, TPACK, ESD, PjBL)
    predictor_colors = {
        "STEM": "#E69F00",  # Okabe-Ito Orange
        "TPACK": "#0072B2",  # Okabe-Ito Blue
        "ESD": "#009E73",  # Okabe-Ito Green
        "PjBL": "#D55E00",  # Okabe-Ito Vermillion
    }
    bar_colors = [predictor_colors.get(src, "#999999") for src in rpp_paths["Source"]]
    plt.bar(rpp_paths["Source"], rpp_paths["Beta"], color=bar_colors)
    plt.xlabel("Predictor")
    plt.ylabel("Path Coefficient (β)")
    plt.title("Predictors of Integrative Lesson Plan Quality")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "fig4_sem_full_model_hoc_proxy.png", dpi=300)
    plt.close()

    med_plot = table12[
        table12["Indirect_Path"].isin(
            [
                "PjBL -> TPACK -> RPP",
                "PjBL -> STEM -> RPP",
                "PjBL -> ESD -> RPP",
            ]
        )
    ]
    plt.figure(figsize=(8, 5))
    plt.bar(
        med_plot["Indirect_Path"],
        med_plot["Estimate_Original"],
        color=["#0072B2", "#E69F00", "#009E73"],  # Okabe-Ito: TPACK, STEM, ESD paths
    )
    plt.xticks(rotation=20, ha="right")
    plt.ylabel("Indirect Effect")
    plt.title("Specific Indirect Effects via Mediating Constructs")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "fig5_sem_mediation_paths.png", dpi=300)
    plt.close()
    print("  Figures 3-5 saved")

    # ========================
    # FILE KOMPATIBILITAS NAMA LAMA
    # ========================
    table6_loadings.to_csv(OUTPUT_DIR / "sem_loadings.csv", index=False)
    table7.to_csv(OUTPUT_DIR / "sem_outer_quality.csv", index=False)
    table8.to_csv(OUTPUT_DIR / "sem_path_coefficients.csv", index=False)
    r2_table.to_csv(OUTPUT_DIR / "sem_table10_hoc.csv", index=False)

    # ========================
    # LIMITATIONS FLAGS
    # ========================
    limitations = pd.DataFrame(
        [
            {
                "Flag": "PjBL05_removed_zero_variance",
                "Status": "Yes",
                "Note": "Indikator PjBL05 dihapus karena variansi nol.",
            },
            {
                "Flag": "Model_type",
                "Status": "PLS-PM",
                "Note": "Analisis menggunakan plspm Python 0.5.7 (variance-based SEM).",
            },
            {
                "Flag": "RPP_single_indicator",
                "Status": "Yes",
                "Note": "RPP dimodelkan sebagai single-indicator construct.",
            },
            {
                "Flag": "Q2_method",
                "Status": "Cross-validated latent-score approximation",
                "Note": "Q2 dihitung pendekatan prediksi skor laten (bukan blindfolding bawaan software GUI).",
            },
            {
                "Flag": "Bootstrap_method",
                "Status": f"Unified manual bootstrap ({N_BOOTSTRAP} iterations)",
                "Note": "Bootstrap dilakukan 1 loop manual (bukan bootstrap bawaan plspm) untuk efisiensi.",
            },
            {
                "Flag": "Mediation_crosscheck",
                "Status": "Sobel + Bootstrap percentile CI",
                "Note": "Mediasi diuji dengan dua metode: Sobel test dan bootstrap CI 95% percentile.",
            },
        ]
    )
    limitations.to_csv(OUTPUT_DIR / "sem_model_limitations.csv", index=False)

    elapsed_total = time.time() - t_start
    print(f"\n=== RM2-RM5 PLS selesai ({elapsed_total:.1f}s) ===")
    print(f"Output folder: {OUTPUT_DIR}")
    for f in sorted(OUTPUT_DIR.iterdir()):
        print(f"  - {f.name}")
