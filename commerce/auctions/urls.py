from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_listing, name="create-listing"),
    path("listing-page", views.listing_page, name="listing-page"),
    path("listing-page/<int:listing_id>", views.listing_page, name="listing-page"),
    path("add-to-watchlist/<int:listing_id>", views.add_to_watchlist, name="add-to-watchlist"),
    path("add-comment", views.add_comment, name="add-comment")
]
