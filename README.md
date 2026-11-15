# Bike Sharing Data Analysis

Proyek analisis data penyewaan sepeda (Bike Sharing Dataset) untuk periode 2011–2012. Proyek mencakup data wrangling, EDA, visualisasi, analisis lanjutan dengan binning suhu, serta dashboard Streamlit.

## Struktur folder

```text
.
├── data/
│   ├── day.csv
│   └── hour.csv
├── dashboard/
│   ├── dashboard.py
│   ├── day_data.csv
│   └── main_data.csv
├── notebook.ipynb
├── requirements.txt
├── README.md
└── url.txt
```

## Menjalankan secara lokal

Disarankan menggunakan Python 3.10 atau lebih baru.

1. Buat dan aktifkan virtual environment (opsional tetapi disarankan).
2. Instal dependensi:

   ```bash
   pip install -r requirements.txt
   ```

3. Jalankan notebook dari root folder:

   ```bash
   jupyter notebook notebook.ipynb
   ```

   Pastikan notebook dijalankan dari direktori root agar folder `data/` ditemukan. Notebook akan membuat file CSV bersih di folder `dashboard/`.

4. Jalankan dashboard:

   ```bash
   streamlit run dashboard/dashboard.py
   ```

Dashboard juga memiliki fallback untuk membaca file mentah di folder `data/` jika CSV hasil cleaning belum dibuat.

## Dataset

Bike Sharing Dataset, berisi `day.csv` (agregasi harian) dan `hour.csv` (agregasi per jam). Sumber dataset: [Kaggle - Bike Sharing Dataset](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset).

## Pertanyaan analisis

1. Bagaimana perbedaan pola penyewaan per jam antara hari kerja dan akhir pekan/libur?
2. Bagaimana variasi permintaan antar musim dan kategori cuaca?
3. Sebagai analisis tambahan, bagaimana distribusi permintaan pada kelompok suhu ternormalisasi?

## Catatan

- Ganti identitas pada bagian awal notebook dengan identitas Anda sendiri.
- Hasil analisis merupakan eksplorasi deskriptif. Hubungan antarvariabel tidak otomatis menunjukkan hubungan sebab-akibat.
- Sebelum submission, jalankan ulang seluruh cell notebook dan cek dashboard pada browser lokal.
