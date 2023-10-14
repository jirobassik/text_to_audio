from django.urls import path
from vote.views import AudioView

urlpatterns = [
    path('', AudioView.as_view(), name='vote-view'),
]
