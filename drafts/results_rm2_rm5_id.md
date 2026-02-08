# Hasil: RM2-RM5 — Analisis PLS-SEM

*Draf v2.1 | Diperbarui dari output PLS-PM (`plspm` Python 0.5.7) | Bahasa Indonesia (gaya akademik)*
*Bootstrap: 5000 iterasi (unified manual bootstrap) | N = 95*

---

## 4.3 Evaluasi Model Pengukuran (Outer Model)

### 4.3.1 Convergent Validity — Outer Loadings

**Tabel 6. Outer Loadings per Indikator**

| Konstruk | Indikator | Loading | Threshold ≥ 0.708 |
|---|---|---:|---|
| **ESD** | ESD_EVA_post | 0.780 | Yes |
|  | ESD_INQ_post | 0.894 | Yes |
|  | ESD_PCK_post | 0.867 | Yes |
| **PjBL** | PjBL01 | 0.811 | Yes |
|  | PjBL02 | 0.834 | Yes |
|  | PjBL03 | 0.847 | Yes |
|  | PjBL04 | 0.857 | Yes |
| **TPACK** | TK_post | 0.690 | No |
|  | PK_post | 0.224 | No |
|  | CK_post | 0.673 | No |
|  | TPK_post | 0.760 | Yes |
|  | TCK_post | 0.795 | Yes |
|  | PCK_post | 0.401 | No |
|  | TPACK_post | 0.758 | Yes |
| **STEM** | S_post | 0.485 | No |
|  | T_post | 0.716 | Yes |
|  | E_post | 0.578 | No |
|  | M_post | 0.914 | Yes |
| **RPP** | RPPInt_total_post | 1.000 | Yes |

*Catatan:* Model SEM-PLS saat ini menggunakan indikator PjBL01-PjBL04 sesuai spesifikasi model pada skrip analisis.

### 4.3.2 Validitas & Reliabilitas Konstruk

**Tabel 7. AVE, Composite Reliability, dan Cronbach's Alpha**

| Konstruk | AVE | AVE ≥ 0.50 | Cronbach α | α ≥ 0.70 | CR | CR ≥ 0.70 |
|---|---:|---|---:|---|---:|---|
| ESD | 0.720 | Yes | 0.807 | Yes | 0.886 | Yes |
| PjBL | 0.701 | Yes | 0.857 | Yes | 0.904 | Yes |
| RPP | 1.000 | Yes | — | — | 1.000 | Yes |
| STEM | 0.480 | **No** | 0.694 | **No** | 0.814 | Yes |
| TPACK | 0.418 | **No** | 0.766 | Yes | 0.834 | Yes |

Konstruk PjBL dan ESD memenuhi kriteria convergent validity dan reliabilitas secara konsisten. Konstruk TPACK dan STEM masih menunjukkan AVE di bawah 0,50, meskipun CR berada di atas 0,70; karena itu, interpretasi konstruk ini tetap dilakukan dengan kehati-hatian metodologis.

### 4.3.3 Discriminant Validity — HTMT

**Tabel 7b. Matriks HTMT**

| | PjBL | TPACK | STEM | ESD | RPP |
|---|---:|---:|---:|---:|---:|
| PjBL | 1.000 | 0.846 | 0.876 | 0.726 | — |
| TPACK | 0.846 | 1.000 | 0.770 | 0.298 | — |
| STEM | 0.876 | 0.770 | 1.000 | 0.456 | — |
| ESD | 0.726 | 0.298 | 0.456 | 1.000 | — |
| RPP | — | — | — | — | 1.000 |

Seluruh nilai HTMT berada di bawah threshold 0,90 (Henseler et al., 2015), sehingga discriminant validity secara HTMT dapat diterima. Pasangan tertinggi adalah PjBL-STEM (0,876), menunjukkan kedekatan konseptual yang relatif tinggi namun masih dalam batas yang dapat diterima.

### 4.3.4 Fornell-Larcker Criterion

**Tabel 7c. Matriks Fornell-Larcker**

Diagonal = √AVE; off-diagonal = korelasi antar skor laten.

| | PjBL | TPACK | STEM | ESD | RPP |
|---|---:|---:|---:|---:|---:|
| PjBL | **0.837** | 0.718 | 0.671 | 0.612 | 0.873 |
| TPACK | 0.718 | **0.646** | 0.525 | 0.176 | 0.761 |
| STEM | 0.671 | 0.525 | **0.692** | 0.374 | 0.857 |
| ESD | 0.612 | 0.176 | 0.374 | **0.848** | 0.619 |
| RPP | 0.873 | 0.761 | 0.857 | 0.619 | **1.000** |

Secara Fornell-Larcker, beberapa pasangan masih menunjukkan overlap korelasional (misalnya TPACK-RPP dan STEM-RPP melebihi √AVE konstruk asal). Oleh karena itu, validitas diskriminan dinilai memadai berdasarkan HTMT, dengan catatan interpretasi konseptual tetap hati-hati.

---

## 4.4 RM2 — Pengaruh Langsung PjBL terhadap TPACK, STEM, ESD

