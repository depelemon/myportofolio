from django.urls import path

from main.views import show_main, show_experiences, projects_page, portfolio_page

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experiences/", show_experiences, name="show_experiences"),
    path('projects/', projects_page, name='projects_page'),
    path('portfolio/', portfolio_page, name='portfolio_page'),
]