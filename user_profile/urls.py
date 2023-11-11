from django.urls import path, include
from user_profile.views import register, UpdateViewProfile

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('edit/', UpdateViewProfile.as_view(), name='edit'),
    path('register/', register, name='register')
]
