from django.urls import re_path
from lists import views as lists

urlpatterns = [
    re_path(r"^$", lists.home_page),
]
