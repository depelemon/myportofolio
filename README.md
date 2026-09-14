# Data Diri

Nama : David Liman

NPM : 2506601956

Kelas : PBP B

# Cara Menjalankan Proyek

Berikut langkah-langkah untuk menjalankan proyek ini secara lokal.

1. **Clone repository** (jika belum punya salinannya) lalu masuk ke direktori proyek:

   ```bash
   git clone <url-repository>
   cd myportofolio
   ```
2. **Buat dan aktifkan virtual environment**:

   ```bash
   python -m venv env
   ```

   - Windows:
     ```bash
     env\Scripts\activate
     ```
   - macOS / Linux:
     ```bash
     source env/bin/activate
     ```
3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
4. **(Opsional) Siapkan file `.env`** di root proyek bila dibutuhkan. Proyek ini membaca environment variables dengan `python-dotenv` (contohnya `PRODUCTION`), namun untuk menjalankan secara lokal umumnya tidak wajib diisi karena sudah ada nilai default.
5. **(Opsional) Jalankan migrasi database** (bila belum ada `db.sqlite3` atau ada perubahan model):

   ```bash
   python manage.py migrate
   ```
6. **Jalankan server development**:

   ```bash
   python manage.py runserver
   ```
7. **Buka aplikasi** di browser pada alamat yang muncul di terminal, biasanya:

   ```
   http://127.0.0.1:8000/
   ```

> Catatan: pastikan `manage.py` berada satu level dengan direktori `portofolio/` saat menjalankan perintah di atas (root proyek).

# Dokumentasi &

Untuk branching, saya memutuskan menggunakan branch bertahap dari branch dev ke branch main, dengan alasan agar mempermudah proses review dan mengurangi risiko error yang mungkin terjadi.

Untuk setiap fitur baru yang signifikan, akan ada branch baru yang dibuat dari branch dev (contohnya feat/<feature-name></feature>). Dengan melakukan branching bertahap, setiap perubahan dapat diuji secara terpisah sebelum digabungkan ke branch utama, sehingga meminimalkan potensi konflik dan memastikan stabilitas kode.

# AI Disclosure (last upd: Tugas Individu 2)

saya menggunakan Claude Code dan Copilot (BYOK dengan API key dari DeepSeek), serta Claude via Web Browser untuk membantu proses pembelajaran di Tugas Individu 1 ini. Claude via Web Browser saya gunakan untuk menanyakan konsep-konsep Web Development, sedangkan Claude Code dan Copilot untuk agentic atau untuk pertanyaan yang membutuhkan konteks kode.

Contoh prompt yang saya gunakan:

```
1. Tambahkan satu model baru pada aplikasi main yang merepresentasikan bagian portofolio pilihanmu.
2. Model tersebut memiliki minimal tiga field selain primary key (id, baik dibuat otomatis oleh Django maupun ditentukan sendiri), dengan tipe data yang sesuai.
3. Buat dan terapkan migrasi model, lalu sertakan berkas migrasinya dalam commit.
4. Buat sebuah view yang mengambil data dari model, memasukkannya ke dalam context, dan meneruskannya ke template baru.
5. Tampilkan seluruh objek menggunakan perulangan Django Template Language dan sediakan tampilan untuk kondisi ketika data masih kosong.
6. Data pada bagian portofolio baru tidak ditulis langsung (hard-coded) di HTML. Teks antarmuka statis, seperti judul halaman, label navigasi, dan isi footer, tetap boleh ditulis di template.
7. Daftarkan named route pada main/urls.py dengan URL yang berbeda dari halaman utama.
8. Tambahkan tautan menuju halaman baru pada navbar menggunakan tag {% url %}. Pastikan navbar dan footer konsisten dengan halaman lain.
9. Tambahkan unit test yang mencakup minimal tiga kasus pengujian:
9a. URL dapat diakses dan menggunakan template yang tepat.
9b. Data model muncul di halaman HTML ketika ada data.
9c. Halaman HTML menampilkan pesan kondisi kosong ketika belum ada data.
10. Pastikan proyek dapat dijalankan dengan python manage.py runserver tanpa error dan seluruh test lulus ketika menjalankan python manage.py test.

Sekarang page bernamakan "Portfolio", untuk membedakan dengan root folder, ubah jadi "Music" (jadi isinya portfolio musik)
Tolong kerjakan tugas-tugas ini untuk item-item di @templates/music.html (ubah portfolio.html jadi music.html), dengan field:

- Nama
- Deskripsi
- Tanggal
- Audio file yang nanti akan aku simpan di dalam static folder, jadi di database disimpan sebagai path string aja

Buat apps baru bertajuk `music`, seperti apps @templates/experiences.html yang ada sekarang. Penuhi setiap syarat yang ada, serta jangan memakai commnent apapun untuk menjelaskan tulisan kode kamu, jelaskan secara rinci di dalam chat saja

```

