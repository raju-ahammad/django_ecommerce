from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    #path('user/login/', views.LoginView.as_view(), redirect_field_name='next', name='Login'),

    #path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    #path('users/', include('django.contrib.auth.urls')),
]
