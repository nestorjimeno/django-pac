<<<<<<< HEAD
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
=======
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
>>>>>>> 7d9b0c63ea1d11041b4a145260cce2de97ca5e23
]
