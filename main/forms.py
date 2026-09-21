from django.forms import ModelForm, TextInput, Textarea, DateInput, URLInput

from main.models import Music, Project

class MusicForm(ModelForm):
    class Meta:
        model = Music
        fields = [
            "name",
            "description",
            "released_at",
            "audio_path",
        ]

        labels = {
            "name": "Judul Lagu",
            "description": "Deskripsi Lagu",
            "released_at": "Tanggal Rilis",
            "audio_path": "Path Audio",
        }

        widgets = {
            "name": TextInput(
                attrs={
                    "placeholder": "Lagu Tugas Akhir",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Lagumu",
                    "rows": 3,
                }
            ),
            "released_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "audio_path": TextInput(
                attrs={
                    "placeholder": "audio/lagu-tugas-akhir.mp3",
                    "maxlength": 255,
                }
            ),
        }


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "released_at",
            "thumbnail",
        ]

        labels = {
            "title": "Judul Proyek",
            "description": "Deskripsi Proyek",
            "released_at": "Tanggal Rilis",
            "thumbnail": "URL Thumbnail",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Website Portofolio",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 4,
                }
            ),
            "released_at": DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                },
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://example.com/thumbnail.png",
                }
            ),
        }
