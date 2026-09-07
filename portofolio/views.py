from django.shortcuts import render


def landing_page(request):
    return render(request, "index.html")

def projects_page(request):
    return render(request, "projects.html")

def portfolio_page(request):
    return render(request, "portfolio.html")
