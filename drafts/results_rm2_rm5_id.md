# Hasil: RM2-RM5 — Analisis PLS-SEM

*Draf v2.1 | Diperbarui dari output PLS-PM (`plspm` Python 0.5.7) | Bahasa Indonesia (gaya akademik)*
*Bootstrap: 5000 iterasi (unified manual bootstrap) | N = 95*

---

## 4.3 Evaluasi Model Pengukuran (Outer Model)

### 4.3.1 Convergent Validity — Outer Loadings

**Tabel 6. Outer Loadings per Indikator**

| Konstruk | Indikator | Loading | Threshold ≥ 0.708 |
|---|---|---:|---|
| **ESD** | ESD_EVA_post | 0.776 | Yes |
|  | ESD_INQ_post | 0.894 | Yes |
|  | ESD_PCK_post | 0.870 | Yes |
| **PjBL** | PjBL01 | 0.815 | Yes |
|  | PjBL02 | 0.804 | Yes |
|  | PjBL03 | 0.835 | Yes |
|  | PjBL04 | 0.850 | Yes |
|  | PjBL05 | 0.840 | Yes |
| **TPACK** | TK_post | 0.689 | No |
|  | PK_post | 0.224 | No |
|  | CK_post | 0.673 | No |
|  | TPK_post | 0.760 | Yes |
|  | TCK_post | 0.795 | Yes |
|  | PCK_post | 0.400 | No |
|  | TPACK_post | 0.759 | Yes |
| **STEM** | S_post | 0.484 | No |
|  | T_post | 0.713 | Yes |
|  | E_post | 0.577 | No |
|  | M_post | 0.916 | Yes |
| **RPP** | RPPInt_total_post | 1.000 | Yes |

*Catatan:* Model SEM-PLS saat ini menggunakan seluruh indikator PjBL01-PjBL05 sesuai spesifikasi model pada skrip analisis.

### 4.3.2 Validitas & Reliabilitas Konstruk

**Tabel 7. AVE, Composite Reliability, dan Cronbach's Alpha**

| Konstruk | AVE | AVE ≥ 0.50 | Cronbach α | α ≥ 0.70 | CR | CR ≥ 0.70 |
|---|---:|---|---:|---|---:|---|
| ESD | 0.720 | Yes | 0.807 | Yes | 0.886 | Yes |
| PjBL | 0.687 | Yes | 0.886 | Yes | 0.917 | Yes |
| RPP | 1.000 | Yes | — | — | 1.000 | Yes |
| STEM | 0.480 | **No** | 0.694 | **No** | 0.814 | Yes |
| TPACK | 0.418 | **No** | 0.766 | Yes | 0.834 | Yes |

Konstruk PjBL dan ESD memenuhi kriteria convergent validity dan reliabilitas secara konsisten. Konstruk TPACK dan STEM masih menunjukkan AVE di bawah 0,50, meskipun CR berada di atas 0,70; karena itu, interpretasi konstruk ini tetap dilakukan dengan kehati-hatian metodologis.

### 4.3.3 Discriminant Validity — HTMT

**Tabel 7b. Matriks HTMT**

| | PjBL | TPACK | STEM | ESD | RPP |
|---|---:|---:|---:|---:|---:|
| PjBL | 1.000 | 0.837 | 0.871 | 0.716 | — |
| TPACK | 0.837 | 1.000 | 0.770 | 0.298 | — |
| STEM | 0.871 | 0.770 | 1.000 | 0.456 | — |
| ESD | 0.716 | 0.298 | 0.456 | 1.000 | — |
| RPP | — | — | — | — | 1.000 |

Seluruh nilai HTMT berada di bawah threshold 0,90 (Henseler et al., 2015), sehingga discriminant validity secara HTMT dapat diterima. Pasangan tertinggi adalah PjBL-STEM (0,871), menunjukkan kedekatan konseptual yang relatif tinggi namun masih dalam batas yang dapat diterima.

### 4.3.4 Fornell-Larcker Criterion

**Tabel 7c. Matriks Fornell-Larcker**

Diagonal = √AVE; off-diagonal = korelasi antar skor laten.

