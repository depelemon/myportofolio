# Log bantuan AI - Tugas 6

- Tanggal: 9 November 2026 (WIB).
- Alat: OpenAI Codex di aplikasi desktop.
- Materi pengguna: `tugas-6.pdf` dan checkout proyek portofolio yang sedang terbuka.
- Prompt pengguna: `do the task given`.

## Ringkasan proses

1. Membaca PDF sebagai spesifikasi tugas dan memeriksa kode Music, Projects, role,
   serializer, permission, view API, template, dan test yang sudah ada.
2. Menemukan API Music sudah tersedia dari pekerjaan sebelumnya, tetapi tombol edit
   pada daftar masih menuju form HTML yang menyimpan lewat POST biasa.
3. Menambahkan modal edit pada daftar Music: GET detail terbaru, isi form melalui
   properti `value`, dan PATCH melalui helper `writeApi` yang menyertakan CSRF.
4. Memperluas APITestCase agar penolakan juga memeriksa database, menguji login nyata
   untuk CSRF, cookie pengguna biasa/Editor, validasi update, star, dan objek hilang.
5. Menyusun progres mingguan, cara verifikasi, dan draf jawaban reflektif bahasa Indonesia.
   Referensi konsep berasal dari dokumentasi DRF, MDN, dan disertasi Roy Fielding.

## Batasan dan tanggung jawab

Ini ringkasan prompt dan tindakan, bukan transkrip lengkap atau klaim pengerjaan manual.
Kode API yang sudah ada dipertahankan; seluruh implementasi tidak diklaim dibuat di sesi ini.
Test Django memeriksa server dan render template, tetapi perlu dilengkapi percobaan browser
untuk interaksi JavaScript. Pemilik tetap perlu memahami perubahan, meninjau jawaban
reflektif, dan mengurus commit/push serta submisi SCELE. AI tidak dapat membuktikan
bahwa prasyarat Tutorial 7 selesai sebelum tenggat sebelumnya.

## Hasil verifikasi sesi ini

- `python manage.py test main`: 77 test lulus, termasuk test Tutorial 7.
- `python manage.py check`: tidak ada masalah.
- `python manage.py makemigrations --check --dry-run`: tidak ada perubahan model.
- Server development berjalan; `/music/`, `/projects/`, serta JSON dan Browsable API
  untuk `/api/v1/music/` dan `/api/v1/projects/` mengembalikan HTTP 200.
- JavaScript hasil render Music lolos pemeriksaan sintaks Node untuk keempat peran;
  seluruh ID HTML pada masing-masing hasil render unik.
- Preview browser mengalami timeout. Klik modal, toast, dan pemutaran audio belum
  diverifikasi secara langsung melalui browser dalam sesi ini.
- Tidak melakukan commit, push, deployment, perubahan visibilitas repositori,
  atau pengumpulan SCELE.
