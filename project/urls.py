from django.urls import path

from .views import (
    login_view,
    register_view,
    logout_view,
    home_page,
    detail_page,
    add_announcement,
    delete_announcement,
    edit_announcement,
)


urlpatterns = [
    path("", home_page, name="home_page"),
    path("detail/<int:pk>/", detail_page, name="detail_page"),
    path("add-announcement/", add_announcement, name="add_page"),
    path("delete-announcement/<int:pk>/", delete_announcement, name="delete_announcement"),
    path("edit/<int:pk>/", edit_announcement, name="edit_announcement"),
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
]
