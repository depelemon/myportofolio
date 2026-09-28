from main.roles import can_edit, can_manage, is_editor


def user_roles(request):
    """Kirim status peran pengguna ke semua template.

    Dipakai untuk menyembunyikan tombol aksi yang tidak boleh dipakai;
    pemeriksaan sebenarnya tetap dilakukan di view (lihat ``main.roles``).
    """
    user = request.user
    return {
        "is_editor": is_editor(user),
        "can_edit": can_edit(user),
        "can_manage": can_manage(user),
    }
