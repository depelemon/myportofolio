# Data Diri

Nama : David Liman

NPM : 2506601956

Kelas : PBP B

# Dokumentasi & AI Disclosure

Untuk branching, saya memutuskan menggunakan branch bertahap dari branch dev ke branch main, dengan alasan agar mempermudah proses review dan mengurangi risiko error yang mungkin terjadi.

Untuk setiap fitur baru yang signifikan, akan ada branch baru yang dibuat dari branch dev (contohnya feat/<feature-name></feature>). Dengan melakukan branching bertahap, setiap perubahan dapat diuji secara terpisah sebelum digabungkan ke branch utama, sehingga meminimalkan potensi konflik dan memastikan stabilitas kode.

AI Disclosure: saya menggunakan Claude Code dan Copilot (BYOK dengan API key dari DeepSeek), serta Claude via Web Browser untuk membantu proses pembelajaran di Tugas Individu 1 ini. Claude via Web Browser saya gunakan untuk menanyakan konsep-konsep Web Development, sedangkan Claude Code dan Copilot untuk agentic atau untuk pertanyaan yang membutuhkan konteks kode. (Kenapa ganti agent? token Claude Codenya habis hehe)

Contoh prompt yang saya gunakan:

1. "how does django url routing work"
2. "if i want to use tailwind, what do i need to change. currently it should be plain css" (scrapped, decided to use plain css for now)
3. "i want to change the navbar to navigate different pages: home, projects, portfolio, but for that i need to add new pages first right? how to do that"
4. "style the experiences section"
5. "currently the experiences section use a hardcoded entries, can i input the data to a json or somewhere else and make the html take the repetiting part?"
6. "explain what is combinator in css, and how does it get used?"

Selengkapnya bisa dilihat di log Claude Code dalam bentuk JSONL [di sini](https://drive.google.com/file/d/1KjL9q7culyguhu6OkjKNOqsV1QGT4Cgc/view?usp=sharing).

# Pertanyaan Reflektif

### Tugas 1

1. Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti \<section\>, \<article\>, atau \<aside\>? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?

Jawab: Saya menggunakan elemen semantik, tapi tidak semuanya, contohnya saya menggunakan \<section\> untuk grouping konten yang berbeda-beda seperti About Me, Experiences (dan section lain yang nantinya akan ditambahkan). Elemen ini jadi best practice untuk membuat struktur HTML lebih mudah dipahami, lebih konsisten antar halaman, dan lebih mudah diakses search engine atau mesin scraper untuk memahami apa yang ada di website saya. Saya tidak menggunakan \<article\> atau \<aside\> karena project saat ini masih sederhana, dan belum ada use casenya di design yang saya pikirkan.

2. Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?

Jawab:  Karena keterbatasan waktu, saya hanya sempat mengimplementasikan styling untuk desktop-view, dan tidak terlalu memperhatikan responsiveness, tetapi karena bagian yang saya kerjakan di tugas ini adalah section Experiences yang berbentuk timeline, layout-nya sudah responsif by design. Tantangan yang saya temui justru ada di elemen dekoratifnya: garis vertikal dan titik penanda timeline diposisikan dengan offset kiri yang tetap, jadi saya harus memastikan penanda selalu sejajar dengan judul tiap entri dan teks tidak menabrak garis saat layar menyempit. Selain itu, karena tiap entri kini berisi poin-poin deskripsi, saya menambah jarak vertikal antar entri agar satu pengalaman tidak menyatu dengan pengalaman berikutnya. Untuk mengevaluasi elemen mana yang diprioritaskan, saya berpatokan pada hierarki konten: judul entri adalah elemen utama (penanda timeline harus sejajar dengannya), lalu meta, dan poin deskripsi paling akhir, sehingga yang dikorbankan saat layar sempit adalah hal-hal dekoratif, bukan teksnya.

3. Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?

Jawab: Batasannya jelas tidak bisa menampilkan data secara dinamis, tetapi karena isi webnya memang masih sedikit (dan belum berisi semua section yang saya plan, karena sekali lagi keterbatasan waktu, maaf kak), jadi memang belum memerlukan database untuk data dinamis. Untuk iterasi selanjutnya, karena ini project portofolio, sepertinya keperluan databasenya tidak terlalu mendesak? Mungkin saya ingin merefactor bagian entri-entri untuk section Experiences (yang sekarang saya simpan di /portofolio/data/experiences.json) agar diimport ke database, dan menambahkan endpoint untuk mengakses data tersebut. Selain itu, mungkin menyimpan foto-foto project di database juga.




