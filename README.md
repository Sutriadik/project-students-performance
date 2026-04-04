# Proyek Akhir: Menyelesaikan Permasalahan Institusi Pendidikan

- **Nama:** Sutriadi kurniawan
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
- Model ML untuk prediksi risiko dropout (`app.py`)
- Deployment ke Streamlit Community Cloud

### Persiapan

**Sumber data:** [students_performance](https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/README.md)

**Setup environment:**
```bash
pip install -r requirements.txt
```

**Menjalankan Notebook:**
```bash
# Buka notebook.ipynb di VS Code / Jupyter
# Pilih kernel → Run All
# Model tersimpan otomatis di folder model/
```

---

## Business Dashboard

Dashboard monitoring performa siswa dibuat menggunakan **Streamlit**.

**Menjalankan Dashboard (lokal):**
```bash
streamlit run dashboard.py
# Buka: http://localhost:8501
```

Konten dashboard (14 visualisasi):
- KPI Overview (Total, Dropout rate, Graduate rate, Avg Nilai Sem 1 & 2)
- Distribusi status siswa & dropout per program studi
- Performa akademik semester 1 & 2
- Faktor keuangan (SPP, beasiswa, hutang)
- Profil demografi (usia, nilai masuk)
- Analisis gender & jadwal kehadiran
- Faktor risiko dropout & feature importance
- Critical Academic Warning (success rate < 50%)
- Tren progression akademik
- Demografi usia & marital status
- Dropout rate per nationality

---

## Menjalankan Prototype Machine Learning

**Lokal:**
```bash
streamlit run app.py
# Buka: http://localhost:8501
```

**Online (Streamlit Community Cloud):**
> 🔗 **https://project-students-performance-prediction.streamlit.app/**

Isi form data akademik dan demografis siswa, lalu klik **Prediksi** untuk mengetahui risiko dropout.

---

## Conclusion

### Faktor Utama Penyebab Dropout

| # | Faktor | Temuan |
|---|--------|--------|
| 1 | **Nilai Semester 1 & 2** | Nilai rendah di awal studi adalah prediktor dropout terkuat |
| 2 | **Mata Kuliah Lulus** | Sedikit MK yang lulus → risiko dropout sangat tinggi |
| 3 | **Status Pembayaran SPP** | Mahasiswa yang menunggak SPP memiliki dropout rate jauh lebih tinggi |
| 4 | **Status Beasiswa** | Penerima beasiswa memiliki dropout rate lebih rendah |
| 5 | **Usia saat Mendaftar** | Mahasiswa yang mendaftar di usia lebih tua lebih berisiko |
| 6 | **Status Hutang** | Mahasiswa dengan hutang memiliki risiko dropout lebih tinggi |

### Rekomendasi Action Items

1. **Program Bimbingan Akademik Dini** — Siswa dengan nilai semester 1 rendah segera diberi tutoring dan pendampingan intensif
2. **Fleksibilitas Pembayaran SPP** — Buat skema cicilan atau keringanan bagi siswa yang mengalami kesulitan keuangan
3. **Perluasan Program Beasiswa** — Perbanyak beasiswa karena terbukti menurunkan dropout rate secara signifikan
4. **Early Warning System** — Gunakan model prediksi untuk monitoring bulanan; siswa dengan probabilitas dropout ≥ 60% segera diberi bimbingan khusus
5. **Program Orientasi & Mentoring** — Khusus untuk mahasiswa baru, terutama yang mendaftar di usia lebih tua

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