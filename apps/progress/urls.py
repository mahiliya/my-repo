from django.urls import path
from . import views

urlpatterns = [
    path("", views.progress_list, name="progress_list"),
]
