"""Generate synthetic barometer dataset by replacing all PjBL items.

Tujuan:
- Membuat dataset sintetis untuk uji sensitivitas/barometer.
- Memodifikasi semua indikator PjBL01-05 agar variabilitas tinggi
  (target std > 0.7) dan berkorelasi dengan konstruk post-test.

Catatan:
- Dataset ini bukan pengganti data utama penelitian.
- Gunakan hanya untuk stress-test model / barometer analisis.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def to_likert_1_4(scores: np.ndarray) -> np.ndarray:
    """Map continuous scores to balanced Likert 1-4 via quartiles."""
    q1, q2, q3 = np.quantile(scores, [0.25, 0.50, 0.75])
    out = np.ones_like(scores, dtype=int)
    out[scores > q1] = 2
    out[scores > q2] = 3
    out[scores > q3] = 4
    return out


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    input_csv = root / "dataset.csv"
    out_dir = root / "outputs" / "sensitivity"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_csv = out_dir / "dataset_synthetic_pjbl_all.csv"
    out_xlsx = out_dir / "dataset_synthetic_pjbl_all.xlsx"
    out_summary = out_dir / "dataset_synthetic_pjbl_all_summary.csv"

    rng = np.random.default_rng(20260207)
    df = pd.read_csv(input_csv)

    # Build latent proxy from post-test constructs (standardized)
    proxy_cols = [
        "TPACK_total_post",
        "STEM_total_post",
        "ESD_total_post",
        "RPPInt_total_post",
    ]
    z = (df[proxy_cols] - df[proxy_cols].mean()) / df[proxy_cols].std(ddof=0)
    latent = z.mean(axis=1).to_numpy(dtype=float)

    # Create five synthetic PjBL indicators with controlled noise.
    # Lower noise => stronger relationship with latent outcomes.
    noise_scales = {
        "PjBL01": 0.55,
        "PjBL02": 0.60,
        "PjBL03": 0.50,
        "PjBL04": 0.65,
        "PjBL05": 0.58,
    }

    df_syn = df.copy()
    for col, sigma in noise_scales.items():
        signal = latent + rng.normal(0.0, sigma, size=len(df_syn))
        df_syn[col] = to_likert_1_4(signal)

    # Save synthetic dataset
    df_syn.to_csv(out_csv, index=False)
    df_syn.to_excel(out_xlsx, index=False)

    # Summary stats + correlation to outcome constructs for quick diagnostics
    rows: list[dict[str, float | str]] = []
    for col in ["PjBL01", "PjBL02", "PjBL03", "PjBL04", "PjBL05"]:
        rows.append(
            {
                "variable": col,
                "mean": float(df_syn[col].mean()),
                "std": float(df_syn[col].std(ddof=1)),
                "min": float(df_syn[col].min()),
                "max": float(df_syn[col].max()),
                "corr_TPACK_total_post": float(
                    df_syn[col].corr(df_syn["TPACK_total_post"])
                ),
                "corr_STEM_total_post": float(
                    df_syn[col].corr(df_syn["STEM_total_post"])
                ),
                "corr_ESD_total_post": float(
                    df_syn[col].corr(df_syn["ESD_total_post"])
                ),
                "corr_RPPInt_total_post": float(
                    df_syn[col].corr(df_syn["RPPInt_total_post"])
                ),
            }
        )

    summary = pd.DataFrame(rows)
    summary.to_csv(out_summary, index=False)

    print(f"Saved: {out_csv}")
    print(f"Saved: {out_xlsx}")
    print(f"Saved: {out_summary}")
    print("\nPjBL std check:")
    print(summary[["variable", "std"]].to_string(index=False))


if __name__ == "__main__":
    main()
