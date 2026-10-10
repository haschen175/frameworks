"""Главная страница и обработка неизвестного адреса."""

from django.shortcuts import render


def index(request):
    """Показать главную страницу."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    """Показать страницу 404 для адреса без маршрута."""
    return render(request, "404.html", status=404)
