import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from main.forms import MusicForm, ProjectForm
from main.models import Experience, Music, Project
from main.roles import editor_required, owner_required
from main.stars import attach_star_info, toggle_user_star

def safe_next_url(request):
    """Ambil parameter ``next`` hanya jika mengarah ke host ini sendiri."""
    next_url = request.POST.get("next") or request.GET.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return None

def redirect_back(request, fallback, *args, **kwargs):
    """Redirect ke ``next`` (jika aman) atau ke URL ``fallback``."""
    next_url = safe_next_url(request)
    if next_url:
        return redirect(next_url)
    return redirect(fallback, *args, **kwargs)

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "David Liman",
        "form": form,
    }
    return render(request, "register.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        # Kembali ke halaman yang tadinya meminta login (?next=), jika ada.
        response = redirect_back(request, "main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "David Liman",
        "form": form,
        "next": safe_next_url(request) or "",
    }
    return render(request, "login.html", context)

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "David Liman",
        "npm": "2506601956",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia."
        ),
        "last_login": last_login,
    }
    
    return render(request, "index.html", context)

def show_experiences(request):
    context = {
        "name": "David Liman",
        "experiences": Experience.objects.all(),
    }
    return render(request, "experiences.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize(
        "json", projects, use_natural_foreign_keys=True  # Tambahkan argumen ini
    )
    return HttpResponse(projects_json, content_type="application/json")

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "David Liman",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    context = {
        "name": "David Liman",
        "project": project,
    }
    return render(request, "project_detail.html", context)

@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "David Liman",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui!")
        return redirect("main:project_detail", project_id=project.id)

    context = {
        "name": "David Liman",
        "form": form,
        "project": project,
    }
    return render(request, "projects_form.html", context)

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Proyek berhasil dihapus!")

    return redirect("main:show_projects")

def get_music_json(request):
    title_query = request.GET.get("title", "").strip()
    musics = Music.objects.all()

    if title_query:
        musics = musics.filter(name__icontains=title_query)

    musics_json = serializers.serialize("json", musics)
    return HttpResponse(musics_json, content_type="application/json")

def show_music(request):
    json_response = get_music_json(request)

    musics = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    musics = [music.object for music in musics]
    attach_star_info(musics, Music, request.user)
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "David Liman",
        "music_list": musics,
        "title_query": title_query,
    }
    return render(request, "music.html", context)

def music_detail(request, music_id):
    music = get_object_or_404(Music, pk=music_id)
    attach_star_info([music], Music, request.user)

    context = {
        "name": "David Liman",
        "music": music,
    }
    return render(request, "music_detail.html", context)

@owner_required
def create_music(request):
    form = MusicForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Musik baru berhasil ditambahkan!")
        return redirect("main:show_music")

    context = {
        "name": "David Liman",
        "form": form,
    }
    return render(request, "music_form.html", context)

@editor_required
def update_music(request, music_id):
    music = get_object_or_404(Music, pk=music_id)
    form = MusicForm(request.POST or None, instance=music)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Musik berhasil diperbarui!")
        return redirect("main:music_detail", music_id=music.id)

    context = {
        "name": "David Liman",
        "form": form,
        "music": music,
    }
    return render(request, "music_form.html", context)

@owner_required
@require_POST
def delete_music(request, music_id):
    music = get_object_or_404(Music, pk=music_id)
    music.delete()
    messages.success(request, "Musik berhasil dihapus!")
    return redirect("main:show_music")

@login_required
@require_POST
def toggle_music_star(request, music_id):
    music = get_object_or_404(Music, pk=music_id)
    toggle_user_star(music, request.user)
    return redirect_back(request, "main:music_detail", music_id=music.id)

# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star
@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")
