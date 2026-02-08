## 4. Hasil

### 4.1 Statistik Deskriptif

Sebelum pengujian hipotesis, kami memeriksa statistik deskriptif untuk seluruh konstruk. Tabel 1 menyajikan rata-rata dan simpangan baku tingkat konstruk pada pretest dan posttest, sementara Gambar 1 memberikan perbandingan visual.

**Tabel 1.** Statistik Deskriptif per Konstruk (Pretest vs Posttest)

| Konstruk | $N$ | Pre $M$ | Pre $SD$ | Post $M$ | Post $SD$ | $M_{\text{diff}}$ |
|---|---|---|---|---|---|---|
| TPACK | 95 | 2,306 | 0,390 | 3,319 | 0,294 | 1,013 |
| STEM | 95 | 2,172 | 0,393 | 3,222 | 0,378 | 1,051 |
| ESD | 95 | 1,929 | 0,328 | 2,726 | 0,259 | 0,798 |
| RPP Integratif | 95 | 2,136 | 0,256 | 3,089 | 0,237 | 0,954 |

*Catatan.* Rentang skala: 1–4. RPP Integratif = rata-rata keseluruhan dari 14 indikator.

Sebagaimana ditunjukkan pada Tabel 1, seluruh konstruk menunjukkan peningkatan substansial setelah intervensi PjBL. Perbedaan rata-rata terbesar diamati pada STEM ($M_{\text{diff}} = 1{,}051$), diikuti TPACK ($M_{\text{diff}} = 1{,}013$), RPP Integratif ($M_{\text{diff}} = 0{,}954$), dan ESD ($M_{\text{diff}} = 0{,}798$).

![Gambar 1. Perbandingan Skor Rata-rata Pre-test vs Post-test per Konstruk](../../outputs/rm1/fig1_pre_post_comparison.png)

*Gambar 1.* Skor rata-rata pre-test vs post-test per konstruk, dengan error bar menunjukkan simpangan baku. Seluruh konstruk menunjukkan peningkatan substansial setelah intervensi PjBL.

### 4.2 RM1: Perubahan Pre-Post

#### Uji Normalitas

Sebelum melakukan perbandingan berpasangan, kami menilai normalitas skor selisih menggunakan uji Shapiro-Wilk. Tabel 2 merangkum hasilnya.

**Tabel 2.** Hasil Uji Normalitas Shapiro-Wilk untuk Skor Selisih

| Konstruk | $W$ | $p$ | Normal |
|---|---|---|---|
| TPACK | 0,968 | ,020 | Tidak |
| STEM | 0,977 | ,088 | Ya |
| ESD | 0,990 | ,704 | Ya |
| RPP Integratif | 0,986 | ,418 | Ya |

Sebagaimana ditunjukkan pada Tabel 2, skor selisih untuk STEM, ESD, dan RPP Integratif terdistribusi normal ($p > {,}05$). Namun, skor selisih TPACK menyimpang signifikan dari normalitas ($W = 0{,}968$, $p = {,}020$). Oleh karena itu, paired-samples t-test diterapkan pada STEM, ESD, dan RPP Integratif, sementara Wilcoxon signed-rank test digunakan untuk TPACK.

#### Uji Berpasangan dan Ukuran Efek

**Tabel 3.** Hasil Uji Berpasangan

| Konstruk | Uji | Statistik | $p$ | Cohen's $d$ | Interpretasi |
|---|---|---|---|---|---|
| TPACK | Wilcoxon | $W = 0{,}0$ | $< {,}001$ | 2,705 | Besar |
| STEM | Paired t | $t(94) = 25{,}90$ | $< {,}001$ | 2,657 | Besar |
| ESD | Paired t | $t(94) = 22{,}79$ | $< {,}001$ | 2,338 | Besar |
| RPP Integratif | Paired t | $t(94) = 40{,}88$ | $< {,}001$ | 4,194 | Besar |

*Catatan.* Wilcoxon $W = 0{,}0$ menunjukkan seluruh partisipan meningkat; Cohen's $d$ untuk TPACK dihitung sebagai rata-rata skor selisih dibagi simpangan baku skor selisih (paired-samples $d_z$).

