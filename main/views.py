import json


from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from django.conf import settings

from main.forms import MusicForm
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

