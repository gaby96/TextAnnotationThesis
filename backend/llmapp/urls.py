from django.urls import path

from .views import ner_view

urlpatterns = [
    path(route="examples/llmannotate", view=ner_view, name="ner_view"),

]