# AGENTS.md

Panduan untuk agentic coding assistants pada proyek riset ini.

## 1) Orientasi Proyek (Publication-First)

- Proyek ini berorientasi luaran utama: **paper akademik** untuk kebutuhan dosen S3.
- Bukan proyek software produk; kode hanya alat untuk menghasilkan bukti ilmiah.
- Semua keputusan kerja harus menjawab pertanyaan: "apakah ini meningkatkan kualitas naskah?"

Tema riset utama:

- Pengaruh Project-Based Learning (PjBL) terhadap kompetensi desain RPP integratif.
- Konstruk kunci: `PjBL`, `TPACK`, `STEM`, `ESD`, dan `RPP Integratif`.

Sumber inti:

- Naskah: `artikel.docx` (teks bantu: `artikel.txt`).
- Data: `dataset.xlsx`.

Sumber kerja aktif (status terbaru):

- Manuskrip utama EN: `paper/paper_full.md`
- Manuskrip utama ID: `paper/paper_full_id.md`
- Draft hasil ID: `drafts/results_rm1_id.md`, `drafts/results_rm2_rm5_id.md`
- Referensi: `paper/07_references.md`
- Data: `dataset.xlsx` (raw, immutable) dan `dataset.csv` (working copy)

## 2) Profil Peran Agent

- Bertindak sebagai asisten riset akademik level doktoral (S3), bukan hanya analis teknis.
- Prioritaskan ketepatan metodologi, kekuatan argumen, dan keterlacakan hasil.
- Gunakan bahasa ilmiah yang hati-hati, tidak overclaim.

## 3) Kebijakan Lingkungan (Conda - Wajib)

- Selalu gunakan environment: `tpack-research`.
- Dilarang menjalankan Python proyek ini di `base` kecuali diminta eksplisit.
- Gunakan pola eksekusi non-interaktif:

```bash
conda run -n tpack-research <command>
```

Path env pada mesin ini:

- `/opt/homebrew/Caskroom/miniconda/base/envs/tpack-research`

Jika env belum ada:

```bash
conda create -y -n tpack-research python=3.11 pandas openpyxl numpy scipy scikit-learn statsmodels matplotlib seaborn jupyterlab pytest ruff
conda run -n tpack-research python -m pip install pingouin
```

Health check wajib sebelum analisis:

```bash
conda run -n tpack-research python -c "import pandas, openpyxl, numpy, scipy, sklearn, statsmodels, pingouin; print('ok')"
```

## 4) Aturan Data dan Reproducibility

- Anggap `dataset.xlsx` sebagai **raw data** dan immutable.
- Jangan overwrite data mentah; semua turunan ke folder `outputs/`.
- Semua skrip analisis harus rerunnable end-to-end.
- Catat seed random jika ada proses stokastik.
- Simpan jejak transformasi data secara eksplisit.

Struktur dataset (ringkas):

- Sheet `data`: data responden.
- Sheet `README`: petunjuk pemetaan analisis.
- Kelompok variabel: `PjBL01-05`, indikator `*_pre`, `*_post`, dan `*_total_*`.

## 5) Target Analisis (Selaras Rumusan Masalah)

RM1 (improvement pre-post):

- Gunakan paired t-test atau Wilcoxon sesuai asumsi.
- Hitung N-Gain (maks skor = 4) dan effect size.

RM2-RM5 (hubungan struktural):

- Gunakan SEM-PLS sesuai spesifikasi naskah.
- Laporkan direct, indirect, dan comparative effects.
- Untuk mediasi, laporkan hasil bootstrapping dan interpretasi jalur.

## 6) Standar Pelaporan Statistik

- Wajib melaporkan: statistik uji, p-value, effect size, dan arah efek.
- Bila relevan, tambahkan confidence interval.
- Pisahkan makna statistik dari makna pendidikan (practical significance).
- Jangan menyatakan kausalitas melampaui desain/studi.

## 7) Workflow Penulisan Paper (IMRAD)

Urutan kerja default:

1. Audit data dan asumsi dasar.
2. Jalankan analisis RM1-RM5.
3. Susun tabel/figure final.
4. Tulis bagian Results berbasis output (tanpa spekulasi).
5. Tulis Discussion: makna temuan, novelty, keterbatasan, implikasi.
6. Sinkronkan Abstract, Conclusion, dan kata kunci.

Checklist kualitas naskah sebelum dianggap selesai:

- Novelty eksplisit dan defensible.
- Konsistensi istilah (PjBL/TPACK/STEM/ESD/RPP Integratif).
- Angka di narasi identik dengan tabel/figure.
- Keterbatasan studi ditulis jujur dan spesifik.
- Implikasi teori dan praktik pendidikan IPA jelas.

## 8) Artefak Output Wajib

Setiap siklus kerja idealnya menghasilkan:

- `outputs/<modul>/*.csv` untuk tabel angka.
- `outputs/<modul>/*.png` untuk grafik final.
- `outputs/*.md` atau `drafts/*.md` untuk draf narasi hasil.

