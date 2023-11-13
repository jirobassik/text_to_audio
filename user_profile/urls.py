from django.urls import path, include
from user_profile.views import UpdateViewProfile, RegisterView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('edit/', UpdateViewProfile.as_view(), name='edit'),
    path('register/', RegisterView.as_view(), name='register')
]
