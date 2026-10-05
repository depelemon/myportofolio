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
5. **Jalankan migrasi database** (wajib setelah pull Tugas 4, karena ada migrasi relasi star pada Music dan pembuatan grup `Editor`):

   ```bash
   python manage.py migrate
   ```
6. **(Opsional) Siapkan akun untuk tiap peran** (lihat bagian [Tugas 4](#tugas-4-autentikasi-otorisasi-dan-star) di bawah):

   ```bash
   python manage.py createsuperuser
   ```
7. **Jalankan server development**:

   ```bash
   python manage.py runserver
   ```
8. **Buka aplikasi** di browser pada alamat yang muncul di terminal, biasanya:

   ```
   http://127.0.0.1:8000/
   ```
9. **(Opsional) Jalankan test**:

   ```bash
   python manage.py test main
   ```

> Catatan: pastikan `manage.py` berada satu level dengan direktori `portofolio/` saat menjalankan perintah di atas (root proyek).

# Progres Mingguan

## Tugas 5: Interaktivitas dengan JavaScript (AJAX)

Pola dari Tutorial 05 (yang dipakai di Projects) sekarang diterapkan ke bagian **Music** dari Tugas 3 dan 4. Tidak ada migrasi baru di tugas ini.

### Alur halaman `/music/`

1. `show_music` hanya merender kerangka halaman: form pencarian, elemen loading/error/empty, `<ul id="music-list">` kosong, dan (khusus pemilik) modal tambah serta modal hapus.
2. JavaScript memanggil `fetch('/api/music/')`, lalu membangun card dari JSON. Saat data dimuat tampil *"Memuat musik..."*, saat kosong tampil pesan kosong (berbeda untuk hasil pencarian), dan saat gagal tampil pesan error dengan tombol **Coba lagi**.
3. Pencarian berdasarkan judul dikirim lewat AJAX dengan *debouncing* 300 ms. Request sebelumnya dibatalkan dengan `AbortController` agar hasil lama tidak menimpa hasil baru, dan kata kunci disimpan di URL (`?title=`) agar tetap sama saat halaman di-reload.

### Endpoint

| Method | URL                    | View                  | Keterangan                                                                                                                                                |
| ------ | ---------------------- | --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GET    | `/api/music/?title=` | `get_music_json`    | JSON dirakit manual dengan`JsonResponse`: field publik, `audio_url`, `star_count`, dan `is_starred` untuk pengguna yang sedang login.             |
| POST   | `/music/add-ajax/`   | `create_music_ajax` | Validasi dengan`MusicForm`, balas **201** (berhasil), **400** (berisi `errors` per field), atau **403** (bukan pemilik portofolio). |
| POST   | `/music/<id>/star/`  | `toggle_music_star` | Jika request mengirim`Accept: application/json`, balas `{is_starred, star_count}`; submit form biasa tetap di-redirect seperti Tugas 4.               |

`create_music_ajax` sengaja tidak memakai `@owner_required`, karena decorator itu me-redirect pengunjung ke halaman login, sehingga `fetch()` akan menerima HTML halaman login dengan status 200. Hak akses diperiksa langsung di dalam view dengan `can_manage()`, jadi pengunjung, pengguna biasa, dan editor sama-sama mendapat JSON 403.

### Tambah data lewat modal

- Tombol **+ Tambah Musik** (hanya untuk pemilik) membuka modal berisi `MusicForm`. Modal ini memakai komponen bersama [templates/components/form_modal.html](templates/components/form_modal.html) yang juga dipakai Projects.
- Form dikirim dengan `fetch()` + `FormData`. Token CSRF ikut lewat field `csrfmiddlewaretoken` dari `{% csrf_token %}` dan header `X-CSRFToken`.
- Jika berhasil, form di-reset, modal ditutup, toast sukses tampil, dan daftar dimuat ulang tanpa reload halaman. Jika gagal, toast error menampilkan pesan validasi dari server (misalnya *"Judul lagu tidak boleh hanya berisi tag HTML."*).

### Perlindungan XSS

- **Sisi client:** setiap nilai dari server yang masuk ke `innerHTML` melewati `escapeHtml()`, termasuk yang dipakai sebagai atribut (`href`, `src`, `data-name`). Nama musik di modal hapus diisi dengan `textContent`, dan toast juga memakai `textContent`.
- **Sisi server:** `MusicForm` punya `clean_name`, `clean_description`, dan `clean_audio_path` yang menjalankan `strip_tags`. Input yang hanya berisi tag HTML, seperti `<img src="x" onerror="alert('XSS!')">`, ditolak dengan status 400.

### Fitur tambahan

- **Star tanpa reload** di halaman daftar: tombol star diperbarui dari balasan JSON server. Pengunjung yang belum login melihat link *Login untuk star* yang kembali ke halaman ini setelah login.
- Tombol **Edit** (editor dan pemilik) dan **Hapus Musik** (pemilik) tetap ada di setiap card. Modal hapus dipakai bersama oleh semua card; JavaScript hanya mengisi judul dan URL-nya, sedangkan penghapusan tetap lewat form `POST` dengan CSRF.
- Helper `escapeHtml`, `getCookie`, `formatDate`, `buildUrl`, dan `extractErrorMessage` dipindahkan ke [static/js/utils.js](static/js/utils.js) dan dimuat di `base.html`, sehingga Projects dan Music tidak menyalin fungsi yang sama.
- Halaman tambah musik lama (`/music/add/`) tetap ada sebagai fallback jika JavaScript tidak berjalan.
- Test baru di `MusicAjaxTest` ([main/tests.py](main/tests.py)) mencakup halaman kerangka, info star di JSON, status 201/400/403/405, penolakan tanpa token CSRF, `strip_tags`, dan toggle star via JSON.

## Tugas 4: Autentikasi, Otorisasi, dan Star

Bagian portofolio dari Tugas 3 (**Music**) sekarang mengikuti hak akses pengguna. Pola yang sama juga diterapkan ke **Projects**.

### Hak akses

| Peran              | Cara mendapatkan            | Baca daftar & detail |      Star / unstar      |        Ubah data        |    Buat & hapus data    |
| ------------------ | --------------------------- | :------------------: | :---------------------: | :---------------------: | :---------------------: |
| Pengunjung         | tidak login                 |          ✅          | ➡️ diarahkan ke login | ➡️ diarahkan ke login | ➡️ diarahkan ke login |
| Pengguna biasa     | registrasi di`/register/` |          ✅          |           ✅           |         ❌ 403         |         ❌ 403         |
| Editor             | anggota grup`Editor`      |          ✅          |           ✅           |           ✅           |         ❌ 403         |
| Pemilik portofolio | superuser                   |          ✅          |           ✅           |           ✅           |           ✅           |

Pemeriksaan dilakukan di sisi server lewat decorator `editor_required` dan `owner_required` di [main/roles.py](main/roles.py): pengunjung tanpa login di-redirect ke `/login/?next=...`, sedangkan pengguna yang tidak berhak mendapat **HTTP 403 Forbidden**. Tombol tambah/edit/hapus juga disembunyikan di template berdasarkan variabel `can_edit` dan `can_manage` yang dikirim oleh context processor [main/context_processors.py](main/context_processors.py).

### Menetapkan peran Editor

Grup `Editor` dibuat otomatis oleh migrasi `0008_create_editor_group`. Untuk menjadikan seseorang editor:

1. Login ke `/admin/` dengan akun superuser.
2. Buka **Users**, pilih akun yang diinginkan.
3. Pada bagian **Groups**, pindahkan `Editor` ke daftar *Chosen groups*, lalu **Save**.

Setelah login ulang, akun tersebut akan melihat tombol **Edit** pada Music dan Projects, dan label peran di navbar.

### Fitur star

- Model `Music` punya relasi `starred_by = ManyToManyField(User)` (migrasi `0007_music_starred_by`).
- View `toggle_music_star` (dan `toggle_star` untuk Projects) hanya menerima `POST` dengan `{% csrf_token %}`, memberi star jika belum dan membatalkannya jika sudah, jadi tiap pengguna maksimal memberi satu star.
- Jumlah star dan status pengguna (★ Star / ★ Starred) tampil di halaman daftar dan detail. Jumlah star untuk seluruh daftar dihitung dengan dua query saja ([main/stars.py](main/stars.py)).

### Endpoint JSON

`/api/music/` dan `/api/project/` tetap berfungsi (termasuk filter `?title=`), tetapi hanya menyerialisasi field publik. Relasi `starred_by` tidak disertakan agar ID/username pengguna yang memberi star tidak bocor.

### Perubahan lain

- Halaman baru: detail musik (`/music/<id>/`) dan edit musik (`/music/<id>/edit/`).
- Setelah login, pengguna dikembalikan ke halaman asal (`?next=`, hanya untuk URL di host yang sama).
- Pesan sukses (tambah/ubah/hapus) kini tampil di semua halaman, tidak hanya di halaman login.
- Hapus data hanya bisa lewat `POST`.
- Test otomatis untuk keempat peran, fitur star, dan privasi endpoint JSON di [main/tests.py](main/tests.py).

# Dokumentasi

Untuk branching, saya memutuskan menggunakan branch bertahap dari branch dev ke branch main, dengan alasan agar mempermudah proses review dan mengurangi risiko error yang mungkin terjadi.

Untuk setiap fitur baru yang signifikan, akan ada branch baru yang dibuat dari branch dev (contohnya feat/<feature-name></feature>). Dengan melakukan branching bertahap, setiap perubahan dapat diuji secara terpisah sebelum digabungkan ke branch utama, sehingga meminimalkan potensi konflik dan memastikan stabilitas kode.

# AI Disclosure (last upd: Tugas Individu 5)

Saya menggunakan Claude Code dan Copilot (BYOK dengan API key dari DeepSeek), serta Claude via Web Browser untuk membantu proses pembelajaran di Tugas Individu 1 ini. Claude via Web Browser saya gunakan untuk menanyakan konsep-konsep Web Development, sedangkan Claude Code dan Copilot untuk agentic atau untuk pertanyaan yang membutuhkan konteks kode.

Prompt yang saya gunakan:

```
Tugas 5:
1. apakah template html sekarang sudah menampilkan hanya kerangka halaman dan
   fetch data melalui js, atau masih ada yang hardcoded?
2. apa plus minusnya sih pakai jsonresponse dibanding serializer
3. apa itu ajax di javascript (bedanya dengan javascript biasa yang kita pakai apa?) dan apa itu XSS
4. coba lengkapi tugas 5 saya, sesuaikan dengan modul yang ada (music dan project, bukan project saja)
```

* AI menambahkan hal di luar kriteria soal: file `roles.py`, `stars.py`, `context_processors.py`, halaman detail musik, dan proteksi pada Projects. Saya meminta penjelasannya dulu sebelum memutuskan untuk keep apa yang diubah AI. Alasannya masuk akal: tanpa decorator, cek peran harus ditulis ulang di 6 view. Terbukti pula view update/delete Projects dari tutorial sebelumnya bisa diakses tanpa login. Namun, strukturnya jadi berbeda dari pola tutorial, sehingga saya perlu memahami tiap file sebelum commit.
* AI menemukan bahwa `/api/project/` membocorkan username pengguna yang memberi star (`use_natural_foreign_keys`). Saya memverifikasinya lewat output JSON sebelum dan sesudah perbaikan.
* Tugas 5: saya meminta AI mengaudit dulu template mana yang masih dirender server sebelum mengimplementasikan. Hasilnya, Projects sudah AJAX tetapi Music (bagian Tugas 3/4 yang dinilai) masih memakai `{% for %}`, dan pencarian Music hanya mengambil HTML halaman lalu menyalin isi `<ul>`-nya, bukan JSON. AI juga menambahkan hal di luar checklist: toggle star via AJAX, modal hapus bersama, dan `static/js/utils.js`. Keterbatasan yang perlu saya cek sendiri: test Django hanya menguji sisi server, jadi perilaku JavaScript (loading, toast, modal) tetap perlu dicoba manual di browser untuk setiap peran.

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

## Tugas 4

Tidak ada~

### Tugas 5

1. Jelaskan apa itu debouncing dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!

Jawab: Debouncing adalah teknik menunda eksekusi sebuah fungsi sampai event berhenti terjadi selama jeda tertentu. Di halaman Music, setiap event `input` menghapus timer sebelumnya (`clearTimeout`) lalu membuat timer baru 300 ms (`setTimeout`), sehingga request ke `/api/music/?title=` hanya dikirim setelah pengguna berhenti mengetik selama 300 ms.

Tanpa debouncing, mengetik "yorushika" akan mengirim 9 request, satu per huruf. Akibatnya:

- server dan database menerima query yang sebagian besar langsung tidak terpakai,
- daftar berkedip karena dirender ulang terus-menerus,
- bisa terjadi *race condition*: response untuk "yoru" datang lebih lambat daripada response untuk "yorushika" dan menimpa hasil yang benar.

Untuk kasus terakhir, saya juga membatalkan request lama dengan `AbortController`, karena debouncing saja belum cukup jika pengguna berhenti sebentar lalu lanjut mengetik.

2. Jelaskan fungsi dari penggunaan `await` ketika kita menggunakan `fetch()`! Apa yang akan terjadi jika kita tidak menggunakan `await`?

Jawab: `fetch()` bersifat asinkron: ia langsung mengembalikan sebuah `Promise`, bukan data. `await` (hanya bisa dipakai di dalam fungsi `async`) menghentikan sementara eksekusi fungsi tersebut sampai Promise selesai, lalu mengembalikan hasilnya. Selama menunggu, browser tetap responsif karena yang berhenti hanya fungsi itu, bukan seluruh halaman. Di `fetchMusic`, ada dua `await`: yang pertama menunggu `Response` (status dan header), yang kedua `await response.json()` menunggu body selesai dibaca dan diparse.

Tanpa `await`, `response` berisi `Promise`, bukan `Response`, sehingga `response.ok` bernilai `undefined` dan `musicData.length` tidak bisa dipakai. Kode setelahnya berjalan sebelum data tiba, sehingga daftar tidak pernah terisi atau langsung masuk kondisi error. Selain itu, error jaringan tidak tertangkap oleh `try/catch` di sekitarnya karena Promise ditolak setelah blok tersebut selesai dieksekusi. Alternatif tanpa `await` adalah merangkai `.then()` dan `.catch()`, tetapi `async/await` lebih mudah dibaca karena alurnya terlihat berurutan.

3. Jelaskan apa itu serangan XSS (Cross-Site Scripting) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django!

Jawab: XSS adalah serangan di mana penyerang menyisipkan kode (biasanya JavaScript) ke dalam data yang nantinya ditampilkan ke pengguna lain. Contohnya, judul lagu diisi `<img src="x" onerror="alert('XSS!')">`. Jika judul itu dimasukkan ke HTML apa adanya, browser setiap pengunjung akan menjalankan `onerror`. Dalam kasus nyata, isinya bukan `alert`, melainkan kode untuk mencuri data, melakukan aksi atas nama korban (misalnya mengirim POST dengan sesi korban, karena token CSRF bisa dibaca dari halaman yang sama), atau mengubah tampilan halaman.

Template Django melakukan *auto-escaping*: `{{ music.name }}` otomatis mengubah `<` menjadi `&lt;`, `"` menjadi `&quot;`, dan seterusnya, sehingga data tampil sebagai teks kecuali developer sengaja memakai `|safe`. Data dari AJAX tidak melewati template engine. JSON dari server berisi string mentah, dan ketika JavaScript menyisipkannya lewat `innerHTML` atau template literal, browser memperlakukannya sebagai HTML. Jadi perlindungan yang tadinya otomatis hilang, dan developer harus ingat meng-escape setiap nilai secara manual. Satu nilai saja yang terlewat sudah cukup menjadi celah.

Karena itu di halaman Music saya memakai dua lapis pertahanan: `escapeHtml()` atau `textContent` untuk setiap nilai yang ditampilkan lewat JavaScript, dan `strip_tags` di `clean_<field>` pada `MusicForm` agar tag HTML tidak tersimpan di database sejak awal.
