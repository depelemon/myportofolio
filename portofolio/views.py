import json

from django.conf import settings
from django.shortcuts import render


def landing_page(request):
    experiences_path = settings.BASE_DIR / "portofolio" / "data" / "experiences.json"
    with open(experiences_path, encoding="utf-8") as f:
        experiences = json.load(f)
    return render(request, "index.html", {"experiences": experiences})

def projects_page(request):
    return render(request, "projects.html")

def portfolio_page(request):
    return render(request, "portfolio.html")
