from django.urls import path
from text_to_audio_manager.views import AudioManagerView

urlpatterns = [
    path('', AudioManagerView.as_view(), name='audio-manager-view'),
]
