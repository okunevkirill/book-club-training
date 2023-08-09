from django.urls import re_path
from lists import views as lists

urlpatterns = [
    re_path(r"^$", lists.home_page, name="home"),
    re_path(r"^lists/new$", lists.new_list, name="new_list"),
    re_path(r"^lists/the-only-list-in-the-world/$", lists.view_list, name="view_list"),
]
