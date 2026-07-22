# SmartTranslate NLP

Sistem Penerjemahan Bahasa Indonesia ke Bahasa Inggris Menggunakan Transformer MarianMT.

Proyek ini dikembangkan sebagai Ujian Akhir Semester (UAS) Natural Language Processing. Aplikasi ini menawarkan antarmuka penerjemahan yang didukung oleh model deep learning canggih dengan visualisasi langkah-langkah preprocessing dan evaluasi metrik formal NLP secara real-time.

## Fitur Utama

- **Penerjemahan Instan**: Menerjemahkan teks Bahasa Indonesia ke Bahasa Inggris menggunakan model Helsinki-NLP/opus-mt-id-en.
- **Preprocessing Transparan**: Visualisasi langkah pemrosesan teks mulai dari lowercase, pembersihan karakter, normalisasi spasi, hingga tokenisasi kata dasar.
- **Evaluasi Kinerja Formal**: Penilaian akurasi hasil penerjemahan secara objektif dengan metrik BLEU, ROUGE-1, ROUGE-2, ROUGE-L, dan METEOR.
- **Visualisasi Grafik**: Diagram batang, diagram gauge, dan tren historis garis skor evaluasi menggunakan Chart.js.
- **Manajemen Dataset**: Penyimpanan data paralel di SQLite dengan fitur unggah file CSV, pencarian, paginasi, statistik baris/kolom/missing value, dan reset data default.
- **Riwayat Penerjemahan**: Pencatatan riwayat terjemahan lengkap dengan metrik penilaian, fitur hapus item, dan ekspor ke berkas CSV.
- **Desain Enterprise Modern**: Tampilan responsif bertema hijau soft profesional dengan tipografi bersih berbasis Poppins.
- **Kemudahan Navigasi**: Menu navigasi atas (Header Navigation) dengan penyesuaian warna gelap otomatis saat digulir dan tombol gulir kembali ke atas.

## Teknologi yang Digunakan

- Python 3.12+
- Flask (Backend Web Framework)
- HTML5, CSS3, JavaScript (Frontend)
- Bootstrap 5 (Responsive Layout)
- PyTorch & HuggingFace Transformers (Inference)
- Helsinki-NLP/opus-mt-id-en (MarianMT Model)
- Pandas & NumPy (Data Processing)
- NLTK (Tokenization & Meteor)
- SacreBLEU (BLEU evaluation)
- Rouge-score (ROUGE evaluation)
- SQLite (Penyimpanan Data & Riwayat)

## Struktur Folder Proyek

```
smarttranslate/
├── app.py
├── requirements.txt
├── README.md
├── smarttranslate.db
├── models/
├── dataset/
│   └── dataset.csv
├── src/
│   ├── config.py
│   ├── database.py
│   ├── dataset.py
│   ├── evaluation.py
│   ├── preprocessing.py
│   ├── translator.py
│   └── utils.py
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   ├── img/
│   └── icons/
└── templates/
    ├── 404.html
    ├── base.html
    ├── dataset.html
    ├── documentation.html
    ├── evaluation.html
    ├── index.html
    └── translate.html
```

## Cara Instalasi

1. Pastikan Anda telah memasang Python 3.12+ pada sistem Anda.
2. Pasang pustaka dan dependensi proyek menggunakan perintah:

```bash
pip install -r requirements.txt
```

## Cara Menjalankan

Jalankan perintah Flask run dari direktori root proyek:

```bash
flask run
```

Setelah aplikasi berjalan, buka peramban web Anda dan buka alamat:

```text
http://127.0.0.1:5000
```

*Catatan: Pada peluncuran pertama kali, aplikasi akan mengunduh model MarianMT seukuran sekitar 300MB dari Hugging Face secara otomatis. Pastikan perangkat Anda terhubung ke internet.*

## Dataset

Aplikasi ini dilengkapi dengan dataset paralel bawaan yang berisi lebih dari 200 pasang kalimat Bahasa Indonesia dan Bahasa Inggris yang mencakup kategori harian, teknologi, akademik, kantor, dan pariwisata. Dataset ini disimpan di SQLite dan dapat diunduh/diunggah kembali melalui menu Dataset.

## Model

Menggunakan model Helsinki-NLP/opus-mt-id-en dari Hugging Face yang dimuat sekali ke memori saat aplikasi dijalankan dan disimpan dalam direktori cache lokal (folder models/) untuk optimasi kecepatan inferensi berikutnya.

## Evaluasi

Proses evaluasi membandingkan kalimat hasil prediksi model terhadap kalimat referensi asli dari dataset menggunakan pustaka formal:
- BLEU (mengukur presisi kecocokan n-gram kata)
- ROUGE (mengukur recall kecocokan tumpang tindih n-gram)
- METEOR (mengukur kemiripan kata dasar dan sinonim menggunakan WordNet NLTK)

## Screenshot

(Tampilan antarmuka beranda, penerjemahan, visualisasi evaluasi, dan tabel manajemen dataset dapat diakses langsung melalui peramban web setelah server dijalankan)

## Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT.
