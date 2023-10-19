from django.urls import path, include
from user_profile.views import register

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', register, name='register')
]
