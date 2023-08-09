from django.urls import re_path, include
from lists import views as lists_views
from lists import urls as list_urls

urlpatterns = [
    re_path(r"^$", lists_views.home_page, name="home"),
    re_path(r"^lists/", include(list_urls)),
]
