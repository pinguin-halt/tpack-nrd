"""Generate sensitivity dataset by modifying PjBL04 and PjBL05.

Tujuan:
- Membuat dataset alternatif untuk uji ulang model RM2-RM5
  tanpa mengubah data mentah `dataset.csv`.
- Memperbaiki isu variansi nol pada PjBL05 dan variansi sangat rendah pada PjBL04.

Catatan penting:
- Dataset ini bersifat *what-if / sensitivity analysis*.
- BUKAN pengganti data asli untuk klaim utama paper.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def quantile_to_likert(
    values: np.ndarray, bins: tuple[float, float, float]
) -> np.ndarray:
    """Map continuous scores to Likert 1-4 using quantile thresholds."""
    q1, q2, q3 = np.quantile(values, bins)
    out = np.ones_like(values, dtype=int)
    out[values > q1] = 2
    out[values > q2] = 3
    out[values > q3] = 4
    return out


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    input_csv = root / "dataset.csv"
    out_dir = root / "outputs" / "sensitivity"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_csv = out_dir / "dataset_pjbl45_modified.csv"
    out_xlsx = out_dir / "dataset_pjbl45_modified.xlsx"
    summary_csv = out_dir / "dataset_pjbl45_modified_summary.csv"

    df = pd.read_csv(input_csv)
    rng = np.random.default_rng(42)

    # Latent quality proxy from post-test constructs (scaled)
    proxy_cols = [
        "TPACK_total_post",
        "STEM_total_post",
        "ESD_total_post",
        "RPPInt_total_post",
    ]
    z = (df[proxy_cols] - df[proxy_cols].mean()) / df[proxy_cols].std(ddof=0)
    latent = z.mean(axis=1).to_numpy(dtype=float)

    # Add small noise to avoid deterministic mapping
    noise_04 = rng.normal(0, 0.35, len(df))
    noise_05 = rng.normal(0, 0.40, len(df))

    score_04 = latent + noise_04
    score_05 = latent + noise_05

    # Map to Likert 2-4 dominated distribution (realistic for observation data)
    # Thresholds chosen to create variance and retain high-end tendency.
    pjbl04_new = quantile_to_likert(score_04, (0.10, 0.45, 0.75))
    pjbl05_new = quantile_to_likert(score_05, (0.15, 0.50, 0.80))

    # Shift to avoid many value=1 for observation context
    pjbl04_new = np.clip(pjbl04_new + 1, 1, 4)
    pjbl05_new = np.clip(pjbl05_new + 1, 1, 4)

    df_new = df.copy()
    df_new["PjBL04"] = pjbl04_new
    df_new["PjBL05"] = pjbl05_new

    df_new.to_csv(out_csv, index=False)
    df_new.to_excel(out_xlsx, index=False)

    summary = pd.DataFrame(
        {
            "variable": ["PjBL04_old", "PjBL05_old", "PjBL04_new", "PjBL05_new"],
            "mean": [
                df["PjBL04"].mean(),
                df["PjBL05"].mean(),
                df_new["PjBL04"].mean(),
                df_new["PjBL05"].mean(),
            ],
            "std": [
                df["PjBL04"].std(),
                df["PjBL05"].std(),
                df_new["PjBL04"].std(),
                df_new["PjBL05"].std(),
            ],
            "min": [
                df["PjBL04"].min(),
                df["PjBL05"].min(),
                df_new["PjBL04"].min(),
                df_new["PjBL05"].min(),
            ],
            "max": [
                df["PjBL04"].max(),
                df["PjBL05"].max(),
                df_new["PjBL04"].max(),
                df_new["PjBL05"].max(),
            ],
        }
    )
    summary.to_csv(summary_csv, index=False)

    print(f"Saved: {out_csv}")
    print(f"Saved: {out_xlsx}")
    print(f"Saved: {summary_csv}")


if __name__ == "__main__":
    main()
