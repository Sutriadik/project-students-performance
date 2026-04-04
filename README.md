# Proyek Akhir: Menyelesaikan Permasalahan Institusi Pendidikan

## Business Understanding

Jaya Jaya Institut merupakan institusi pendidikan perguruan yang telah berdiri sejak tahun 2000 dan telah mencetak banyak lulusan dengan reputasi yang sangat baik. Namun, institusi ini menghadapi tantangan serius berupa tingginya angka siswa yang tidak menyelesaikan pendidikannya (dropout). Dari total 4424 siswa, sebanyak 1421 siswa (32.1%) mengalami dropout. Hal ini berdampak negatif terhadap reputasi dan efektivitas institusi dalam menjalankan misinya.

### Permasalahan Bisnis

1. Tingginya angka dropout siswa (32.1%) yang berdampak pada reputasi dan keberlanjutan institusi.
2. Belum adanya sistem deteksi dini yang dapat mengidentifikasi siswa yang berpotensi dropout sejak awal.
3. Pihak institusi belum memiliki dashboard untuk memonitor performa siswa secara visual dan real-time.
4. Kurangnya pemahaman mendalam tentang faktor-faktor utama yang menyebabkan siswa dropout.

### Cakupan Proyek

1. Analisis data untuk mengidentifikasi faktor-faktor yang mempengaruhi dropout siswa.
2. Pembangunan model machine learning untuk memprediksi status siswa (Dropout, Enrolled, Graduate).
3. Pembuatan business dashboard menggunakan Streamlit untuk memonitor performa siswa.
4. Pembuatan prototype sistem prediksi berbasis Streamlit yang di-deploy pada Streamlit Community Cloud.
5. Penyusunan rekomendasi action items berdasarkan hasil analisis.

### Persiapan

Sumber data: [students' performance dataset](https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/README.md)

Setup environment:

```bash
# Clone repository
git clone <repository-url>
cd submission

# Install dependencies
pip install -r requirements.txt
```

## Business Dashboard

Business dashboard dibuat menggunakan **Streamlit** untuk membantu Jaya Jaya Institut memahami data dan memonitor performa siswa. Dashboard ini menampilkan:

1. **Metrik utama**: Total siswa, jumlah dan persentase Graduate, Dropout, dan Enrolled.
2. **Distribusi status siswa**: Visualisasi bar chart jumlah siswa per status.
3. **Dropout rate per course**: Identifikasi program studi dengan tingkat dropout tertinggi.
4. **Performa akademik**: Perbandingan unit kurikulum yang disetujui di semester 1 dan 2 berdasarkan status siswa.
5. **Faktor finansial**: Pengaruh pembayaran SPP dan beasiswa terhadap status siswa.
6. **Faktor demografis**: Distribusi usia pendaftaran dan pengaruh gender terhadap status siswa.
7. **Filter interaktif**: Sidebar filter untuk Status, Gender, dan Beasiswa.

Cara menjalankan dashboard:

```bash
streamlit run dashboard.py
```

## Menjalankan Sistem Machine Learning

Prototype sistem machine learning dibuat menggunakan Streamlit yang memungkinkan pengguna memasukkan data siswa dan mendapatkan prediksi status (Dropout / Enrolled / Graduate) beserta probabilitasnya.

Cara menjalankan secara lokal:

```bash
streamlit run app.py
```

Link prototype (Streamlit Community Cloud): **[masukkan link setelah deploy]**

## Conclusion

Berdasarkan analisis yang telah dilakukan, berikut adalah kesimpulan dari proyek ini:

1. **Faktor akademik** merupakan prediktor paling kuat terhadap status siswa. Jumlah unit kurikulum yang disetujui dan nilai rata-rata di semester 1 dan 2 menjadi fitur terpenting dalam memprediksi dropout.
2. **Faktor finansial** juga berpengaruh signifikan. Siswa yang membayar SPP tepat waktu dan penerima beasiswa memiliki tingkat kelulusan yang lebih tinggi.
3. **Usia saat pendaftaran** berhubungan dengan risiko dropout. Siswa yang mendaftar di usia lebih tua cenderung lebih berisiko dropout.
4. Model machine learning berhasil dibangun dan mampu memprediksi status siswa dengan akurasi yang baik, sehingga dapat digunakan sebagai sistem deteksi dini dropout.

### Rekomendasi Action Items

Berikut rekomendasi yang dapat dilakukan Jaya Jaya Institut untuk mengurangi angka dropout:

- **Action item 1: Sistem peringatan dini berbasis akademik.** Implementasikan monitoring otomatis terhadap performa siswa di akhir semester 1. Siswa dengan unit disetujui dan nilai di bawah rata-rata perlu segera diberikan bimbingan akademik intensif.
- **Action item 2: Program bantuan finansial yang lebih proaktif.** Perluas program beasiswa dan keringanan SPP, terutama bagi siswa yang teridentifikasi berisiko dropout karena faktor finansial (debitur, SPP tidak lancar).
- **Action item 3: Mentoring khusus untuk siswa berisiko tinggi.** Sediakan program mentoring atau tutoring khusus bagi siswa yang masuk kategori berisiko berdasarkan prediksi model, terutama di semester awal perkuliahan.
- **Action item 4: Evaluasi dan perbaikan program studi.** Lakukan evaluasi mendalam terhadap program studi dengan dropout rate tertinggi untuk mengidentifikasi dan memperbaiki faktor penyebab spesifik pada masing-masing program.
