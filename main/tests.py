import json
from datetime import date

from django.contrib.auth.models import AnonymousUser, Group, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Music, Project
from main.roles import EDITOR_GROUP, can_edit, can_manage, is_editor


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
        response = self.client.get(reverse("main:get_music_json"))
        item = response.json()[0]

        self.assertEqual(item["pk"], str(music.id))
        self.assertEqual(item["fields"]["name"], music.name)
        self.assertEqual(item["fields"]["description"], music.description)
        self.assertEqual(item["fields"]["released_at"], "2026-05-17")
        self.assertEqual(
            item["fields"]["audio_url"], "/static/audio/lagu-tugas-akhir.mp3"
        )

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


class RoleTestMixin:
    """Siapkan satu akun untuk tiap peran: biasa, editor, dan pemilik."""

    password = "Rahasia-PBP-2026"

    @classmethod
    def setUpTestData(cls):
        # Dibuat sekali per kelas (hashing password cukup lambat); TestCase
        # mengembalikan state database dan atribut ini untuk tiap tes.
        cls.user = User.objects.create_user("biasa", password=cls.password)
        cls.editor = User.objects.create_user("editor", password=cls.password)
        cls.editor.groups.add(Group.objects.get(name=EDITOR_GROUP))
        cls.owner = User.objects.create_superuser(
            "pemilik", password=cls.password
        )
        cls.music = Music.objects.create(
            name="Main Menu",
            description="Musik menu utama.",
            released_at=date(2026, 9, 14),
            audio_path="audio/main_menu.mp3",
        )
        cls.project = Project.objects.create(
            title="Website Portofolio",
            description="Portofolio pribadi.",
            released_at=date(2026, 9, 1),
        )

    def login_as(self, user):
        self.client.force_login(user)

    def music_payload(self, **overrides):
        payload = {
            "name": "Lagu Baru",
            "description": "Deskripsi lagu.",
            "released_at": "2026-09-20",
            "audio_path": "audio/language.mp3",
        }
        payload.update(overrides)
        return payload


class RoleHelperTest(RoleTestMixin, TestCase):
    def test_editor_group_is_created_by_migration(self):
        self.assertTrue(Group.objects.filter(name=EDITOR_GROUP).exists())

    def test_role_checks(self):
        anonymous = AnonymousUser()
        self.assertFalse(can_edit(anonymous))
        self.assertFalse(can_edit(self.user))
        self.assertTrue(is_editor(self.editor))
        self.assertTrue(can_edit(self.editor))
        self.assertFalse(can_manage(self.editor))
        self.assertTrue(can_edit(self.owner))
        self.assertTrue(can_manage(self.owner))


