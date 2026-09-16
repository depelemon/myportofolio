from django.forms import ModelForm, TextInput, Textarea, DateInput

from main.models import Music

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
