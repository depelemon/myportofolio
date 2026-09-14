from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Music


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
            started_at=timezone.now(),
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experiences")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experiences"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experiences.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experiences"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experiences"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")


class MusicTest(TestCase):
    def test_music_url_uses_music_template(self):
        response = self.client.get(reverse("main:show_music"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "music.html")
        self.assertContains(response, f'href="{reverse("main:show_music")}"')

    def test_music_page_shows_music_data(self):
        music = Music.objects.create(
            name="Lagu Tugas Akhir",
            description="Aransemen piano untuk tugas akhir semester.",
            released_at=date(2026, 5, 17),
            audio_path="audio/lagu-tugas-akhir.mp3",
        )
        response = self.client.get(reverse("main:show_music"))

        self.assertContains(response, music.name)
        self.assertContains(response, music.description)
        self.assertContains(response, "17 May 2026")
        self.assertContains(response, 'src="/static/audio/lagu-tugas-akhir.mp3"')
        self.assertNotContains(response, "Belum ada musik yang ditambahkan.")

    def test_music_audio_path_is_normalized(self):
        music = Music.objects.create(
            name="Main Menu",
            description="Musik menu utama.",
            released_at=date(2026, 9, 14),
            audio_path="static\\audio\\main_menu.mp3",
        )

        self.assertEqual(music.audio_path, "audio/main_menu.mp3")

    def test_empty_music_page_shows_empty_message(self):
        response = self.client.get(reverse("main:show_music"))

        self.assertContains(response, "Belum ada musik yang ditambahkan.")