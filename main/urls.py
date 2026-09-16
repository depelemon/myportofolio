from django.urls import path

from main.views import create_music, delete_music, get_music_json, show_main, show_experiences, projects_page, show_music

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experiences/", show_experiences, name="show_experiences"),
    path('projects/', projects_page, name='projects_page'),
    path('music/', show_music, name='show_music'),
    path("music/add/", create_music, name="create_music"),
    path("music/<uuid:music_id>/delete/", delete_music, name="delete_music"),
    path("api/music/", get_music_json, name="get_music_json"),
]
