from django.urls import path

from main.views import (
    create_music,
    create_project,
    delete_music,
    delete_project,
    get_music_json,
    get_projects_json,
    project_detail,
    show_experiences,
    show_main,
    show_music,
    show_projects,
    update_project,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experiences/", show_experiences, name="show_experiences"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/<uuid:project_id>/", project_detail, name="project_detail"),
    path("projects/<uuid:project_id>/edit/", update_project, name="update_project"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("music/", show_music, name="show_music"),
    path("music/add/", create_music, name="create_music"),
    path("music/<uuid:music_id>/delete/", delete_music, name="delete_music"),
    path("api/music/", get_music_json, name="get_music_json"),
    path("api/project/", get_projects_json, name="get_projects_json"),
]
