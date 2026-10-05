from django.urls import path

from main.views import (
    create_music,
    create_music_ajax,
    create_project,
    create_project_ajax,
    delete_music,
    delete_project,
    get_music_json,
    get_projects_json,
    login_user,
    logout_user,
    music_detail,
    project_detail,
    register,
    show_experiences,
    show_main,
    show_music,
    show_projects,
    toggle_music_star,
    toggle_star,
    update_music,
    update_project,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experiences/", show_experiences, name="show_experiences"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
    path("projects/<uuid:project_id>/", project_detail, name="project_detail"),
    path("projects/<uuid:project_id>/edit/", update_project, name="update_project"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("music/", show_music, name="show_music"),
    path("music/add/", create_music, name="create_music"),
    path("music/add-ajax/", create_music_ajax, name="create_music_ajax"),
    path("music/<uuid:music_id>/", music_detail, name="music_detail"),
    path("music/<uuid:music_id>/edit/", update_music, name="update_music"),
    path("music/<uuid:music_id>/delete/", delete_music, name="delete_music"),
    path(
        "music/<uuid:music_id>/star/",
        toggle_music_star,
        name="toggle_music_star",
    ),
    path("api/music/", get_music_json, name="get_music_json"),
    path("api/project/", get_projects_json, name="get_projects_json"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path(
        "projects/<uuid:project_id>/star/",
        toggle_star,
        name="toggle_star",
    ),
]
