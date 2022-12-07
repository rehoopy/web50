from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("newPage/", views.newPage, name="newPage"),
    path("wiki/<str:title>/edit/", views.edit, name="edit"),
    path("save/", views.save, name="save"),
    path("wiki/", views.randomEntry,name="randomEntry"),
    path("search/wiki/<str:title>", views.entry, name="entries"),
]
