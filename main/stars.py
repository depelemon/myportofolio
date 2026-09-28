"""Helper fitur star untuk model yang punya relasi ``starred_by``."""

from django.db.models import Count


def toggle_user_star(obj, user):
    """Beri star jika belum, batalkan jika sudah (maks. satu star per user).

    Mengembalikan ``True`` jika setelah pemanggilan ``obj`` di-star oleh
    ``user``. ManyToManyField menyimpan pasangan (obj, user) secara unik,
    jadi ``add`` berulang tidak akan menggandakan star.
    """
    if obj.starred_by.filter(pk=user.pk).exists():
        obj.starred_by.remove(user)
        return False
    obj.starred_by.add(user)
    return True


def attach_star_info(objects, model, user):
    """Isi ``star_count`` dan ``is_starred`` pada tiap objek di ``objects``.

    Cukup dua query untuk seluruh daftar, alih-alih dua query per objek
    jika dihitung langsung di template.
    """
    ids = [obj.pk for obj in objects]
    counts = dict(
        model.objects.filter(pk__in=ids)
        .annotate(star_count=Count("starred_by"))
        .values_list("pk", "star_count")
    )
    starred_ids = set()
    if user.is_authenticated:
        starred_ids = set(
            model.objects.filter(pk__in=ids, starred_by=user)
            .values_list("pk", flat=True)
        )

    for obj in objects:
        obj.star_count = counts.get(obj.pk, 0)
        obj.is_starred = obj.pk in starred_ids
    return objects
