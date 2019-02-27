from django.contrib import admin
from Module_Account import views
from django.urls import path

urlpatterns = [
    path('', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
]
