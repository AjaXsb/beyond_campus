from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.register, name="signup"),
    path("login/", views.login_user, name="login"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout_user, name="logout"),

    path("applications/", views.show_applications, name="applications"),
    path('create-listing/', views.create_listing, name='create_listing'),
    path('apply/<int:listing_id>/', apply_to_listing, name='apply_to_listing'),

    path('',views.my_favourites, name='my_favourites'),
    path('',views.myhouse_dashboard, name='myhouse_dashboard'),
    path("maintenance/<int:property_id>/", views.request_maintenance, name='request_maintenance'),
    path("insurance/<int:property_id>/", views.insurance_coverage, name='insurance_coverage'),
    path("utility/<int:property_id>/", views.utility_provider, name='utility_provider'),


]

urlpatterns = [
    path('properties/<int:property_id>/report/', report_issue, name='report_issue'),
]

urlpatterns = [
    path('properties/<int:property_id>/reviews/', property_reviews, name='property_reviews'),
]
