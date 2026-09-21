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

# AI Disclosure (last upd: Tugas Individu 3)

Saya menggunakan Claude Code dan Copilot (BYOK dengan API key dari DeepSeek), serta Claude via Web Browser untuk membantu proses pembelajaran di Tugas Individu 1 ini. Claude via Web Browser saya gunakan untuk menanyakan konsep-konsep Web Development, sedangkan Claude Code dan Copilot untuk agentic atau untuk pertanyaan yang membutuhkan konteks kode.

Prompt yang saya gunakan:

```
1. make sure every html extends index.html
2. make a ProjectForm, take context from the Project model in models.py
3. add create, update, delete, in views.py for Projects, use json and serializers, take music's endpoint for example.
4. update css, since some aspects are similar to music's form, might want to rename the css' class/id to make it more general
5. complete the projects_form.html and projects.html
6. add api endpoint in urls.py for api/project
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

### Tugas 3

1. Jelaskan mengapa kita menggunakan `ModelForm` pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan `{% csrf_token %}` pada form tersebut!

Jawab:

Sebagai salah satu prinsip DRY, yaitu tidak mengulang apa yang sudah ditulis di models.py. Fields-fields diambil dari models.py instead of ditulis ulang. Selain itu, validasi jadi otomatis mengikuti ketentuan yang ditulis di models.py juga (misalnya 255 karakter, tipe data apa, dll.)

Kode di template HTML juga dapat menjadi lebih singkat, dengan satu loop `{% for field in form %}`, dibanding semua field dihard-code di template.

Terakhir, hanya data dari ``Meta.fields`` yang diproses, jadi lebih aman dibanding input mentah jika membuat form HTML.

Pertanyaan kedua, mengapa CSRF token wajib? CSRF (atau Cross Site Request Forgery) adalah serangan yang memanfaatkan fakta bahwa browser otomatis menyertakan cookie session ke domain tujuan, bahkan untuk request yang dipicu dari situs lain. Contohnya, saat saya sedang login di situs portofolio ini lalu membuka situs jahat yang berisi form tersembunyi yang mem-POST ke `/projects/<id>/delete/` dan disubmit otomatis lewat JavaScript, browser akan mengirim request itu beserta cookie session saya, sehingga server mengira itu request sah dan proyek saya terhapus. Penyerang tidak perlu mencuri cookie-nya.

Jika ada `{% csrf_token %}`, setiap POST harus menyertakan token acak yang unik per session, dan server memeriksanya lewat `CsrfViewMiddleware`. Situs jahat tidak dapat membaca token tersebut (same-origin policy), sehingga request palsu itu ditolak dengan error 403.

2. Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?

Jawab:
JSON lebih disukai karena ringkas, lebih kecil, dan lebih cepat diparsing, selain itu JSON lebih mudah dibaca (``{ "name": "David" }`` vs ``<name>David</name>``), dan ada juga aspek familiaritas/kemiripan dengan struktur data modern seperti object/array/dictionary. JSON juga lebih mudah diolah di JavaScript, karena formatnya mirip dengan object literal JS. Selain itu, JSON punya tipe bawaan untuk object, array, string, number, boolean, dan null, sehingga langsung cocok dengan dict/list di Python, sedangkan XML lebih verbose dan tipe datanya harus ditafsirkan sendiri. Perlu dicatat bahwa REST API sebenarnya juga boleh memakai XML (Django pun bisa `serialize("xml", ...)`), tetapi JSON menjadi konvensi yang dominan karena alasan-alasan di atas.

3. Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?

Jawab:
Alur pada endpoint `api/project/` (fungsi `get_projects_json` di `views.py`):

- Browser mengirim `GET /api/project/` (dengan query seperti `?title=web` optsional)
- Request melewati middleware, lalu urls.py di portofolio meneruskan request ke urls.py di main app, yang memetakan path `api/project/` ke fungsi `get_projects_json`.
- Fungsi tersebut membaca query `title` dari `request.GET`, lalu mengambil data lewat ORM: `Project.objects.all()`, dan menyaringnya dengan `filter(title__icontains=...)` bila ada query.
- Hasilnya berupa QuerySet berisi objek model Python, yang kemudian diubah menjadi string JSON dengan `serializers.serialize("json", projects)`.
- String JSON itu dibungkus dengan `HttpResponse(..., content_type="application/json")` dan dikirim kembali ke client, sehingga client tahu bahwa isinya JSON dan bukan HTML.
- Untuk halaman `/projects/`, fungsi `show_projects` memanggil `get_projects_json`, mendeserialisasi hasilnya dengan `serializers.deserialize("json", ...)` menjadi objek `Project`, lalu mengirimnya sebagai context ke `projects.html` untuk dirender menjadi HTML.

Mengapa perlu serialization? Karena HTTP hanya membawa teks (byte), sedangkan objek model seperti `Project` hanyalah struktur di memori Python yang tidak bisa langsung dikirim, dan client seperti JavaScript atau aplikasi mobile juga tidak mengenal objek Python. Serialization mengubah objek menjadi format standar (JSON) yang bisa dikirim dan dipahami client mana pun. Serializer Django juga menangani tipe data khusus seperti `UUIDField` (`id`) dan `DateField` (`released_at`) yang bukan tipe bawaan JSON dengan mengubahnya menjadi string yang valid, dan hasilnya bisa dideserialisasi kembali menjadi objek model.

Endpoint JSON hanya mengirim data tanpa tampilan, sehingga bisa dipakai ulang oleh banyak client, tidak hanya browser. Untuk halaman HTML saja sebenarnya `Project.objects.all()` langsung ke template sudah cukup; di proyek ini `show_projects` sengaja memutar lewat serialize lalu deserialize untuk mengikuti pola endpoint music dan menunjukkan alur serialization.
