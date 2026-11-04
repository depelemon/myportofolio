from django.urls import path

from main import api_views

app_name = "api"

urlpatterns = [
    path("projects/", api_views.project_list, name="project-list"),
    path("projects/<uuid:project_id>/", api_views.project_detail, name="project-detail"),
    path("projects/<uuid:project_id>/star/", api_views.project_star, name="project-star"),
    path("music/", api_views.music_list, name="music-list"),
    path("music/<uuid:music_id>/", api_views.music_detail, name="music-detail"),
    path("music/<uuid:music_id>/star/", api_views.music_star, name="music-star"),
]
