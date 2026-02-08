from django.urls import path
from . import views

app_name = "schools"

urlpatterns = [
    path("", views.school_list, name="list"),
    path("<str:school_code>/", views.school_detail, name="detail"),
    path("api/sigungus/", views.sigungu_api, name="sigungu_api"),
]