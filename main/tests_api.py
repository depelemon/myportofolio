import uuid
from datetime import date

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import Music, Project
from main.serializers import MusicSerializer, ProjectSerializer


class ProjectAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_superuser("api-owner", password="test-password")
        cls.visitor = User.objects.create_user("api-visitor", password="test-password")
        cls.editor = User.objects.create_user("api-editor")
        cls.editor.groups.add(Group.objects.get(name="Editor"))
        cls.staff = User.objects.create_user("api-staff", is_staff=True)
        cls.project = Project.objects.create(
            title="Portfolio", description="My website", released_at=date(2026, 11, 4),
        )

    def setUp(self):
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "description": "A useful app",
            "released_at": "2026-11-04", "thumbnail": "https://example.com/image.png",
        }

    def test_public_list_and_detail(self):
        self.project.starred_by.add(self.visitor)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertEqual(response.data[0]["star_count"], 1)
        self.assertEqual(set(response.data[0]), {
            "id", "title", "description", "released_at", "thumbnail", "star_count", "is_starred",
        })
        self.assertNotContains(response, self.visitor.username)
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)
        self.assertFalse(ProjectSerializer(self.project).data["is_starred"])

    def test_search_and_empty_results(self):
        self.assertEqual(len(self.client.get(self.list_url, {"title": " PORT "}).data), 1)
        self.assertEqual(self.client.get(self.list_url, {"title": "not-found"}).data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, 404)
        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(self.client.patch(url, {"title": "Changed"}).status_code, 403)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")
        self.assertEqual(Project.objects.count(), 1)

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())
        response = self.client.post(self.list_url, self.payload)
        self.assertEqual(response.status_code, 201)

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"description": "<br>"}, "description"),
            ({"thumbnail": "javascript:alert(1)"}, "thumbnail"),
            ({"released_at": "not-a-date"}, "released_at"),
        ]:
            with self.subTest(changes=changes):
                response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)
        response = self.client.post(self.list_url, '{"title":', content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response = self.client.patch(self.detail_url, {"title": "<b>Clean</b>"}, format="json")
        self.assertEqual(response.data["title"], "Clean")

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        self.project.starred_by.add(self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["star_count"], 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")
        self.assertEqual(self.project.title, "Changed")
        self.assertEqual(self.client.put(self.detail_url, {"title": "Incomplete"}, format="json").status_code, 400)
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 200)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.assertEqual(self.client.get(self.star_url).status_code, 403)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url, {"user": self.owner.pk}, format="json")
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertFalse(self.project.starred_by.filter(pk=self.owner.pk).exists())
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "id": str(self.project.pk), "star_count": 99,
            "is_starred": True, "starred_by_names": "forged", "starred_by": [self.visitor.pk],
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data["id"], str(self.project.pk))
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        for user in (self.staff, self.editor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}).status_code, 403)
            self.assertEqual(self.client.post(self.list_url, self.payload).status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, 405)
        self.assertEqual(self.client.get(self.star_url).status_code, 405)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="api-owner", password="test-password"))
        self.assertEqual(client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(client.patch(self.detail_url, {"title": "Changed"}).status_code, 403)
        self.assertEqual(client.delete(self.detail_url).status_code, 403)
        self.assertEqual(client.post(self.star_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="api-owner", password="test-password")
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, 200)
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.post(self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token).status_code, 201)
        client.logout()
        client.login(username="api-visitor", password="test-password")
        client.cookies.pop("csrftoken", None)
        self.assertEqual(client.get(reverse("main:show_projects")).status_code, 200)
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.post(self.star_url, HTTP_X_CSRFTOKEN=token).status_code, 200)


class MusicAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_superuser("music-owner", password="test-password")
        cls.visitor = User.objects.create_user("music-visitor")
        cls.editor = User.objects.create_user("music-editor")
        cls.editor.groups.add(Group.objects.get(name="Editor"))
        cls.music = Music.objects.create(
            name="Main Menu", description="Piano", released_at=date(2026, 11, 4),
            audio_path="audio/main_menu.mp3",
        )

    def setUp(self):
        self.list_url = reverse("api:music-list")
        self.detail_url = reverse("api:music-detail", args=[self.music.pk])
        self.star_url = reverse("api:music-star", args=[self.music.pk])
        self.payload = {
            "name": "New Music", "description": "Piano arrangement",
            "released_at": "2026-11-04", "audio_path": "static\\audio\\language.mp3",
        }

    def test_public_reads_search_and_privacy(self):
        self.music.starred_by.add(self.visitor)
        response = self.client.get(self.list_url, {"title": " MENU "})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["audio_url"], "/static/audio/main_menu.mp3")
        self.assertNotContains(response, self.visitor.username)
        self.assertNotIn("starred_by", response.data[0])
        self.assertNotIn("starred_by_names", response.data[0])
        self.assertEqual(self.client.get(self.list_url, {"title": "missing"}).data, [])
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)
        self.assertEqual(self.client.get(reverse("api:music-detail", args=[uuid.uuid4()])).status_code, 404)

    def test_owner_crud_and_validation(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["audio_path"], "audio/language.mp3")
        self.assertEqual(response.data["audio_url"], "/static/audio/language.mp3")
        for field in ("name", "description", "audio_path"):
            response = self.client.post(self.list_url, {**self.payload, field: "<br>"}, format="json")
            self.assertEqual(response.status_code, 400)
            self.assertIn(field, response.data)
        self.assertEqual(self.client.patch(self.detail_url, {"name": "<b>Clean</b>"}, format="json").data["name"], "Clean")
        self.assertEqual(self.client.put(self.detail_url, {"name": "Incomplete"}, format="json").status_code, 400)
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 200)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertFalse(Music.objects.filter(pk=self.music.pk).exists())

    def test_editor_can_update_but_cannot_create_or_delete(self):
        self.client.force_authenticate(self.editor)
        response = self.client.patch(self.detail_url, {"name": "Edited"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.music.refresh_from_db()
        self.assertEqual(self.music.name, "Edited")
        self.assertEqual(self.music.description, "Piano")
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 200)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)

    def test_guests_and_regular_users_cannot_manage_music(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user)
            self.assertEqual(self.client.get(self.detail_url).status_code, 200)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"name": "Changed"}).status_code, 403)
            self.assertEqual(self.client.put(self.detail_url, self.payload).status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)

    def test_star_read_only_fields_and_methods(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.client.force_authenticate(self.visitor)
        response = self.client.post(self.star_url, {"user": self.owner.pk})
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertFalse(self.music.starred_by.filter(pk=self.owner.pk).exists())
        self.assertFalse(self.client.post(self.star_url).data["is_starred"])
        self.assertEqual(self.client.get(self.star_url).status_code, 405)
        self.client.force_authenticate(self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "audio_url": "https://example.com/forged.mp3", "starred_by": [self.visitor.pk],
        }, format="json")
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["audio_url"], "/static/audio/language.mp3")

    def test_session_csrf_and_safe_methods(self):
        client = APIClient(enforce_csrf_checks=True)
        client.force_login(self.owner)
        self.assertEqual(client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(client.patch(self.detail_url, {"name": "Changed"}).status_code, 403)
        self.assertEqual(client.delete(self.detail_url).status_code, 403)
        self.assertEqual(client.post(self.star_url).status_code, 403)
        client.get(reverse("main:show_music"))
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.post(self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token).status_code, 201)
        for url in (self.list_url, self.detail_url):
            self.assertEqual(client.head(url).status_code, 200)
            self.assertEqual(client.options(url).status_code, 200)
        self.music.refresh_from_db()
        self.assertEqual(self.music.name, "Main Menu")

    def test_serializers_use_prefetched_stars(self):
        self.music.starred_by.add(self.visitor)
        Music.objects.create(**{
            **{key: value for key, value in self.payload.items() if key != "released_at"},
            "released_at": date(2026, 11, 4),
        })
        with self.assertNumQueries(2):
            data = MusicSerializer(Music.objects.prefetch_related("starred_by"), many=True).data
            self.assertEqual(len(data), 2)
