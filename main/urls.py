from django.urls import path

from main.views import show_main, show_experiences, projects_page, show_music

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experiences/", show_experiences, name="show_experiences"),
    path('projects/', projects_page, name='projects_page'),
    path('music/', show_music, name='show_music'),
]
