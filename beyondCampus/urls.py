from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.register, name="signup"),
    path("login/", views.login_user, name="login"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout_user, name="logout"),

    path("application",views.apply_to_listing,name="application"),
    path("reviews",views.property_reviews,name="review"),
    path("add_favourite",views.add_to_favourites,name="add_favourite"),
    path("report",views.report_issue,name="report"),
    
    path("landlord_applications/", views.show_landlord_applications, name="show_landlord_applications"),
    path("student_applications/", views.show_student_applications, name="show_student_applications"),
    path('delete_application/<int:application_id>/', views.delete_application, name='delete_application'),
    path('accept_application/<int:application_id>/', views.accept_application, name='accept_application'),
    path('reject_application/<int:application_id>/', views.reject_application, name='reject_application'),
    path('apply/<int:listing_id>/', views.apply_to_listing, name='apply_to_listing'),

    path('my_favourites',views.my_favourites, name='my_favourites'),
    path('myhouse_dashboard',views.myhouse_dashboard, name='myhouse_dashboard'),
    path("maintenance/<int:property_id>/", views.request_maintenance, name='request_maintenance'),
    path("insurance/<int:property_id>/", views.insurance_coverage, name='insurance_coverage'),
    path("utility/<int:property_id>/", views.utility_provide, name='utility_provider'),
    path('faqs/', views.faq_view, name='faqs'),


]
