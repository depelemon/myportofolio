// Helper bersama untuk halaman yang memuat data lewat AJAX (Projects, Music).
// Dimuat dari base.html sehingga tersedia di semua halaman.

// Mengubah karakter khusus HTML menjadi entity agar ditampilkan sebagai teks.
// Data yang dirakit lewat innerHTML tidak lagi di-escape otomatis oleh Django.
function escapeHtml(value) {
    return String(value ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
}

// Membaca nilai cookie, digunakan untuk mengambil token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Format tanggal "YYYY-MM-DD" menjadi "01 Sep 2026" tanpa pergeseran zona waktu
function formatDate(isoDate) {
    const date = new Date(isoDate);
    if (Number.isNaN(date.getTime())) return '';
    return date.toLocaleDateString('en-GB', {
        day: '2-digit', month: 'short', year: 'numeric', timeZone: 'UTC',
    });
}

// Ganti UUID placeholder pada URL hasil {% url %} dengan ID sebenarnya
const URL_ID_PLACEHOLDER = '00000000-0000-0000-0000-000000000000';

function buildUrl(urlTemplate, id) {
    return urlTemplate.replace(URL_ID_PLACEHOLDER, encodeURIComponent(id));
}

// Ubah respons error JSON dari view AJAX menjadi satu kalimat untuk toast.
// Respons 400 berisi {"errors": {field: [{message}]}}, respons lain {"message"}.
function extractErrorMessage(result, status) {
    if (result && result.errors) {
        return Object.values(result.errors).flat().map(error => error.message).join(' ');
    }
    return (result && result.message) || `Terjadi kesalahan (status ${status}).`;
}