Sebagaimana ditunjukkan pada Tabel 3, keempat konstruk menunjukkan peningkatan signifikan secara statistik dari pretest ke posttest ($p < {,}001$). Ukuran efek seragam besar, dengan nilai Cohen's $d$ melebihi 2,3 untuk seluruh konstruk.

#### Normalized Gain

Di luar signifikansi statistik dan ukuran efek, kami menghitung normalized gain (N-Gain) untuk mengukur proporsi peningkatan maksimum yang dapat dicapai. Tabel 4 menyajikan ringkasan N-Gain, sementara Gambar 2 memvisualisasikan distribusi kategori gain.

**Tabel 4.** Ringkasan N-Gain

| Konstruk | N-Gain $M$ | $SD$ | Kategori | High (%) | Medium (%) | Low (%) |
|---|---|---|---|---|---|---|
| TPACK | 0,596 | 0,160 | Medium | 26,3 | 72,6 | 1,1 |
| STEM | 0,574 | 0,179 | Medium | 24,2 | 69,5 | 6,3 |
| ESD | 0,376 | 0,129 | Medium | 0,0 | 71,6 | 28,4 |
| RPP Integratif | 0,513 | 0,103 | Medium | 3,2 | 95,8 | 1,1 |

Sebagaimana ditunjukkan pada Tabel 4, seluruh konstruk mencapai kategori Medium gain ($0{,}3$–$0{,}7$). TPACK memperoleh rata-rata N-Gain tertinggi ($M = 0{,}596$), diikuti STEM ($M = 0{,}574$), RPP Integratif ($M = 0{,}513$), dan ESD ($M = 0{,}376$).

![Gambar 2. Distribusi Kategori N-Gain per Konstruk](../../outputs/rm1/fig2_ngain_distribution.png)

*Gambar 2.* Distribusi kategori N-Gain (High, Medium, Low) per konstruk. ESD tidak memiliki partisipan dengan High-gain dan memiliki proporsi Low-gain tertinggi.

Ringkasnya, analisis pre-post (RM1) menunjukkan bahwa PjBL secara signifikan meningkatkan keempat konstruk dengan ukuran efek besar, meskipun ESD menunjukkan gain terkecil. Untuk memahami hubungan struktural antar konstruk ini, kami beralih ke analisis PLS-SEM yang menjawab RM2–RM5.

### 4.3 RM2–RM5: Analisis PLS-SEM

#### Evaluasi Model Pengukuran

Sebelum menguji hipotesis struktural, kami mengevaluasi model pengukuran untuk memastikan reliabilitas dan validitas yang memadai. Tabel 5 menyajikan outer loadings untuk seluruh indikator.

**Tabel 5.** Outer Loadings

| Konstruk | Indikator | Loading | $\geq 0{,}708$ |
|---|---|---|---|
| ESD | ESD-EVA | 0,780 | Ya |
| ESD | ESD-INQ | 0,894 | Ya |
| ESD | ESD-PCK | 0,867 | Ya |
| PjBL | PjBL01 | 0,815 | Ya |
| PjBL | PjBL02 | 0,804 | Ya |
| PjBL | PjBL03 | 0,835 | Ya |
| PjBL | PjBL04 | 0,850 | Ya |
| PjBL | PjBL05 | 0,840 | Ya |
| TPACK | TK | 0,689 | Tidak |
| TPACK | PK | 0,224 | Tidak |
| TPACK | CK | 0,673 | Tidak |
| TPACK | TPK | 0,760 | Ya |
| TPACK | TCK | 0,795 | Ya |
| TPACK | PCK | 0,400 | Tidak |
| TPACK | TPACK_int | 0,759 | Ya |
| STEM | Science | 0,484 | Tidak |
| STEM | Technology | 0,713 | Ya |
| STEM | Engineering | 0,577 | Tidak |
| STEM | Mathematics | 0,916 | Ya |
| RPP | RPPInt_total | 1,000 | Ya |

