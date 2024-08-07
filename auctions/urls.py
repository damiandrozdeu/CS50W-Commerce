from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create_listing/", views.create_listing, name="create_listing"),
    path("categories/", views.categories, name="categories"),
    path("categories/<int:category_id>", views.categories_details, name="categories_details"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("auction/<int:auction_id>/", views.auction, name="auction"),
    path("auction/<int:auction_id>/add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("auction/<int:auction_id>/remove_watchlist", views.remove_watchlist, name="remove_watchlist"),
    path("auction/<int:auction_id>/add_bid", views.add_bid, name="add_bid"),
    path("auction/<int:auction_id>/add_comment", views.add_comment, name="add_comment"),
    path("auction/<int:auction_id>/close_auction", views.close_auction, name="close_auction"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