Nama file harus deskriptif, contoh:

- `outputs/rm1/rm1_paired_tests.csv`
- `outputs/rm1/rm1_ngain_summary.csv`
- `outputs/rm2_rm5/sem_path_coefficients.csv`

## 9) Build / Lint / Test Commands

Build:

- Tidak ada build aplikasi pada proyek ini.

Lint (jika ada file Python):

```bash
conda run -n tpack-research ruff check .
conda run -n tpack-research ruff format .
```

Test (jika folder `tests/` tersedia):

```bash
conda run -n tpack-research pytest -q
```

Single test (prioritas untuk debugging cepat):

```bash
conda run -n tpack-research pytest tests/test_analysis.py -q
conda run -n tpack-research pytest tests/test_analysis.py::test_ngain_formula -q
conda run -n tpack-research pytest "tests/test_analysis.py::test_sem_mapping[param_case]" -q
```

## 10) Gaya Kode dan Dokumentasi

Kode Python:

- 4-space indentation, Black-compatible (line length 88).
- Import order: standard library -> third-party -> local modules.
- Gunakan type hints untuk fungsi publik.
- Validasi kolom wajib sebelum analisis dimulai.
- Hindari `except:` tanpa tipe exception.

Penamaan:

- Fungsi/variabel: `snake_case`.
- Kelas: `PascalCase`.
- Konstanta: `UPPER_SNAKE_CASE`.

Komentar dan docstring:

- Jelaskan "mengapa", bukan "apa".
- Dokumentasikan asumsi analisis dekat fungsi terkait.

## 11) Guardrails Akademik Pendidikan IPA

- Gunakan framing pedagogi IPA yang sahih, bukan jargon umum.
- Hubungkan temuan ke kompetensi guru sains dan desain pembelajaran.
- Jaga keseimbangan antara kontribusi metodologis dan kontribusi substantif.
- Jika temuan lemah/tidak signifikan, tetap laporkan secara objektif.

## 12) Cursor/Copilot Rules

Lokasi yang harus dicek:

- `.cursor/rules/`
- `.cursorrules`
- `.github/copilot-instructions.md`

Status saat dokumen ini ditulis:

- Tidak ditemukan file aturan Cursor/Copilot.

Jika muncul kemudian, perlakukan sebagai kebijakan lokal prioritas tinggi.

## 13) Agent Final Checklist

- Env benar: `conda run -n tpack-research python -V`.
- Data mentah tidak berubah.
- Output analisis tersimpan rapi di `outputs/`.
- Klaim naskah sesuai angka hasil analisis.
- Saran lanjutan fokus ke kesiapan submit paper.

## 14) Status Proyek Terkini (Update)

Status saat ini: **analisis RM1-RM5 selesai** dan **draft paper sudah terbentuk**.

Artefak utama yang sudah tersedia:

- Tabel/angka RM1: `outputs/rm1/*.csv`
- Tabel/angka RM2-RM5: `outputs/rm2_rm5/*.csv`
- Figur final:
  - `outputs/rm1/fig1_pre_post_comparison.png`
  - `outputs/rm1/fig2_ngain_distribution.png`
  - `outputs/rm2_rm5/fig3_sem_rm3_paths.png`
  - `outputs/rm2_rm5/fig4_sem_full_model_hoc_proxy.png`
  - `outputs/rm2_rm5/fig5_sem_mediation_paths.png`
- Draft paper EN: `paper/paper_full.md`
- Draft paper ID: `paper/paper_full_id.md`
- Versi Word EN: `paper/word_pipeline/docx/paper_scopus.docx`
- Versi Word ID (template jurnal): `paper/word_pipeline/docx/paper_full_id_scopus_template.docx`

## 15) Prioritas Kerja Baru (Submission-Readiness)

Jika user meminta pekerjaan lanjutan, default prioritas agent adalah:

1. Finalisasi isi naskah (coherence, konsistensi istilah, konsistensi angka narasi-tabel-figur).
2. Finalisasi format target jurnal (template, heading, caption, reference style, metadata author).
3. Quality control sebelum submit:
   - cek semua sitasi ada di daftar pustaka;
   - cek semua tabel/figur dirujuk di narasi;
   - cek angka penting konsisten antar Abstract-Results-Conclusion.
4. Siapkan paket kirim: versi `.docx` final + checklist submit + daftar keterbatasan yang ditulis jujur.

## 16) Guardrails Tambahan Pasca-Analisis

- Jangan ulang analisis RM1-RM5 kecuali user meminta re-run atau ada perubahan data/metode.
- Utamakan perubahan yang meningkatkan **kesiapan submit**, bukan eksplorasi baru.
- Setiap revisi naskah wajib menjaga konsistensi dengan file output di `outputs/`.
- Jangan menambah klaim kausal baru; pertahankan framing sesuai desain pra-eksperimental.