| | PjBL | TPACK | STEM | ESD | RPP |
|---|---:|---:|---:|---:|---:|
| PjBL | **0.829** | 0.727 | 0.683 | 0.617 | 0.882 |
| TPACK | 0.727 | **0.646** | 0.524 | 0.176 | 0.761 |
| STEM | 0.683 | 0.524 | **0.692** | 0.375 | 0.856 |
| ESD | 0.617 | 0.176 | 0.375 | **0.848** | 0.619 |
| RPP | 0.882 | 0.761 | 0.856 | 0.619 | **1.000** |

Secara Fornell-Larcker, beberapa pasangan masih menunjukkan overlap korelasional (misalnya TPACK-RPP dan STEM-RPP melebihi √AVE konstruk asal). Oleh karena itu, validitas diskriminan dinilai memadai berdasarkan HTMT, dengan catatan interpretasi konseptual tetap hati-hati.

---

## 4.4 RM2 — Pengaruh Langsung PjBL terhadap TPACK, STEM, ESD

**Tabel 8. Koefisien Jalur Langsung (Direct Effects) dengan Bootstrap CI**

| Jalur | β | Boot Mean | SE | t | p | CI 2.5% | CI 97.5% | Sig. | f² | Interpretasi f² |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| PjBL → TPACK | 0.727 | 0.732 | 0.055 | 13.295 | <0.001 | 0.610 | 0.823 | **Yes** | 1.123 | Large |
| PjBL → STEM | 0.683 | 0.686 | 0.054 | 12.616 | <0.001 | 0.573 | 0.782 | **Yes** | 0.872 | Large |
| PjBL → ESD | 0.617 | 0.618 | 0.065 | 9.496 | <0.001 | 0.485 | 0.739 | **Yes** | 0.614 | Large |
| PjBL → RPP | 0.030 | 0.034 | 0.045 | 0.770 | 0.441 | -0.055 | 0.123 | No | 0.007 | Negligible |
| TPACK → RPP | 0.425 | 0.418 | 0.037 | 11.346 | <0.001 | 0.345 | 0.491 | **Yes** | 2.783 | Large |
| STEM → RPP | 0.484 | 0.485 | 0.037 | 13.116 | <0.001 | 0.412 | 0.556 | **Yes** | 5.444 | Large |
| ESD → RPP | 0.345 | 0.338 | 0.040 | 8.355 | <0.001 | 0.264 | 0.423 | **Yes** | 2.399 | Large |

**R² Konstruk Endogen:**

| Konstruk | R² | Interpretasi |
|---|---:|---|
| TPACK | 0.529 | Moderate-Substantial |
| STEM | 0.466 | Moderate |
| ESD | 0.380 | Moderate |
| RPP | 0.977 | Substantial |

**Interpretasi RM2:** PjBL berpengaruh positif dan signifikan terhadap TPACK, STEM, dan ESD. Namun, pengaruh langsung PjBL terhadap RPP tidak signifikan (β = 0,030; p = 0,441), yang mengindikasikan bahwa pengaruh PjBL terhadap kualitas RPP terutama bekerja melalui jalur mediasi kompetensi integratif.

---

## 4.5 RM3 — Perbandingan Dimensi: PjBL → TPACK vs STEM vs ESD

**Tabel 9. Ranking Koefisien Jalur PjBL → Dimensi Integrasi**

| Rank | Dimensi | β | t | p | f² | Signifikan |
|---:|---|---:|---:|---:|---:|---|
| 1 | TPACK | 0.727 | 13.295 | <0.001 | 1.123 | Yes |
| 2 | STEM | 0.683 | 12.616 | <0.001 | 0.872 | Yes |
| 3 | ESD | 0.617 | 9.496 | <0.001 | 0.614 | Yes |

![Figur 3. Perbandingan Koefisien Jalur PjBL → TPACK/STEM/ESD](../outputs/rm2_rm5/fig3_sem_rm3_paths.png)

**Interpretasi RM3:** Seluruh dimensi responsif terhadap intervensi PjBL, dengan urutan kontribusi terbesar pada TPACK, diikuti STEM dan ESD. Perbedaan antar-koefisien diinterpretasikan deskriptif berdasarkan besar efek jalur.

---

## 4.6 RM4 — Kontribusi TPACK, STEM, ESD terhadap Kemampuan Integratif RPP

**Tabel 11. Jalur ke RPP Integratif**