*Catatan.* Indikator dengan loading antara 0,40 dan 0,70 dipertahankan mengikuti rekomendasi Hair et al. (2022) untuk penelitian eksploratoris.

**Tabel 6.** Reliabilitas Konstruk dan Validitas Konvergen

| Konstruk | AVE | CR | Cronbach's alpha |
|---|---|---|---|
| ESD | 0,720 | 0,886 | 0,807 |
| PjBL | 0,687 | 0,917 | 0,886 |
| RPP | 1,000 | 1,000 | — |
| STEM | 0,480 | 0,814 | 0,694 |
| TPACK | 0,418 | 0,834 | 0,766 |

*Catatan.* Threshold: AVE >= 0,50, CR >= 0,70, alpha >= 0,70. RPP adalah konstruk single-indicator.

**Tabel 6b.** Matriks Heterotrait-Monotrait (HTMT)

| | PjBL | TPACK | STEM | ESD |
|---|---|---|---|---|
| PjBL | — | | | |
| TPACK | 0,837 | — | | |
| STEM | 0,871 | 0,770 | — | |
| ESD | 0,716 | 0,298 | 0,456 | — |

*Catatan.* Seluruh nilai $< 0{,}90$, mendukung validitas diskriminan.

Dengan properti pengukuran yang memadai, kami melanjutkan untuk mengevaluasi model struktural.

#### Model Struktural: Efek Langsung (RM2)

Setelah mengonfirmasi model pengukuran, kami menguji hubungan struktural untuk menjawab RM2. Tabel 7 menyajikan koefisien jalur, statistik bootstrap, dan ukuran efek untuk seluruh jalur langsung.

**Tabel 7.** Model Struktural — Koefisien Jalur dan Signifikansi

| Jalur | $\beta$ | $SE$ | $t$ | $p$ | CI 95% | Sig. | $f^2$ |
|---|---|---|---|---|---|---|---|
| PjBL $\rightarrow$ TPACK | 0,727 | 0,055 | 13,295 | $< {,}001$ | [0,610; 0,823] | Ya | 1,123 (B) |
| PjBL $\rightarrow$ STEM | 0,683 | 0,054 | 12,616 | $< {,}001$ | [0,573; 0,782] | Ya | 0,872 (B) |
| PjBL $\rightarrow$ ESD | 0,617 | 0,065 | 9,496 | $< {,}001$ | [0,485; 0,739] | Ya | 0,614 (B) |
| PjBL $\rightarrow$ RPP | 0,030 | 0,045 | 0,770 | ,441 | [-0,055; 0,123] | Tidak | 0,007 (N) |
| TPACK $\rightarrow$ RPP | 0,425 | 0,037 | 11,346 | $< {,}001$ | [0,345; 0,491] | Ya | 2,783 (B) |
| STEM $\rightarrow$ RPP | 0,484 | 0,037 | 13,116 | $< {,}001$ | [0,412; 0,556] | Ya | 5,444 (B) |
| ESD $\rightarrow$ RPP | 0,345 | 0,040 | 8,355 | $< {,}001$ | [0,264; 0,423] | Ya | 2,399 (B) |

*Catatan.* B = Besar, N = Negligible. Bootstrap: 5.000 iterasi, seed = 42.

Sebagaimana ditunjukkan pada Tabel 7, PjBL memberikan efek positif signifikan terhadap ketiga dimensi integrasi: TPACK ($\beta = 0{,}727$, $p < {,}001$, $f^2 = 1{,}123$), STEM ($\beta = 0{,}683$, $p < {,}001$, $f^2 = 0{,}872$), dan ESD ($\beta = 0{,}617$, $p < {,}001$, $f^2 = 0{,}614$). Seluruh ukuran efek besar. Penting dicatat, jalur langsung dari PjBL ke RPP tidak signifikan ($\beta = 0{,}030$, $p = {,}441$), menunjukkan bahwa PjBL tidak langsung mempengaruhi kualitas RPP tetapi bekerja melalui konstruk mediator.