Selengkapnya bisa dilihat di log Claude Code dalam bentuk JSONL [di sini](https://drive.google.com/file/d/1EbFrMbnWK_ZQVrMlb2Ing-Z9RlkdiWsQ/view?usp=sharing)

# Pertanyaan Reflektif

### Tugas 1

1. Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti \<section\>, \<article\>, atau \<aside\>? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?

Jawab: Saya menggunakan elemen semantik, tapi tidak semuanya, contohnya saya menggunakan \<section\> untuk grouping konten yang berbeda-beda seperti About Me, Experiences (dan section lain yang nantinya akan ditambahkan). Elemen ini jadi best practice untuk membuat struktur HTML lebih mudah dipahami, lebih konsisten antar halaman, dan lebih mudah diakses search engine atau mesin scraper untuk memahami apa yang ada di website saya. Saya tidak menggunakan \<article\> atau \<aside\> karena project saat ini masih sederhana, dan belum ada use casenya di design yang saya pikirkan.

2. Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?

Jawab:  Karena keterbatasan waktu, saya hanya sempat mengimplementasikan styling untuk desktop-view, dan tidak terlalu memperhatikan responsiveness, tetapi karena bagian yang saya kerjakan di tugas ini adalah section Experiences yang berbentuk timeline, layout-nya sudah responsif by design. Tantangan yang saya temui justru ada di elemen dekoratifnya: garis vertikal dan titik penanda timeline diposisikan dengan offset kiri yang tetap, jadi saya harus memastikan penanda selalu sejajar dengan judul tiap entri dan teks tidak menabrak garis saat layar menyempit. Selain itu, karena tiap entri kini berisi poin-poin deskripsi, saya menambah jarak vertikal antar entri agar satu pengalaman tidak menyatu dengan pengalaman berikutnya. Untuk mengevaluasi elemen mana yang diprioritaskan, saya berpatokan pada hierarki konten: judul entri adalah elemen utama (penanda timeline harus sejajar dengannya), lalu meta, dan poin deskripsi paling akhir, sehingga yang dikorbankan saat layar sempit adalah hal-hal dekoratif, bukan teksnya.

3. Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?

Jawab: Batasannya jelas tidak bisa menampilkan data secara dinamis, tetapi karena isi webnya memang masih sedikit (dan belum berisi semua section yang saya plan, karena sekali lagi keterbatasan waktu, maaf kak), jadi memang belum memerlukan database untuk data dinamis. Untuk iterasi selanjutnya, karena ini project portofolio, sepertinya keperluan databasenya tidak terlalu mendesak? Mungkin saya ingin merefactor bagian entri-entri untuk section Experiences (yang sekarang saya simpan di /portofolio/data/experiences.json) agar diimport ke database, dan menambahkan endpoint untuk mengakses data tersebut. Selain itu, mungkin menyimpan foto-foto project di database juga.

### Tugas 2

1. Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran urls.py proyek, urls.py aplikasi, view, model, dan template.

Jawab: Saya menambahkan page baru, "Music", contoh alur yang terjadi di dalam django:

- pertama browser mengirim request (misalnya, waktu user klik link "Music" di navbar), lebih spesifiknya browser mengirim GET /music/ yang dibungkus lewat HttpRequest dan diteruskan lewat middleware di settings.py.
- request itu pertama lewat routing di portofolio/urls.py, lalu diteruskan ke main.urls.
- setelah diteruskan ke main.urls (main/urls.py), routing Django mencocokkan path /music/ yang dipetakan ke suatu function di View bernama show_music.
- function show_music di views.py menerima request lalu mengambil data model Music dari database, lalu dioper sebagai context untuk dirender pada music.html.
- peran Model (Music di models.py) adalah mendefinisikan field data apa saja yang perlu ada (name, description, released_at, audio_path) dan menjadi perantara ke database lewat ORM.
- template (contohnya music.html, yang juga menggunakan base.html) adalah kerangka HTML yang mengisi `{% block content %}`. `{% for music in music_list %}` membuat satu kartu untuk setiap objek, `{{ music.name }}` dan filter `date` menampilkan data, `{% static music.audio_path %}` mengubah `audio/main_menu.mp3` menjadi `/static/audio/main_menu.mp3`, dan `{% empty %}` menampilkan pesan "Belum ada musik yang ditambahkan." jika tabel masih kosong.
- setelah proses render selesai, respons berupa HTML yang dibungkus menjadi HttpResponse (dengan status 200, success) dikirim kembali melalui middleware ke browser, lalu response tersebut ditampilkan oleh browser dengan request tambahan untuk CSS dan/atau static file, seperti file mp3 untuk musik.

Singkatnya: **browser → `portofolio/urls.py` → `main/urls.py` → view → model/database → view → template → HTML → browser**.

2. Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.

Jawab: Karena best practicenya adalah memisahkan data dan tampilan. Template HTML cukup tahu bagaimana cara sebuah lagu ditampilkan, regardless of ada berapa dan apa saja datanya. Pros-nya:

- Menambah atau mengubah data jadi mudah, melalui admin, tanpa menyentuh bagian yang di-hardcode.
- Kalau ingin mengubah tampilan musik misalnya, tinggal ubah templatenya saja, tidak perlu ubah satu-satu seperti jika semua entri musik di-hardcode.
- Data lebih konsisten dan valid, karena model memaksa setiap entri punya field yang sama dengan tipe yang jelas.
- Data bisa dipakai ulang dan diolah. Data yang sama bisa diurutkan, difilter, ditampilkan di halaman lain.
- Mempermudah testing.

Hal ini juga menjawab rencana saya di Tugas 1, sebelumnya data Experiences disimpan terpisah dari database, sekarang Experiences dan Music sama-sama diambil dari model.

3. Apa perbedaan fungsi makemigrations dan migrate pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.

Jawab:

- **`makemigrations`** membandingkan isi `models.py` saat ini dengan kondisi yang tercatat di file-file migrasi sebelumnya, lalu membuat file migrasi baru (file Python di folder `migrations/`) yang berisi daftar operasi perubahan, misalnya `CreateModel` atau `AddField`. Di tahap ini belum ada perubahan di database, baru "rencana" perubahan.
- Pada saat `migrate` dijalankan, barulah file-file migrasi diterapkan ke database, dengan menerjemahkannya menjadi perintah SQL (seperti   `CREATE TABLE`atau`ALTER TABLE`). Django mencatat migrasi mana yang sudah dijalankan di tabel `django_migrations`, jadi migrasi yang sama tidak akan diterapkan dua kali.

Singkatnya, `makemigrations` menulis rencana perubahan, sedangkan `migrate` mengeksekusi rencana tersebut ke database.

Contoh yang saya alami di tugas ini adalah saat menambahkan model `Music`. Setelah menulis class `Music` di `models.py`, saya menjalankan `python manage.py makemigrations`, yang menghasilkan file `main/migrations/0004_music.py` berisi operasi `Create model Music`. Pada tahap ini tabelnya belum ada, sehingga membuka `/music/` akan error `no such table: main_music`. Setelah itu saya menjalankan `python manage.py migrate` untuk benar-benar membuat tabel `main_music` di database. Saat deploy ke PWS, file `0004_music.py` yang sudah di-commit tinggal dijalankan dengan `migrate` agar database production ikut punya tabel yang sama.

Contoh lain yang juga membutuhkan kedua perintah: menambah field baru (misalnya `duration = models.DurationField()` pada `Music`), menghapus atau mengganti nama field, atau mengubah tipe dan atribut field, seperti migrasi `0003_alter_experience_started_at.py` di proyek ini. Sebaliknya, perubahan yang tidak memengaruhi struktur tabel, seperti menambah method `save()` untuk merapikan `audio_path` atau mengubah `__str__`, tidak memerlukan migrasi (`makemigrations` akan melaporkan "No changes detected").
