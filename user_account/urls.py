from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.user_register, name='user_register'),
    path('settings/', views.account_settings, name='account_settings'),
    path('subscription/', views.update_subscription, name='subscription'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('make_request/', views.make_request, name='make_request'),
    path("update", views.update_user, name="update_user")
]
