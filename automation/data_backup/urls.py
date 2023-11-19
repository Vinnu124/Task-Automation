from django.urls import path
from .views import backup_view,home_view,backup_drive

urlpatterns = [
    path("home/", home_view, name="home"),
    path("backup/", backup_view, name="backup"),
    path("backup_drive/", backup_drive, name="backup_drive"),
]