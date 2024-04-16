from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.register, name="signup"),
    path("login/", views.login_user, name="login"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout_user, name="logout"),
]

urlpatterns = [
    path('properties/<int:property_id>/add_favourite/', add_to_favourites, name='add_to_favourites'),
    path('properties/<int:property_id>/favourites/', show_favourites, name='show_favourites'),
    path('properties/<int:property_id>/myfavourites/', my_favourites, name='my_favourites'),
    # Make sure you have views and URLs set for 'property_details' and 'listing'
]
urlpatterns = [
    path('properties/<int:property_id>/report/', report_issue, name='report_issue'),
]

urlpatterns = [
    path('properties/<int:property_id>/reviews/', property_reviews, name='property_reviews'),
]
