from rest_framework.permissions import BasePermission, SAFE_METHODS

from main.roles import can_edit, can_manage


class IsPortfolioOwnerOrReadOnly(BasePermission):
    message = "Hanya pemilik portofolio yang dapat mengelola proyek melalui API."

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or can_manage(request.user)


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    message = "Hanya pemilik yang dapat menambah/menghapus; Editor dapat mengubah data."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        return can_manage(request.user) or (
            request.method in ("PUT", "PATCH") and can_edit(request.user)
        )
