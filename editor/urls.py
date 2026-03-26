from django.urls import path
from django.views.generic import RedirectView

app_name = "editor"
urlpatterns = [
    path("", RedirectView.as_view(url="/admin/"), name="root"),
]