class MusicAuthorizationTest(RoleTestMixin, TestCase):
    def test_anyone_can_read_list_and_detail(self):
        self.assertEqual(self.client.get(reverse("main:show_music")).status_code, 200)
        response = self.client.get(reverse("main:music_detail", args=[self.music.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.music.name)

    def test_anonymous_is_redirected_to_login(self):
        urls = [
            reverse("main:create_music"),
            reverse("main:update_music", args=[self.music.id]),
            reverse("main:delete_music", args=[self.music.id]),
            reverse("main:toggle_music_star", args=[self.music.id]),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.post(url)
                self.assertRedirects(
                    response,
                    f"{reverse('main:login')}?next={url}",
                    fetch_redirect_response=False,
                )
        self.assertTrue(Music.objects.filter(pk=self.music.pk).exists())

    def test_regular_user_gets_403_for_changes(self):
        self.login_as(self.user)
        self.assertEqual(self.client.get(reverse("main:create_music")).status_code, 403)
        self.assertEqual(
            self.client.post(
                reverse("main:update_music", args=[self.music.id]),
                self.music_payload(),
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.post(reverse("main:delete_music", args=[self.music.id])).status_code,
            403,
        )
        self.music.refresh_from_db()
        self.assertEqual(self.music.name, "Main Menu")

    def test_editor_can_update_but_not_create_or_delete(self):
        self.login_as(self.editor)
        response = self.client.post(
            reverse("main:update_music", args=[self.music.id]),
            self.music_payload(name="Main Menu (Remaster)"),
        )
        self.assertRedirects(response, reverse("main:music_detail", args=[self.music.id]))
        self.music.refresh_from_db()
        self.assertEqual(self.music.name, "Main Menu (Remaster)")

        self.assertEqual(
            self.client.post(reverse("main:create_music"), self.music_payload()).status_code,
            403,
        )
        self.assertEqual(
            self.client.post(reverse("main:delete_music", args=[self.music.id])).status_code,
            403,
        )
        self.assertEqual(Music.objects.count(), 1)

    def test_owner_can_create_update_and_delete(self):
        self.login_as(self.owner)
        self.client.post(reverse("main:create_music"), self.music_payload())
        self.assertTrue(Music.objects.filter(name="Lagu Baru").exists())

        self.client.post(
            reverse("main:update_music", args=[self.music.id]),
            self.music_payload(name="Diubah Pemilik"),
        )
        self.music.refresh_from_db()
        self.assertEqual(self.music.name, "Diubah Pemilik")

        self.client.post(reverse("main:delete_music", args=[self.music.id]))
        self.assertFalse(Music.objects.filter(pk=self.music.pk).exists())

    def test_delete_requires_post(self):
        self.login_as(self.owner)
        response = self.client.get(reverse("main:delete_music", args=[self.music.id]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Music.objects.filter(pk=self.music.pk).exists())

    def test_controls_are_hidden_by_role(self):
        # Tombol per card dirender JavaScript berdasarkan flag ini; modal
        # tambah dan hapus hanya ada di HTML milik pemilik portofolio.
        cases = [
            (None, False, False),
            (self.user, False, False),
            (self.editor, True, False),
            (self.owner, True, True),
        ]
        for account, sees_edit, sees_manage in cases:
            with self.subTest(account=account):
                self.client.logout()
                if account:
                    self.login_as(account)
                content = self.client.get(reverse("main:show_music")).content.decode()
                self.assertIn(
                    f'const CAN_EDIT = "{str(sees_edit).lower()}" === "true";',
                    content,
                )
                self.assertIn(
                    f'const CAN_MANAGE = "{str(sees_manage).lower()}" === "true";',
                    content,
                )
                self.assertEqual('id="add-music-modal"' in content, sees_manage)
                self.assertEqual('id="delete-music-modal"' in content, sees_manage)


class MusicStarTest(RoleTestMixin, TestCase):
    def toggle(self, **data):
        return self.client.post(
            reverse("main:toggle_music_star", args=[self.music.id]), data
        )

    def test_toggle_star_adds_then_removes_one_star(self):
        self.login_as(self.user)
        self.toggle()
        self.assertTrue(self.music.starred_by.filter(pk=self.user.pk).exists())
        self.assertEqual(self.music.starred_by.count(), 1)

        self.toggle()
        self.assertEqual(self.music.starred_by.count(), 0)

    def test_star_count_and_status_are_shown(self):
        self.music.starred_by.add(self.editor, self.owner)
        self.login_as(self.user)
        response = self.client.get(reverse("main:music_detail", args=[self.music.id]))
        self.assertContains(response, '<span class="star-count">2</span>', html=True)
        self.assertContains(response, 'aria-pressed="false"')

        self.toggle()
        response = self.client.get(reverse("main:music_detail", args=[self.music.id]))
        self.assertContains(response, '<span class="star-count">3</span>', html=True)
        self.assertContains(response, 'aria-pressed="true"')

    def test_toggle_star_requires_post(self):
        self.login_as(self.user)
        response = self.client.get(reverse("main:toggle_music_star", args=[self.music.id]))
        self.assertEqual(response.status_code, 405)

    def test_toggle_star_redirects_to_safe_next_only(self):
        self.login_as(self.user)
        response = self.toggle(next=reverse("main:show_music"))
        self.assertRedirects(response, reverse("main:show_music"))

        response = self.toggle(next="https://evil.example.com/")
        self.assertRedirects(
            response, reverse("main:music_detail", args=[self.music.id])
        )

    def test_list_uses_constant_number_of_queries(self):
        for i in range(5):
            music = Music.objects.create(
                name=f"Lagu {i}",
                description="-",
                released_at=date(2026, 1, i + 1),
                audio_path="audio/language.mp3",
            )
            music.starred_by.add(self.user)
        self.login_as(self.user)
        # sesi, user, daftar musik, jumlah star, dan status star pengguna.
        with self.assertNumQueries(5):
            self.client.get(reverse("main:get_music_json"))


class ProjectAuthorizationTest(RoleTestMixin, TestCase):
    def project_payload(self, **overrides):
        payload = {
            "title": "Proyek Baru",
            "description": "Deskripsi.",
            "released_at": "2026-09-20",
            "thumbnail": "",
        }
        payload.update(overrides)
        return payload

    def test_anonymous_cannot_update_or_delete(self):
        url = reverse("main:update_project", args=[self.project.id])
        response = self.client.post(url, self.project_payload())
        self.assertRedirects(
            response, f"{reverse('main:login')}?next={url}", fetch_redirect_response=False
        )
        self.client.post(reverse("main:delete_project", args=[self.project.id]))
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())

    def test_regular_user_gets_403(self):
        self.login_as(self.user)
        response = self.client.get(reverse("main:update_project", args=[self.project.id]))
        self.assertEqual(response.status_code, 403)

    def test_editor_can_update_but_not_delete(self):
        self.login_as(self.editor)
        self.client.post(
            reverse("main:update_project", args=[self.project.id]),
            self.project_payload(title="Diubah Editor"),
        )
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Diubah Editor")
        self.assertEqual(
            self.client.post(reverse("main:delete_project", args=[self.project.id])).status_code,
            403,
        )

    def test_owner_can_delete(self):
        self.login_as(self.owner)
        self.client.post(reverse("main:delete_project", args=[self.project.id]))
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_regular_user_can_star_project(self):
        self.login_as(self.user)
        self.client.post(reverse("main:toggle_star", args=[self.project.id]))
        self.assertEqual(self.project.starred_by.count(), 1)


class JsonEndpointTest(RoleTestMixin, TestCase):
    def test_json_does_not_expose_starring_users(self):
        self.music.starred_by.add(self.user)
        self.project.starred_by.add(self.user)

        for url_name in ("main:get_music_json", "main:get_projects_json"):
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 200)
                data = json.loads(response.content)
                self.assertEqual(len(data), 1)
                self.assertNotIn("starred_by", data[0]["fields"])
                self.assertNotContains(response, self.user.username)

    def test_json_title_filter_still_works(self):
        response = self.client.get(reverse("main:get_music_json"), {"title": "menu"})
        self.assertEqual(json.loads(response.content)[0]["fields"]["name"], "Main Menu")
        response = self.client.get(reverse("main:get_music_json"), {"title": "xyz"})
        self.assertEqual(json.loads(response.content), [])


class LoginRedirectTest(RoleTestMixin, TestCase):
    def test_login_returns_to_next_and_sets_cookie(self):
        next_url = reverse("main:music_detail", args=[self.music.id])
        response = self.client.post(
            reverse("main:login"),
            {"username": "biasa", "password": self.password, "next": next_url},
        )
        self.assertRedirects(response, next_url)
        self.assertIn("last_login", response.cookies)

    def test_login_ignores_external_next(self):
        response = self.client.post(
            reverse("main:login"),
            {
                "username": "biasa",
                "password": self.password,
                "next": "https://evil.example.com/",
            },
        )
        self.assertRedirects(response, reverse("main:show_main"))

class ProjectAjaxTest(RoleTestMixin, TestCase):
    def payload(self, **overrides):
        payload = {
            "title": "Proyek AJAX",
            "description": "Deskripsi.",
            "released_at": "2026-09-20",
            "thumbnail": "",
        }
        payload.update(overrides)
        return payload

    def test_projects_page_has_no_server_rendered_list(self):
        response = self.client.get(reverse("main:show_projects"))
        self.assertNotContains(response, self.project.title)
        self.assertContains(response, 'id="grid"')

    def test_json_includes_star_info_for_current_user_only(self):
        self.project.starred_by.add(self.user)
        url = reverse("main:get_projects_json")

        fields = json.loads(self.client.get(url).content)[0]["fields"]
        self.assertEqual(fields["star_count"], 1)
        self.assertFalse(fields["is_starred"])

        self.login_as(self.user)
        fields = json.loads(self.client.get(url).content)[0]["fields"]
        self.assertTrue(fields["is_starred"])

    def test_owner_can_create_via_ajax(self):
        self.login_as(self.owner)
        response = self.client.post(reverse("main:create_project_ajax"), self.payload())
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Project.objects.filter(title="Proyek AJAX").exists())

    def test_anonymous_editor_and_regular_user_get_json_403(self):
        url = reverse("main:create_project_ajax")
        for user in (None, self.user, self.editor):
            with self.subTest(user=user):
                self.client.logout()
                if user:
                    self.login_as(user)
                response = self.client.post(url, self.payload())
                self.assertEqual(response.status_code, 403)
                self.assertIn("message", response.json())
        self.assertFalse(Project.objects.filter(title="Proyek AJAX").exists())

    def test_create_ajax_requires_post(self):
        self.login_as(self.owner)
        response = self.client.get(reverse("main:create_project_ajax"))
        self.assertEqual(response.status_code, 405)

    def test_invalid_data_returns_400_with_errors(self):
        self.login_as(self.owner)
        response = self.client.post(
            reverse("main:create_project_ajax"), self.payload(title="   ")
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.json()["errors"])

    def test_html_is_stripped_and_html_only_title_rejected(self):
        self.login_as(self.owner)
        url = reverse("main:create_project_ajax")
        self.client.post(url, self.payload(title="Halo <b>dunia</b>"))
        self.assertTrue(Project.objects.filter(title="Halo dunia").exists())

        response = self.client.post(
            url, self.payload(title="<img src=x onerror=alert(1)>")
        )
        self.assertEqual(response.status_code, 400)

    def test_javascript_url_thumbnail_is_rejected(self):
        self.login_as(self.owner)
        response = self.client.post(
            reverse("main:create_project_ajax"),
            self.payload(thumbnail="javascript:alert(1)"),
        )
        self.assertEqual(response.status_code, 400)

    def test_add_modal_only_for_owner(self):
        url = reverse("main:show_projects")
        self.assertNotContains(self.client.get(url), 'id="add-project-modal"')
        self.login_as(self.editor)
        self.assertNotContains(self.client.get(url), 'id="add-project-modal"')
        self.login_as(self.owner)
        self.assertContains(self.client.get(url), 'id="add-project-modal"')


class MusicAjaxTest(RoleTestMixin, TestCase):
    def test_music_page_has_no_server_rendered_list(self):
        response = self.client.get(reverse("main:show_music"))
        self.assertNotContains(response, self.music.name)
        for element_id in ("music-list", "music-loading", "music-error", "music-empty"):
            self.assertContains(response, f'id="{element_id}"')

    def test_json_includes_star_info_for_current_user_only(self):
        self.music.starred_by.add(self.user)
        url = reverse("main:get_music_json")

        fields = self.client.get(url).json()[0]["fields"]
        self.assertEqual(fields["star_count"], 1)
        self.assertFalse(fields["is_starred"])

        self.login_as(self.user)
        fields = self.client.get(url).json()[0]["fields"]
        self.assertTrue(fields["is_starred"])

    def test_owner_can_create_via_ajax(self):
        self.login_as(self.owner)
        response = self.client.post(
            reverse("main:create_music_ajax"), self.music_payload()
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Music.objects.filter(name="Lagu Baru").exists())

    def test_anonymous_editor_and_regular_user_get_json_403(self):
        url = reverse("main:create_music_ajax")
        for user in (None, self.user, self.editor):
            with self.subTest(user=user):
                self.client.logout()
                if user:
                    self.login_as(user)
                response = self.client.post(url, self.music_payload())
                self.assertEqual(response.status_code, 403)
                self.assertIn("message", response.json())
        self.assertFalse(Music.objects.filter(name="Lagu Baru").exists())

    def test_create_ajax_requires_post(self):
        self.login_as(self.owner)
        response = self.client.get(reverse("main:create_music_ajax"))
        self.assertEqual(response.status_code, 405)

    def test_create_ajax_enforces_csrf(self):
        client = self.client_class(enforce_csrf_checks=True)
        client.force_login(self.owner)
        response = client.post(reverse("main:create_music_ajax"), self.music_payload())
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Music.objects.filter(name="Lagu Baru").exists())

    def test_invalid_data_returns_400_with_errors(self):
        self.login_as(self.owner)
        response = self.client.post(
            reverse("main:create_music_ajax"),
            self.music_payload(name="   ", released_at="bukan-tanggal"),
        )
        self.assertEqual(response.status_code, 400)
        errors = response.json()["errors"]
        self.assertIn("name", errors)
        self.assertIn("released_at", errors)

    def test_html_is_stripped_and_html_only_name_rejected(self):
        self.login_as(self.owner)
        url = reverse("main:create_music_ajax")
        self.client.post(
            url,
            self.music_payload(
                name="Halo <b>dunia</b>",
                description="<script>alert(1)</script>Lagu santai",
            ),
        )
        music = Music.objects.get(name="Halo dunia")
        self.assertEqual(music.description, "alert(1)Lagu santai")

        response = self.client.post(
            url, self.music_payload(name="<img src=\"x\" onerror=\"alert('XSS!')\">")
        )
        self.assertEqual(response.status_code, 400)

    def test_add_modal_only_for_owner(self):
        url = reverse("main:show_music")
        self.assertNotContains(self.client.get(url), 'id="add-music-modal"')
        self.login_as(self.editor)
        self.assertNotContains(self.client.get(url), 'id="add-music-modal"')
        self.login_as(self.owner)
        self.assertContains(self.client.get(url), 'id="add-music-modal"')

    def test_star_toggle_returns_json_for_fetch(self):
        self.login_as(self.user)
        url = reverse("main:toggle_music_star", args=[self.music.id])

        response = self.client.post(url, HTTP_ACCEPT="application/json")
        self.assertEqual(response.json(), {"is_starred": True, "star_count": 1})

        response = self.client.post(url, HTTP_ACCEPT="application/json")
        self.assertEqual(response.json(), {"is_starred": False, "star_count": 0})