| Prediktor | β | t | p | f² | Interpretasi f² |
|---|---:|---:|---:|---:|---|
| STEM | 0.484 | 13.116 | <0.001 | 5.444 | Large |
| TPACK | 0.425 | 11.346 | <0.001 | 2.783 | Large |
| ESD | 0.345 | 8.355 | <0.001 | 2.399 | Large |
| PjBL (langsung) | 0.030 | 0.770 | 0.441 | 0.007 | Negligible |

![Figur 4. Jalur ke Kualitas RPP Integratif](../outputs/rm2_rm5/fig4_sem_full_model_hoc_proxy.png)

**Interpretasi RM4:** Ketiga dimensi integrasi (STEM, TPACK, ESD) berkontribusi positif-signifikan terhadap kualitas RPP dengan ukuran efek besar. Pengaruh langsung PjBL terhadap RPP tetap tidak signifikan, sehingga mekanisme utama peningkatan RPP terjadi melalui peningkatan kompetensi integratif.

**Q² Predictive Relevance:**

| Konstruk | Q² | Relevansi Prediktif |
|---|---:|---|
| TPACK | 0.503 | Besar |
| STEM | 0.430 | Besar |
| ESD | 0.355 | Sedang-Besar |
| RPP | 0.974 | Sangat besar |

Nilai Q² seluruh konstruk endogen positif, menunjukkan model memiliki relevansi prediktif yang baik hingga sangat baik.

---

## 4.7 RM5 — Analisis Mediasi: Efek Tidak Langsung PjBL melalui TPACK, STEM, ESD

**Tabel 12. Efek Tidak Langsung dan Mediasi (Bootstrap 5000 iterasi)**

| Jalur | Estimate | Boot Mean | SE | t | p | CI 2.5% | CI 97.5% | VAF | Tipe Mediasi |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| PjBL → TPACK → RPP | 0.309 | 0.306 | 0.035 | 8.725 | <0.001 | 0.239 | 0.375 | 0.350 | Partial |
| PjBL → STEM → RPP | 0.330 | 0.333 | 0.033 | 10.039 | <0.001 | 0.271 | 0.401 | 0.374 | Partial |
| PjBL → ESD → RPP | 0.213 | 0.209 | 0.031 | 6.685 | <0.001 | 0.151 | 0.275 | 0.241 | Partial |
| Total indirect | 0.852 | 0.847 | 0.040 | 21.016 | <0.001 | 0.769 | 0.928 | — | — |
| Direct effect | 0.030 | 0.034 | 0.045 | 0.770 | 0.441 | -0.055 | 0.123 | — | — |
| Total effect | 0.882 | 0.882 | 0.021 | 42.952 | <0.001 | 0.838 | 0.917 | — | — |

**Cross-check Sobel Test:**

| Jalur Mediasi | z Sobel | p Sobel |
|---|---:|---:|
| PjBL → TPACK → RPP | 8.686 | <0.001 |
| PjBL → STEM → RPP | 9.052 | <0.001 |
| PjBL → ESD → RPP | 6.335 | <0.001 |

![Figur 5. Jalur Mediasi PjBL → Dimensi → RPP](../outputs/rm2_rm5/fig5_sem_mediation_paths.png)

**Interpretasi RM5:**

1. Ketiga jalur mediasi spesifik (melalui TPACK, STEM, dan ESD) signifikan dan konsisten antara bootstrap percentile CI serta uji Sobel.

2. Jalur mediasi terbesar berasal dari STEM (indirect β = 0,330), diikuti TPACK (β = 0,309) dan ESD (β = 0,213).

3. Total indirect effect sangat signifikan, sementara direct effect PjBL -> RPP tidak signifikan. Pola ini menunjukkan **full mediation secara agregat**: pengaruh PjBL terhadap kualitas RPP terutama bekerja melalui peningkatan dimensi integrasi.

---

## 4.8 Ringkasan Model Struktural

| Komponen | Temuan |
|---|---|
| **RM2** | PjBL -> TPACK, STEM, dan ESD semuanya signifikan |
| **RM3** | Urutan responsivitas: TPACK > STEM > ESD |
| **RM4** | STEM, TPACK, ESD berkontribusi signifikan ke RPP; direct PjBL -> RPP tidak signifikan |
| **RM5** | Full mediation secara agregat; jalur mediasi terbesar melalui STEM |
| **GoF** | R² RPP = 0.977; Q² RPP = 0.974 |

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
