from django.urls import path

from .views import Roles

urlpatterns = [
    path('roles', view=Roles.as_view())
    ]
