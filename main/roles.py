"""Aturan hak akses (otorisasi) untuk data portofolio.

Ada empat peran yang dikenali:

- Pengunjung tanpa login: hanya dapat membaca data.
- Pengguna biasa: dapat membaca data serta memberi/membatalkan star.
- Editor (anggota grup ``Editor``): hak pengguna biasa + mengubah data.
- Pemilik portofolio (superuser): hak pengguna biasa + membuat, mengubah,
  dan menghapus data.

Keanggotaan grup ``Editor`` diatur lewat Django Admin; grupnya sendiri
dibuat otomatis oleh migrasi ``0008_create_editor_group``.
"""

from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

EDITOR_GROUP = "Editor"


def is_editor(user):
    """True jika ``user`` anggota grup Editor (hasilnya di-cache per request)."""
    if not user.is_authenticated:
        return False
    if not hasattr(user, "_is_editor"):
        user._is_editor = user.groups.filter(name=EDITOR_GROUP).exists()
    return user._is_editor


def can_edit(user):
    """Boleh mengubah data: pemilik portofolio atau editor."""
    return user.is_superuser or is_editor(user)


def can_manage(user):
    """Boleh membuat dan menghapus data: hanya pemilik portofolio."""
    return user.is_superuser


def role_required(check):
    """Decorator view: wajib login, lalu 403 jika ``check(user)`` gagal.

    Pengunjung tanpa login di-redirect ke halaman login (``LOGIN_URL``),
    sedangkan pengguna yang sudah login tetapi tidak berhak mendapat
    HTTP 403 Forbidden.
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if not check(request.user):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return login_required(wrapped)

    return decorator


editor_required = role_required(can_edit)
owner_required = role_required(can_manage)
