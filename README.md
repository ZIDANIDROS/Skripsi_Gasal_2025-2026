# Market Basket Analysis Menggunakan Algoritma Apriori

Sistem ini merupakan aplikasi berbasis web yang digunakan untuk melakukan **Market Basket Analysis (MBA)** menggunakan algoritma Apriori untuk menentukan strategi bundling produk pada CV ALBA.

Aplikasi dibangun menggunakan framework Flask dan bahasa pemrograman Python.

---

## 📌 Fitur Sistem

- Upload data transaksi dalam format `.xlsx`
- Proses analisis menggunakan algoritma Apriori
- Menampilkan nilai:
  - Support
  - Confidence
  - Lift
- Menampilkan hasil aturan asosiasi
- Menyediakan kesimpulan rekomendasi bundling produk

---

## 📂 Struktur Project

```
skripsi/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data_processing/
│   ├── __init__.py
│   └── apriori_logic.py
│
├── templates/
│   ├── index.html
│   ├── data.html
│   ├── proses.html
│   ├── hasil.html
│   └── kesimpulan.html
│
├── static/
└── uploads/
```

---

## 🛠️ Persyaratan Sistem

- Python 3.10 atau lebih baru
- Pip (Python Package Manager)

---

## 🚀 Tahapan Instalasi dan Menjalankan Aplikasi

### 1️⃣ Clone Repository

```bash
git clone https://github.com/username/nama-repository.git
```

Masuk ke folder project:

```bash
cd nama-repository
```

---

### 2️⃣ Membuat Virtual Environment

```bash
python -m venv venv
```

Aktifkan virtual environment:

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

Jika berhasil, akan muncul `(venv)` pada terminal.

---

### 3️⃣ Install Dependencies

Install seluruh library yang dibutuhkan:

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Menjalankan Aplikasi

```bash
python app.py
```

Jika berhasil, akan muncul:

```
Running on http://127.0.0.1:5000
```

Buka browser dan akses:

```
http://127.0.0.1:5000
```

---

## 📊 Cara Menggunakan Aplikasi

1. Buka halaman utama.
2. Upload file data transaksi (.xlsx).
3. Klik tombol proses analisis.
4. Sistem akan menampilkan:
   - Frequent itemset
   - Association rules
   - Nilai support, confidence, dan lift
5. Lihat halaman kesimpulan untuk rekomendasi bundling produk.

---

## 📦 Library yang Digunakan

- Flask
- Pandas
- NumPy
- Mlxtend
- Openpyxl

---

## 📄 Lisensi

Project ini dibuat untuk keperluan penelitian skripsi.
