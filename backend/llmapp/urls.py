from django.urls import path

from .views import ner_view, docClassification_view

urlpatterns = [
    path(route="examples/llmannotate", view=ner_view, name="ner_view"),
    path(route="examples/docClassllmannotate", view=docClassification_view, name="docClassification_view")

]