**Tabel 8. Koefisien Jalur Langsung (Direct Effects) dengan Bootstrap CI**

| Jalur | β | Boot Mean | SE | t | p | CI 2.5% | CI 97.5% | Sig. | f² | Interpretasi f² |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| PjBL → TPACK | 0.718 | 0.722 | 0.053 | 13.561 | <0.001 | 0.606 | 0.811 | **Yes** | 1.063 | Large |
| PjBL → STEM | 0.671 | 0.675 | 0.056 | 11.987 | <0.001 | 0.558 | 0.775 | **Yes** | 0.820 | Large |
| PjBL → ESD | 0.612 | 0.613 | 0.065 | 9.454 | <0.001 | 0.482 | 0.733 | **Yes** | 0.598 | Large |
| PjBL → RPP | 0.040 | 0.043 | 0.042 | 1.025 | 0.305 | -0.038 | 0.127 | No | 0.015 | Negligible |
| TPACK → RPP | 0.420 | 0.414 | 0.036 | 11.645 | <0.001 | 0.343 | 0.483 | **Yes** | 2.987 | Large |
| STEM → RPP | 0.483 | 0.484 | 0.036 | 13.503 | <0.001 | 0.414 | 0.553 | **Yes** | 5.785 | Large |
| ESD → RPP | 0.340 | 0.335 | 0.040 | 8.464 | <0.001 | 0.261 | 0.417 | **Yes** | 2.546 | Large |

**R² Konstruk Endogen:**

| Konstruk | R² | Interpretasi |
|---|---:|---|
| TPACK | 0.515 | Moderate-Substantial |
| STEM | 0.451 | Moderate |
| ESD | 0.374 | Moderate |
| RPP | 0.978 | Substantial |

**Interpretasi RM2:** PjBL berpengaruh positif dan signifikan terhadap TPACK, STEM, dan ESD. Namun, pengaruh langsung PjBL terhadap RPP tidak signifikan (β = 0,040; p = 0,305), yang mengindikasikan bahwa pengaruh PjBL terhadap kualitas RPP terutama bekerja melalui jalur mediasi kompetensi integratif.

---

## 4.5 RM3 — Perbandingan Dimensi: PjBL → TPACK vs STEM vs ESD

**Tabel 9. Ranking Koefisien Jalur PjBL → Dimensi Integrasi**

| Rank | Dimensi | β | t | p | f² | Signifikan |
|---:|---|---:|---:|---:|---:|---|
| 1 | TPACK | 0.718 | 13.561 | <0.001 | 1.063 | Yes |
| 2 | STEM | 0.671 | 11.987 | <0.001 | 0.820 | Yes |
| 3 | ESD | 0.612 | 9.454 | <0.001 | 0.598 | Yes |

![Figur 3. Perbandingan Koefisien Jalur PjBL → TPACK/STEM/ESD](../outputs/rm2_rm5/fig3_sem_rm3_paths.png)

**Interpretasi RM3:** Seluruh dimensi responsif terhadap intervensi PjBL, dengan urutan kontribusi terbesar pada TPACK, diikuti STEM dan ESD. Perbedaan antar-koefisien diinterpretasikan deskriptif berdasarkan besar efek jalur.

---

## 4.6 RM4 — Kontribusi TPACK, STEM, ESD terhadap Kemampuan Integratif RPP

**Tabel 11. Jalur ke RPP Integratif**

| Prediktor | β | t | p | f² | Interpretasi f² |
|---|---:|---:|---:|---:|---|
| STEM | 0.483 | 13.503 | <0.001 | 5.785 | Large |
| TPACK | 0.420 | 11.645 | <0.001 | 2.987 | Large |
| ESD | 0.340 | 8.464 | <0.001 | 2.546 | Large |
| PjBL (langsung) | 0.040 | 1.025 | 0.305 | 0.015 | Negligible |

![Figur 4. Jalur ke Kualitas RPP Integratif](../outputs/rm2_rm5/fig4_sem_full_model_hoc_proxy.png)

**Interpretasi RM4:** Ketiga dimensi integrasi (STEM, TPACK, ESD) berkontribusi positif-signifikan terhadap kualitas RPP dengan ukuran efek besar. Pengaruh langsung PjBL terhadap RPP tetap tidak signifikan, sehingga mekanisme utama peningkatan RPP terjadi melalui peningkatan kompetensi integratif.

**Q² Predictive Relevance:**

| Konstruk | Q² | Relevansi Prediktif |
|---|---:|---|
| TPACK | 0.493 | Besar |
| STEM | 0.411 | Besar |
| ESD | 0.345 | Sedang-Besar |
| RPP | 0.975 | Sangat besar |

Nilai Q² seluruh konstruk endogen positif, menunjukkan model memiliki relevansi prediktif yang baik hingga sangat baik.

---

## 4.7 RM5 — Analisis Mediasi: Efek Tidak Langsung PjBL melalui TPACK, STEM, ESD

**Tabel 12. Efek Tidak Langsung dan Mediasi (Bootstrap 5000 iterasi)**