Model menjelaskan 97,7% varians RPP ($R^2 = 0{,}977$), 52,9% TPACK ($R^2 = 0{,}529$), 46,6% STEM ($R^2 = 0{,}466$), dan 38,0% ESD ($R^2 = 0{,}380$).

Relevansi prediktif ($Q^2$) bernilai positif dan substansial untuk seluruh konstruk endogen: RPP (0,974), TPACK (0,503), STEM (0,430), dan ESD (0,355), menunjukkan kapasitas prediktif yang kuat melampaui prediksi rerata sederhana.

#### Analisis Komparatif: Dimensi Dominan (RM3)

Berdasarkan temuan RM2, RM3 menanyakan dimensi integrasi mana yang paling responsif terhadap PjBL. Tabel 8 membandingkan koefisien jalur PjBL ke dimensi, dan Gambar 3 memvisualisasikan hubungan ini.

**Tabel 8.** RM3 — Perbandingan Koefisien Jalur PjBL ke Dimensi

| Rank | Dimensi | $\beta$ | $t$ | $p$ | $f^2$ | Signifikan |
|---|---|---|---|---|---|---|
| 1 | TPACK | 0,727 | 13,295 | $< {,}001$ | 1,123 | Ya |
| 2 | STEM | 0,683 | 12,616 | $< {,}001$ | 0,872 | Ya |
| 3 | ESD | 0,617 | 9,496 | $< {,}001$ | 0,614 | Ya |

Sebagaimana ditunjukkan pada Tabel 8, TPACK muncul sebagai dimensi paling responsif ($\beta = 0{,}727$, $f^2 = 1{,}123$), diikuti STEM ($\beta = 0{,}683$, $f^2 = 0{,}872$) dan ESD ($\beta = 0{,}617$, $f^2 = 0{,}614$). Seluruh jalur signifikan dengan ukuran efek besar, menghasilkan urutan: TPACK > STEM > ESD.

![Gambar 3. Koefisien Jalur dari PjBL ke Konstruk Mediator](../../outputs/rm2_rm5/fig3_sem_rm3_paths.png)

*Gambar 3.* Koefisien jalur dari PjBL ke setiap dimensi integrasi (TPACK, STEM, ESD). Seluruh jalur signifikan ($p < {,}001$) dengan ukuran efek besar. TPACK paling responsif terhadap PjBL ($\beta = 0{,}727$), diikuti STEM ($\beta = 0{,}683$) dan ESD ($\beta = 0{,}617$).

#### Higher-Order Construct: Dimensi yang Berkontribusi terhadap Kualitas RPP (RM4)

Sementara RM3 menguji efek diferensial PjBL terhadap ketiga dimensi, RM4 fokus pada bagaimana dimensi-dimensi ini berkontribusi terhadap kualitas RPP integratif. Gambar 4 mengilustrasikan model struktural lengkap dengan jalur dari PjBL melalui konstruk mediator ke RPP.

![Gambar 4. Prediktor Kualitas RPP Integratif](../../outputs/rm2_rm5/fig4_sem_full_model_hoc_proxy.png)

*Gambar 4.* Koefisien jalur dari dimensi integrasi ke kualitas RPP. Ketiga dimensi berkontribusi signifikan: STEM ($\beta = 0{,}484$), TPACK ($\beta = 0{,}425$), dan ESD ($\beta = 0{,}345$). Jalur langsung dari PjBL ke RPP tidak signifikan ($\beta = 0{,}030$, garis putus-putus).

Sebagaimana ditunjukkan pada Gambar 4 dan Tabel 7, ketiga dimensi integrasi berkontribusi signifikan dan substansial terhadap kualitas RPP integratif. STEM adalah kontributor terkuat ($\beta = 0{,}484$), diikuti TPACK ($\beta = 0{,}425$) dan ESD ($\beta = 0{,}345$). Nilai $f^2$ yang konsisten besar (seluruh $> 2{,}3$) menunjukkan bahwa setiap dimensi memberikan kontribusi bermakna dan non-redundan terhadap kualitas RPP keseluruhan.

#### Analisis Mediasi (RM5)

