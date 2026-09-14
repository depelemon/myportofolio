import json

from django.conf import settings
from django.shortcuts import render

from main.models import Experience, Music

def show_main(request):
    context = {
        "name": "David Liman",
        "npm": "2506601956",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia."
        ),
    }
    
    return render(request, "index.html", context)


def show_experiences(request):
    context = {
        "name": "David Liman",
        "experiences": Experience.objects.all(),
    }
    return render(request, "experiences.html", context)

def projects_page(request):
    return render(request, "projects.html", {"name": "David Liman"})

def show_music(request):
    context = {
        "name": "David Liman",
        "music_list": Music.objects.all(),
    }
    return render(request, "music.html", context)
