import json
import datetime

from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied        

from django.conf import settings

from main.forms import MusicForm, ProjectForm
from main.models import Experience, Music, Project

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Burhan",
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
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "David Liman",
        "form": form,
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
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "David Liman",
        "music_list": musics,
        "title_query": title_query,
    }
    return render(request, "music.html", context)

def delete_music(request, music_id):
    music = get_object_or_404(Music, pk=music_id)

    if request.method == "POST":
        music.delete()
        messages.success(request, "Musik berhasil dihapus!")
        return redirect("main:show_music")

    return redirect("main:show_music")

@login_required(login_url="/login/")
def create_music(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
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
