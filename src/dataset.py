import os
import csv
import pandas as pd
from src.config import Config
from src.database import get_db_connection

DEFAULT_PAIRS = [
    ("Halo, apa kabar?", "Hello, how are you?"),
    ("Selamat pagi semuanya.", "Good morning everyone."),
    ("Siapa nama Anda?", "What is your name?"),
    ("Saya tinggal di Jakarta.", "I live in Jakarta."),
    ("Apakah Anda bisa membantu saya?", "Can you help me?"),
    ("Terima kasih banyak atas bantuan Anda.", "Thank you very much for your help."),
    ("Sama-sama, dengan senang hati.", "You are welcome, with pleasure."),
    ("Di mana stasiun kereta api terdekat?", "Where is the nearest train station?"),
    ("Berapa harga tiket ini?", "How much is this ticket?"),
    ("Saya ingin memesan secangkir kopi hangat.", "I want to order a cup of warm coffee."),
    ("Hari ini cuacanya sangat bagus.", "Today the weather is very nice."),
    ("Kemarin saya pergi ke perpustakaan.", "Yesterday I went to the library."),
    ("Besok kita akan mengadakan rapat besar.", "Tomorrow we will hold a big meeting."),
    ("Buku ini sangat menarik untuk dibaca.", "This book is very interesting to read."),
    ("Di mana letak toilet umum?", "Where is the public toilet located?"),
    ("Saya suka makan nasi goreng pedas.", "I like to eat spicy fried rice."),
    ("Kami sedang belajar bahasa Inggris.", "We are learning English."),
    ("Apakah Anda memiliki rekomendasi hotel?", "Do you have a hotel recommendation?"),
    ("Jam berapa sekarang di sana?", "What time is it now there?"),
    ("Saya merasa kurang enak badan hari ini.", "I feel a bit unwell today."),
    ("Obat ini harus diminum tiga kali sehari.", "This medicine must be taken three times a day."),
    ("Hati-hati di jalan saat pulang.", "Be careful on the road when going home."),
    ("Selamat ulang tahun, semoga panjang umur.", "Happy birthday, I wish you a long life."),
    ("Semoga sukses dengan ujian Anda.", "Good luck with your exam."),
    ("Di mana saya bisa menukar uang?", "Where can I exchange money?"),
    ("Kamar ini sangat bersih dan nyaman.", "This room is very clean and comfortable."),
    ("Saya ingin membeli oleh-oleh khas daerah.", "I want to buy local souvenirs."),
    ("Pemandangan alam di sini sangat indah.", "The natural scenery here is very beautiful."),
    ("Bandara berada cukup jauh dari pusat kota.", "The airport is quite far from the city center."),
    ("Saya tersesat, bolehkah saya bertanya?", "I am lost, may I ask a question?"),
    ("Tolong pelankan suara Anda sedikit.", "Please lower your voice a bit."),
    ("Saya tidak mengerti apa maksud Anda.", "I do not understand what you mean."),
    ("Tolong tulis alamat ini di kertas.", "Please write this address on paper."),
    ("Apakah Anda menerima pembayaran kartu kredit?", "Do you accept credit card payments?"),
    ("Saya sangat senang bertemu dengan Anda.", "I am very happy to meet you."),
    ("Mari kita pergi makan malam bersama.", "Let us go have dinner together."),
    ("Telepon seluler saya kehabisan baterai.", "My mobile phone has run out of battery."),
    ("Saya ingin menyewa sepeda untuk keliling.", "I want to rent a bicycle to go around."),
    ("Harga barang-barang di pasar sangat murah.", "The price of goods in the market is very cheap."),
    ("Saya harus pergi sekarang juga.", "I have to go right now."),
    ("Pemrosesan bahasa alami adalah bidang yang menarik.", "Natural language processing is an exciting field."),
    ("Model transformer mengubah dunia teknologi informasi.", "Transformer models are changing the world of information technology."),
    ("Mari kita lakukan analisis data hari ini.", "Let us do data analysis today."),
    ("Bahasa adalah alat komunikasi paling penting.", "Language is the most important communication tool."),
    ("Kecerdasan buatan berkembang sangat cepat.", "Artificial intelligence is developing very fast."),
    ("Jaringan saraf tiruan meniru otak manusia.", "Artificial neural networks mimic the human brain."),
    ("Pembelajaran mendalam membutuhkan banyak data.", "Deep learning requires a lot of data."),
    ("Pembelajaran mesin membantu memprediksi tren.", "Machine learning helps predict trends."),
    ("Algoritma ini sangat efisien dalam komputasi.", "This algorithm is very efficient in computation."),
    ("Kami menggunakan pustaka pandas untuk manipulasi data.", "We use the pandas library for data manipulation."),
    ("Numpy menyediakan operasi matriks yang cepat.", "Numpy provides fast matrix operations."),
    ("Sacrebleu digunakan untuk mengevaluasi metrik terjemahan.", "Sacrebleu is used to evaluate translation metrics."),
    ("Metrik rouge mengukur tumpang tindih n-gram.", "The rouge metric measures n-gram overlap."),
    ("Meteor mengevaluasi keselarasan kata secara dinamis.", "Meteor evaluates word alignment dynamically."),
    ("Data latih harus dibersihkan terlebih dahulu.", "The training data must be cleaned first."),
    ("Tokenisasi memecah teks menjadi unit kecil.", "Tokenization breaks text into small units."),
    ("Penerjemahan mesin membantu menghubungkan banyak orang.", "Machine translation helps connect many people."),
    ("Korpus paralel berisi teks dua bahasa.", "A parallel corpus contains texts of two languages."),
    ("Evaluasi otomatis menghemat waktu dan biaya.", "Automatic evaluation saves time and cost."),
    ("Kami memproses kumpulan data sebelum melatih model.", "We process the dataset before training the model."),
    ("Setiap kalimat harus memiliki pasangan terjemahan.", "Each sentence must have a translation pair."),
    ("Akurasi terjemahan sangat tergantung kualitas data.", "Translation accuracy highly depends on data quality."),
    ("Representasi vektor menyimpan makna kata.", "Vector representation stores word meaning."),
    ("Perhatian mandiri adalah kunci arsitektur transformer.", "Self-attention is the key of the transformer architecture."),
    ("Gunakan pustaka huggingface untuk memuat model.", "Use the huggingface library to load the model."),
    ("Token khusus digunakan untuk menandai awal kalimat.", "Special tokens are used to mark the start of a sentence."),
    ("Model marianmt sangat cocok untuk penerjemahan.", "The marianmt model is very suitable for translation."),
    ("Kami membagi data menjadi latih dan uji.", "We split the data into train and test."),
    ("Fungsi kerugian dioptimalkan menggunakan adam.", "The loss function is optimized using adam."),
    ("Kecepatan inferensi dapat ditingkatkan dengan gpu.", "Inference speed can be increased with a GPU."),
    ("Model pra-terlatih sangat menghemat sumber daya.", "Pre-trained models highly save resources."),
    ("Penerjemahan berbasis aturan memiliki banyak batasan.", "Rule-based translation has many limitations."),
    ("Analisis sentimen mendeteksi emosi dalam teks.", "Sentiment analysis detects emotions in text."),
    ("Ekstraksi entitas mengenali nama orang dan lokasi.", "Entity extraction recognizes names of people and locations."),
    ("Ringkasan teks otomatis menghasilkan poin penting.", "Automatic text summarization generates key points."),
    ("Klasifikasi teks membagi dokumen ke dalam kategori.", "Text classification divides documents into categories."),
    ("Model bahasa generatif dapat menulis cerita.", "Generative language models can write stories."),
    ("Penyetelan halus menyesuaikan model ke tugas spesifik.", "Fine-tuning adapts the model to a specific task."),
    ("Bias dalam data harus diidentifikasi dan dikurangi.", "Bias in data must be identified and mitigated."),
    ("Etika kecerdasan buatan adalah topik penting.", "Ethics of artificial intelligence is an important topic."),
    ("Rapat hari ini dimulai pukul sembilan pagi.", "Today's meeting starts at nine in the morning."),
    ("Laporan keuangan harus diserahkan akhir bulan.", "The financial report must be submitted at the end of the month."),
    ("Saya bekerja sebagai pengembang perangkat lunak.", "I work as a software developer."),
    ("Kantor kami menerapkan sistem kerja fleksibel.", "Our office implements a flexible working system."),
    ("Kami membutuhkan proposal proyek minggu depan.", "We need the project proposal next week."),
    ("Evaluasi kinerja dilakukan setiap enam bulan.", "Performance evaluation is conducted every six months."),
    ("Kerja sama tim sangat penting untuk sukses.", "Teamwork is very important for success."),
    ("Tolong kirimkan berkas ini melalui surat elektronik.", "Please send this file via email."),
    ("Saya sedang menghadiri konferensi teknologi.", "I am attending a technology conference."),
    ("Silakan tanda tangani dokumen kontrak kerja.", "Please sign the employment contract document."),
    ("Batas waktu pengumpulan tugas adalah besok sore.", "The deadline for task submission is tomorrow afternoon."),
    ("Kami harus memotong anggaran biaya operasional.", "We have to cut operational budget costs."),
    ("Peluncuran produk baru ditunda bulan depan.", "The launch of the new product is postponed to next month."),
    ("Manajer pemasaran sedang mempresentasikan strategi.", "The marketing manager is presenting the strategy."),
    ("Silakan hubungi bagian layanan pelanggan.", "Please contact customer service."),
    ("Kami berkomitmen memberikan kualitas terbaik.", "We are committed to providing the best quality."),
    ("Keamanan data adalah prioritas utama perusahaan.", "Data security is the company's top priority."),
    ("Sesi pelatihan karyawan diadakan hari kamis.", "The employee training session is held on Thursday."),
    ("Surat penawaran harga telah dikirim ke klien.", "The price quotation letter has been sent to the client."),
    ("Proyek ini membutuhkan analisis kebutuhan detail.", "This project requires a detailed requirements analysis."),
    ("Kami merencanakan perjalanan liburan ke Bali.", "We are planning a holiday trip to Bali."),
    ("Tiket pesawat sudah dipesan jauh hari.", "The plane tickets have been booked long in advance."),
    ("Candi Borobudur adalah tujuan wisata populer.", "Borobudur Temple is a popular tourist destination."),
    ("Saya ingin mengunjungi museum sejarah besok.", "I want to visit the history museum tomorrow."),
    ("Pantai di Lombok sangat bersih dan indah.", "The beach in Lombok is very clean and beautiful."),
    ("Di mana tempat menyewa mobil yang murah?", "Where is a cheap car rental place?"),
    ("Wisatawan asing harus membawa paspor mereka.", "Foreign tourists must carry their passports."),
    ("Makanan tradisional Indonesia sangat kaya rempah.", "Traditional Indonesian food is very rich in spices."),
    ("Saya ingin memesan tur berpemandu untuk kota ini.", "I want to book a guided tour for this city."),
    ("Berapa lama perjalanan dari sini ke bandara?", "How long is the trip from here to the airport?"),
    ("Peta digital sangat membantu saat bepergian.", "Digital maps are very helpful when traveling."),
    ("Kami menginap di penginapan dekat pantai.", "We stayed at a guesthouse near the beach."),
    ("Cuaca tropis sangat hangat sepanjang tahun.", "The tropical weather is very warm all year round."),
    ("Jangan lupa membawa tabir surya saat liburan.", "Do not forget to bring sunscreen during holidays."),
    ("Saya ingin mencoba kuliner lokal di pasar malam.", "I want to try local cuisine at the night market."),
    ("Penerbangan kami ditunda selama dua jam.", "Our flight was delayed for two hours."),
    ("Stasiun pengisian daya baterai ada di sana.", "The battery charging station is over there."),
    ("Kami membeli tiket masuk secara daring.", "We bought the admission tickets online."),
    ("Taksi online sangat mudah ditemukan di sini.", "Online taxis are very easy to find here."),
    ("Simpan barang bawaan Anda di tempat yang aman.", "Keep your luggage in a safe place."),
    ("Metode penelitian harus dijelaskan secara rinci.", "The research method must be explained in detail."),
    ("Tinjauan pustaka mendukung landasan teori.", "The literature review supports the theoretical foundation."),
    ("Hipotesis diuji menggunakan analisis statistik.", "The hypothesis is tested using statistical analysis."),
    ("Hasil penelitian ini dipublikasikan di jurnal internasional.", "The results of this study are published in an international journal."),
    ("Daftar pustaka diletakkan di bagian akhir.", "The bibliography is placed at the end."),
    ("Pengumpulan data dilakukan melalui kuesioner.", "Data collection is conducted through questionnaires."),
    ("Sampel penelitian harus representatif.", "The research sample must be representative."),
    ("Tesis ini membahas tentang pembelajaran mesin.", "This thesis discusses machine learning."),
    ("Abstrak merangkum seluruh isi laporan.", "The abstract summarizes the entire content of the report."),
    ("Penelitian lanjutan diperlukan untuk validasi.", "Further research is required for validation."),
    ("Analisis kuantitatif menghasilkan data angka.", "Quantitative analysis produces numerical data."),
    ("Studi kasus dilakukan pada tiga sekolah.", "The case study was conducted at three schools."),
    ("Kesimpulan menjawab tujuan penelitian.", "The conclusion answers the research objectives."),
    ("Saran diberikan untuk perbaikan sistem.", "Suggestions are provided for system improvement."),
    ("Variabel bebas memengaruhi variabel terikat.", "The independent variable influences the dependent variable."),
    ("Etika penelitian harus dijunjung tinggi oleh peneliti.", "Research ethics must be upheld by researchers."),
    ("Kutipan langsung harus mencantumkan sumber.", "Direct citations must state the source."),
    ("Plagiarisme adalah pelanggaran akademik berat.", "Plagiarism is a serious academic offense."),
    ("Sidang tugas akhir diadakan bulan depan.", "The final project defense is held next month."),
    ("Dosen pembimbing memberikan banyak masukan.", "The advisor provides a lot of input."),
    ("Kopi arabika memiliki aroma yang sangat harum.", "Arabica coffee has a very fragrant aroma."),
    ("Anak-anak bermain layang-layang di lapangan.", "Children play kites in the field."),
    ("Ibu memasak sup ayam di dapur.", "Mother cooks chicken soup in the kitchen."),
    ("Ayah membaca koran sambil minum teh hangat.", "Father reads the newspaper while drinking warm tea."),
    ("Kereta komuter selalu penuh di pagi hari.", "The commuter train is always full in the morning."),
    ("Kami merayakan hari kemerdekaan setiap agustus.", "We celebrate independence day every August."),
    ("Pasar tradisional menjual sayuran segar.", "The traditional market sells fresh vegetables."),
    ("Toko buku itu buka dari jam delapan pagi.", "The bookstore is open from eight in the morning."),
    ("Saya membeli sepatu baru untuk sekolah.", "I bought new shoes for school."),
    ("Kucing hitam itu memanjat pohon mangga.", "The black cat climbed the mango tree."),
    ("Adik sedang menggambar pemandangan gunung.", "Little sibling is drawing a mountain scenery."),
    ("Mereka bermain sepak bola di bawah hujan.", "They play soccer under the rain."),
    ("Pertunjukan musik itu sangat meriah.", "The music performance was very lively."),
    ("Kami menanam bunga mawar di kebun depan.", "We plant roses in the front garden."),
    ("Udara pegunungan sangat sejuk dan segar.", "The mountain air is very cool and fresh."),
    ("Jalan raya sangat macet saat jam pulang kerja.", "The highway is very congested during rush hour."),
    ("Lampu lalu lintas di perempatan mati.", "The traffic light at the intersection is broken."),
    ("Kami mengunjungi nenek di desa akhir pekan lalu.", "We visited grandmother in the village last weekend."),
    ("Museum itu menyimpan koleksi benda bersejarah.", "The museum stores a collection of historical objects."),
    ("Lukisan dinding itu dibuat oleh seniman lokal.", "The wall painting was made by a local artist."),
    ("Gelas kaca itu pecah karena jatuh dari meja.", "The glass cup broke because it fell from the table."),
    ("Kami menyalakan lampu karena hari sudah gelap.", "We turned on the light because it was already dark."),
    ("Pencuri itu ditangkap oleh polisi kemarin malam.", "The thief was caught by the police last night."),
    ("Buku catatan saya tertinggal di kelas.", "My notebook was left in the classroom."),
    ("Kami selalu berdiskusi untuk menyelesaikan masalah.", "We always discuss to solve problems."),
    ("Air sungai itu sangat jernih dan dingin.", "The river water is very clear and cold."),
    ("Burung-burung berkicau merdu di pagi hari.", "Birds chirp melodiously in the morning."),
    ("Kami membutuhkan lemari baru untuk baju.", "We need a new wardrobe for clothes."),
    ("Kunci rumah saya hilang entah di mana.", "My house key is lost somewhere."),
    ("Jendela kamar harus dibuka agar udara segar masuk.", "The room window must be opened so fresh air enters."),
    ("Pekerjaan rumah matematika sangat sulit.", "The mathematics homework is very difficult."),
    ("Kakak perempuan saya bekerja di bank swasta.", "My older sister works in a private bank."),
    ("Paman saya mengajar sejarah di universitas.", "My uncle teaches history at the university."),
    ("Sepeda motor baru itu berwarna merah terang.", "The new motorcycle is bright red."),
    ("Kami berenang di kolam renang umum.", "We swam in the public swimming pool."),
    ("Tolong matikan televisi jika tidak ditonton.", "Please turn off the television if not watched."),
    ("Mereka sedang membangun jembatan baru.", "They are building a new bridge."),
    ("Banjir melanda beberapa wilayah kota.", "Floods hit several areas of the city."),
    ("Petani menanam padi di sawah.", "Farmers plant rice in the paddy fields."),
    ("Nelayan pergi melaut pada malam hari.", "Fishermen go to sea at night."),
    ("Saya ingin menabung uang di bank.", "I want to save money in the bank."),
    ("Kursi kayu itu sangat kokoh.", "The wooden chair is very sturdy."),
    ("Kami membuat kue bolu cokelat bersama ibu.", "We made chocolate sponge cake with mother."),
    ("Adik menangis karena mainannya rusak.", "Little sibling cried because their toy was broken."),
    ("Pencarian informasi sekarang sangat mudah dengan internet.", "Searching for information is now very easy with the internet."),
    ("Kami menonton film dokumenter tentang sejarah dinosaurus.", "We watched a documentary film about dinosaur history."),
    ("Kakek suka membaca buku sastra kuno.", "Grandfather likes to read ancient literature books."),
    ("Pintu gerbang sekolah ditutup jam tujuh pagi.", "The school gate is closed at seven in the morning."),
    ("Kami membersihkan rumah bersama setiap hari minggu.", "We clean the house together every Sunday."),
    ("Kakak laki-laki saya gemar bermain gitar.", "My older brother likes playing guitar."),
    ("Saya membeli buah apel merah di supermarket.", "I bought red apples at the supermarket."),
    ("Suara musik dari tetangga sangat bising.", "The music sound from the neighbor is very noisy."),
    ("Kami menggunakan kompor gas untuk memasak.", "We use a gas stove to cook."),
    ("Sepatu olahraga ini sangat ringan dipakai.", "These sports shoes are very light to wear."),
    ("Pemerintah membangun jalan tol baru.", "The government builds a new toll road."),
    ("Hujan deras disertai angin kencang merusak atap.", "Heavy rain with strong wind damaged the roof."),
    ("Kami merayakan kelulusan kakak minggu depan.", "We celebrate older sibling's graduation next week."),
    ("Anak kucing itu manja sekali.", "The kitten is very affectionate."),
    ("Saya minum teh chamomile sebelum tidur malam.", "I drink chamomile tea before sleeping at night."),
    ("Kami menaruh tempat sampah di depan rumah.", "We put a trash bin in front of the house."),
    ("Udara malam ini terasa sangat dingin sekali.", "The air tonight feels very cold indeed."),
    ("Bunga anggrek itu mekar dengan indah sekali.", "The orchid flower blooms very beautifully indeed.")
]

