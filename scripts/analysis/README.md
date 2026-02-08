# Analisis

Jalankan dari root proyek (`/Users/pinguinhalt/Documents/UNNES/tpack`) dengan environment `tpack-research`.

## RM1

```bash
conda run -n tpack-research python scripts/analysis/rm1_analysis.py
```

Output: `outputs/rm1/`

## RM2-RM5

```bash
conda run -n tpack-research python scripts/analysis/rm2_rm5_sem_analysis.py
```

Output: `outputs/rm2_rm5/`

Catatan: script RM2-RM5 menggunakan `semopy` (SEM berbasis kovarians) sebagai evidence awal struktur model.
