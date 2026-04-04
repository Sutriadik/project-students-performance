# Proyek Akhir: Menyelesaikan Permasalahan Institusi Pendidikan

- **Nama:** Sutriadi Kurniawan
- **Email:** sutriadik@gmail.com
- **ID Dicoding:** sutriadi_kurniawan

---

## Business Understanding

### Latar Belakang Bisnis

Jaya Jaya Institut adalah institusi pendidikan perguruan tinggi yang berdiri sejak tahun 2000. Meskipun telah mencetak banyak lulusan, institusi ini menghadapi masalah serius berupa tingginya angka **dropout** mahasiswa (32.1%). Dropout yang tinggi berdampak pada reputasi institusi, efisiensi anggaran, dan kualitas lulusan secara keseluruhan.

### Permasalahan Bisnis

1. Faktor apa yang paling memengaruhi siswa untuk dropout?
2. Bisakah kita memprediksi siswa yang berisiko dropout sedini mungkin?
3. Intervensi apa yang dapat dilakukan untuk mengurangi angka dropout?

### Cakupan Proyek

- Analisis data siswa dengan pendekatan CRISP-DM
- Business dashboard interaktif berbasis Streamlit (`dashboard.py`)
- Model ML prediksi dropout binary: **Dropout vs Graduate** (`app.py`)
- Deployment ke Streamlit Community Cloud

### Persiapan

**Sumber data:** [students_performance](https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/README.md)

**Setup environment:**

```bash
# Python yang digunakan: Python 3.11
# Buat virtual environment
python3 -m venv venv
source venv/bin/activate       # macOS/Linux
# venv\Scripts\activate        # Windows

# Install semua dependencies
pip install -r requirements.txt
```

**Menjalankan Notebook:**
```bash
# Buka di VS Code
code notebook.ipynb

# Pilih kernel → venv → Run All
# Model tersimpan otomatis di folder model/
```

---

## Business Dashboard

Dashboard monitoring performa siswa menggunakan **Streamlit**.

**Menjalankan Dashboard (lokal):**
```bash
streamlit run dashboard.py
```

**Dashboard online:**
> 🔗 **https://project-students-performance-dashboard.streamlit.app/**

---

## Menjalankan Prototype Machine Learning

**Lokal:**
```bash
streamlit run app.py
```

**Online (Streamlit Community Cloud):**
> 🔗 **https://project-students-performance-prediction.streamlit.app/**

Isi form data akademik dan demografis siswa, lalu klik **Prediksi**.
Hasil prediksi: **Dropout** atau **Graduate**.

---

## Conclusion

### 1. Faktor-faktor Penyebab Dropout (EDA & Dashboard)

| # | Faktor | Temuan |
|---|--------|--------|
| 1 | **Nilai Semester 1 & 2** | Dropout mendekati nilai 0, Graduate berkisar 12–14 |
| 2 | **MK Lulus Semester 1 & 2** | Dropout lulus 0–2 MK, Graduate lulus 5–6 MK |
| 3 | **Status SPP** | SPP belum lunas → ~70% dropout, hanya ~8% graduate |
| 4 | **Status Beasiswa** | Penerima beasiswa memiliki dropout rate lebih rendah |
| 5 | **Usia saat Mendaftar** | Usia 26–30 dan 41+ memiliki dropout rate tertinggi |
| 6 | **Status Hutang** | Siswa berhutang memiliki risiko dropout lebih tinggi |
| 7 | **Gender** | Laki-laki dropout ~45%, perempuan ~25% |

### 2. Performa Model Machine Learning

Model binary classification **Dropout vs Graduate** (Enrolled dikecualikan dari training).

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|:--------:|:---------:|:------:|:--------:|
| **Random Forest** ⭐ | **0.9091** | **0.8933** | 0.9661 | **0.9283** |
| Decision Tree | 0.8939 | 0.8875 | 0.9457 | 0.9157 |
| Logistic Regression | 0.9105 | 0.8903 | **0.9729** | 0.9297 |

**Random Forest dipilih** karena memiliki keseimbangan terbaik antara Accuracy (90.91%), Precision (89.33%), dan F1-Score (92.83%).

**Top 5 Feature Importance (Random Forest):**
1. `Sem2_approval_rate` — rasio MK lulus Semester 2
2. `Total_approved` — total MK lulus kedua semester
3. `Curricular_units_2nd_sem_approved` — jumlah MK lulus Sem 2
4. `Avg_grade` — nilai rata-rata kedua semester
5. `Curricular_units_2nd_sem_grade` — nilai rata-rata Semester 2

### Rekomendasi Action Items

1. **Bimbingan Akademik Dini** — Siswa dengan nilai Sem 1 rendah atau MK lulus < 3 segera diberi pendampingan intensif
2. **Fleksibilitas Pembayaran SPP** — Skema cicilan bagi siswa yang kesulitan keuangan
3. **Perluasan Program Beasiswa** — Terbukti menurunkan dropout rate secara signifikan
4. **Early Warning System** — Monitoring bulanan; prob dropout ≥ 60% → bimbingan khusus
5. **Program Mentoring** — Khusus mahasiswa baru usia lebih tua dan mahasiswa laki-laki

---

## Struktur Proyek

```
submission project/
├── model/
│   ├── model.joblib
│   ├── scaler.joblib
│   ├── label_encoder.joblib
│   └── feature_names.joblib
├── .streamlit/
│   └── config.toml
├── notebook.ipynb
├── app.py
├── dashboard.py
├── README.md
├── requirements.txt
├── data.csv
└── sutriadik24-dashboard.png
```