def generate_default_dataset_csv():
    os.makedirs(Config.DATASET_DIR, exist_ok=True)
    if not os.path.exists(Config.DATASET_PATH):
        with open(Config.DATASET_PATH, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "indonesia", "english", "created_at"])
            for idx, (indo, eng) in enumerate(DEFAULT_PAIRS, 1):
                writer.writerow([idx, indo, eng, "2026-07-21 00:00:00"])

def import_csv_to_db(file_path=None):
    if file_path is None:
        file_path = Config.DATASET_PATH
    
    if not os.path.exists(file_path):
        generate_default_dataset_csv()
    
    df = pd.read_csv(file_path)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dataset")
    
    for idx, row in df.iterrows():
        indo = str(row["indonesia"]) if pd.notna(row["indonesia"]) else ""
        eng = str(row["english"]) if pd.notna(row["english"]) else ""
        created = str(row["created_at"]) if "created_at" in df.columns and pd.notna(row["created_at"]) else "2026-07-21 00:00:00"
        
        cursor.execute(
            "INSERT INTO dataset (indonesia, english, created_at) VALUES (?, ?, ?)",
            (indo, eng, created)
        )
    conn.commit()
    conn.close()

def get_dataset_from_db(page: int, per_page: int, search_query: str = ""):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    offset = (page - 1) * per_page
    
    if search_query:
        query = "%" + search_query + "%"
        cursor.execute(
            "SELECT COUNT(*) FROM dataset WHERE indonesia LIKE ? OR english LIKE ?",
            (query, query)
        )
        total_count = cursor.fetchone()[0]
        
        cursor.execute(
            "SELECT * FROM dataset WHERE indonesia LIKE ? OR english LIKE ? LIMIT ? OFFSET ?",
            (query, query, per_page, offset)
        )
        rows = cursor.fetchall()
    else:
        cursor.execute("SELECT COUNT(*) FROM dataset")
        total_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT * FROM dataset LIMIT ? OFFSET ?", (per_page, offset))
        rows = cursor.fetchall()
        
    conn.close()
    return [dict(row) for row in rows], total_count

def get_dataset_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM dataset")
    total_rows = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM dataset WHERE indonesia IS NULL OR indonesia = '' OR english IS NULL OR english = ''")
    missing_values = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total_rows": total_rows,
        "total_cols": 4,
        "missing_values": missing_values
    }
