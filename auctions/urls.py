from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns =[
    path("", views.index, name="index"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("login/", auth_views.LoginView.as_view(template_name="auctions/login.html"), name="login"), 
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create_listing, name="create_listing"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("categories/", views.categories, name="categories"),
    path("categoties/<str:category>/", views.category_listings, name="category_listings"),
    path("listing/<int:listing_id>/watchlist", views.toggle_watchlist, name="toggle_watchlist"),
    path("listing/<int:listing_id>/close", views.close_listing, name="close_listing"),
]