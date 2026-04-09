# 🏪 Warung Sejahtera Inventory System

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 📋 Deskripsi Proyek
Proyek ini adalah hasil implementasi **SDLC Waterfall** dari A sampai Z untuk memenuhi kebutuhan **IT Analyst Portfolio**. 
Aplikasi ini berfungsi sebagai sistem kasir dan manajemen stok sederhana untuk toko kelontong "Warung Sejahtera".

**Tujuan Bisnis:** Membantu pemilik warung memantau stok barang, mengurangi kerugian akibat barang kadaluarsa, dan mempercepat proses transaksi penjualan.

## 🛠 Tech Stack
- **Frontend/Backend:** Streamlit (Python)
- **Data Storage:** CSV (Pandas)
- **Deployment:** Streamlit Community Cloud

## ✨ Fitur Utama
- **Dashboard:** Menampilkan total produk, total nilai modal, dan peringatan stok menipis.
- **Manajemen Produk:** Tambah, Edit, Hapus data barang (Harga Beli, Jual, Stok, Expired).
- **Kasir Penjualan:** Input penjualan otomatis mengurangi stok dan menampilkan total harga.

## 📁 Struktur Proyek (Analisis SDLC)
1. **Fase Planning:** [Project Charter](/docs/Project_Charter.md)
2. **Fase Analysis:** [BRD & User Stories](/docs/02_BRD_Analysis.md) | [BPMN Diagram](/docs/diagram_alur.png)
3. **Fase Design:** [Data Dictionary](/docs/03_Design_Database.md) | [Wireframe](/docs/wireframe.png)
4. **Fase Development:** `app.py`
5. **Fase Testing:** Manual Test Case (Lihat dokumentasi)

## 🚀 Cara Menjalankan di Lokal
```bash
# Clone repo
git clone https://github.com/[USERNAME_LO]/warung-sejahtera-app.git
cd warung-sejahtera-app

# Buat virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Jalankan
streamlit run app.py