| Jalur | Estimate | Boot Mean | SE | t | p | CI 2.5% | CI 97.5% | VAF | Tipe Mediasi |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| PjBL → TPACK → RPP | 0.301 | 0.299 | 0.034 | 8.840 | <0.001 | 0.235 | 0.364 | 0.345 | Partial |
| PjBL → STEM → RPP | 0.324 | 0.327 | 0.033 | 9.825 | <0.001 | 0.265 | 0.395 | 0.371 | Partial |
| PjBL → ESD → RPP | 0.208 | 0.205 | 0.031 | 6.642 | <0.001 | 0.148 | 0.270 | 0.238 | Partial |
| Total indirect | 0.833 | 0.830 | 0.038 | 21.919 | <0.001 | 0.756 | 0.905 | — | — |
| Direct effect | 0.040 | 0.043 | 0.042 | 1.025 | 0.305 | -0.038 | 0.127 | — | — |
| Total effect | 0.873 | 0.873 | 0.023 | 38.027 | <0.001 | 0.822 | 0.913 | — | — |

**Cross-check Sobel Test:**

| Jalur Mediasi | z Sobel | p Sobel |
|---|---:|---:|
| PjBL → TPACK → RPP | 8.882 | <0.001 |
| PjBL → STEM → RPP | 8.918 | <0.001 |
| PjBL → ESD → RPP | 6.362 | <0.001 |

![Figur 5. Jalur Mediasi PjBL → Dimensi → RPP](../outputs/rm2_rm5/fig5_sem_mediation_paths.png)

**Interpretasi RM5:**

1. Ketiga jalur mediasi spesifik (melalui TPACK, STEM, dan ESD) signifikan dan konsisten antara bootstrap percentile CI serta uji Sobel.

2. Jalur mediasi terbesar berasal dari STEM (indirect β = 0,324), diikuti TPACK (β = 0,301) dan ESD (β = 0,208).

3. Total indirect effect sangat signifikan, sementara direct effect PjBL -> RPP tidak signifikan. Pola ini menunjukkan **full mediation secara agregat**: pengaruh PjBL terhadap kualitas RPP terutama bekerja melalui peningkatan dimensi integrasi.

---

## 4.8 Ringkasan Model Struktural

| Komponen | Temuan |
|---|---|
| **RM2** | PjBL -> TPACK, STEM, dan ESD semuanya signifikan |
| **RM3** | Urutan responsivitas: TPACK > STEM > ESD |
| **RM4** | STEM, TPACK, ESD berkontribusi signifikan ke RPP; direct PjBL -> RPP tidak signifikan |
| **RM5** | Full mediation secara agregat; jalur mediasi terbesar melalui STEM |
| **GoF** | R² RPP = 0.978; Q² RPP = 0.975 |

---

## Catatan Metodologis dan Keterbatasan Model

1. **TPACK dan STEM masih AVE < 0,50.** Meskipun CR memadai, validitas konvergen pada dua konstruk ini belum optimal dan perlu dipertimbangkan pada interpretasi.

2. **Fornell-Larcker belum sepenuhnya ideal** untuk beberapa pasangan yang melibatkan RPP, meskipun HTMT seluruh pasangan berada di bawah 0,90.

3. **RPP single-indicator construct.** AVE = 1,0 dan R² sangat tinggi perlu dibaca hati-hati karena konstruk outcome tidak memodelkan error antar-indikator.

4. **Bootstrap 5000 iterasi.** Jumlah iterasi sudah memadai untuk estimasi CI percentile yang stabil pada pelaporan final SEM-PLS.

5. **Desain one-group pretest-posttest** tanpa kelompok kontrol. Analisis SEM menggunakan data posttest, sehingga klaim kausalitas dibatasi pada asosiasi struktural.

---

*File output sumber:*
- `outputs/rm2_rm5/sem_table6_loadings.csv`
- `outputs/rm2_rm5/sem_table7_ave_cr.csv`
- `outputs/rm2_rm5/sem_htmt_matrix.csv`
- `outputs/rm2_rm5/sem_fornell_larcker.csv`
- `outputs/rm2_rm5/sem_table8_paths.csv`
- `outputs/rm2_rm5/sem_table9_r2.csv` / `sem_rm3_path_comparison.csv`
- `outputs/rm2_rm5/sem_table11_hoc.csv` / `sem_rm4_hoc_paths.csv`
- `outputs/rm2_rm5/sem_table12_mediation.csv` / `sem_rm5_mediation.csv`
- `outputs/rm2_rm5/sem_q2_predictive_relevance.csv`
- `outputs/rm2_rm5/sem_model_limitations.csv`
- `outputs/rm2_rm5/fig3_sem_rm3_paths.png`
- `outputs/rm2_rm5/fig4_sem_full_model_hoc_proxy.png`
- `outputs/rm2_rm5/fig5_sem_mediation_paths.png`

*Draf ini menggantikan versi 1.0 yang menggunakan CB-SEM (semopy). Seluruh angka di atas berasal dari PLS-PM (plspm Python 0.5.7) dengan unified manual bootstrap 5000 iterasi.*
