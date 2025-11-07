from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.role_selection, name='role-selection'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),
]