Terakhir, RM5 menguji apakah TPACK, STEM, dan ESD memediasi hubungan antara PjBL dan kualitas RPP. Tabel 9 menyajikan hasil analisis mediasi, dan Gambar 5 memvisualisasikan efek tidak langsung spesifik.

**Tabel 9.** Analisis Mediasi — Efek Tidak Langsung

| Jalur Tidak Langsung | $\beta_{\text{indirect}}$ | $SE$ | $t$ | $p$ | CI 95% | VAF | Sobel $z$ | Sobel $p$ |
|---|---|---|---|---|---|---|---|---|
| PjBL $\rightarrow$ TPACK $\rightarrow$ RPP | 0,309 | 0,035 | 8,725 | $< {,}001$ | [0,239; 0,375] | 35,0% | 8,686 | $< {,}001$ |
| PjBL $\rightarrow$ STEM $\rightarrow$ RPP | 0,330 | 0,033 | 10,039 | $< {,}001$ | [0,271; 0,401] | 37,4% | 9,052 | $< {,}001$ |
| PjBL $\rightarrow$ ESD $\rightarrow$ RPP | 0,213 | 0,031 | 6,685 | $< {,}001$ | [0,151; 0,275] | 24,1% | 6,335 | $< {,}001$ |
| Total indirect | 0,852 | 0,040 | 21,016 | $< {,}001$ | [0,769; 0,928] | — | — | — |
| Langsung (PjBL $\rightarrow$ RPP) | 0,030 | 0,045 | 0,770 | ,441 | [-0,055; 0,123] | — | — | — |
| Total effect | 0,882 | 0,021 | 42,952 | $< {,}001$ | [0,838; 0,917] | — | — | — |

Sebagaimana ditunjukkan pada Tabel 9, ketiga jalur tidak langsung signifikan secara statistik berdasarkan confidence interval bootstrap:

- **PjBL $\rightarrow$ STEM $\rightarrow$ RPP** adalah jalur mediasi terkuat (indirect $\beta = 0{,}330$, $p < {,}001$, CI 95% [0,271; 0,401]). VAF 37,4% menunjukkan mediasi parsial, dan uji Sobel mengonfirmasi signifikansi ($z = 9{,}052$, $p < {,}001$).
- **PjBL $\rightarrow$ TPACK $\rightarrow$ RPP** menghasilkan efek tidak langsung signifikan (indirect $\beta = 0{,}309$, $p < {,}001$, CI 95% [0,239; 0,375]). VAF 35,0% konsisten dengan mediasi parsial.
- **PjBL $\rightarrow$ ESD $\rightarrow$ RPP** juga signifikan (indirect $\beta = 0{,}213$, $p < {,}001$, CI 95% [0,151; 0,275]). VAF 24,1% menunjukkan mediasi parsial.

![Gambar 5. Efek Tidak Langsung Spesifik melalui Konstruk Mediator](../../outputs/rm2_rm5/fig5_sem_mediation_paths.png)

*Gambar 5.* Efek tidak langsung spesifik PjBL terhadap RPP melalui setiap konstruk mediator. STEM memediasi porsi terbesar ($\beta_{\text{indirect}} = 0{,}330$), diikuti TPACK ($\beta_{\text{indirect}} = 0{,}309$) dan ESD ($\beta_{\text{indirect}} = 0{,}213$). Seluruh jalur tidak langsung signifikan ($p < {,}001$).

Total indirect effect signifikan ($\beta = 0{,}852$, $p < {,}001$), sementara direct effect PjBL terhadap RPP tidak signifikan ($\beta = 0{,}030$, $p = {,}441$). Pola ini konsisten dengan full mediation secara agregat: PjBL mempengaruhi kualitas RPP integratif bukan secara langsung, tetapi melalui peningkatan ketiga dimensi integrasi. Total effect PjBL terhadap RPP signifikan ($\beta = 0{,}882$, $p < {,}001$), mengonfirmasi bahwa pengaruh keseluruhan PjBL terhadap kualitas RPP substansial dan bekerja melalui dimensi mediator.
