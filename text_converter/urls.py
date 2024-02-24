from django.urls import path
from text_converter.views import TextConverterView, TextConverterLoginAudioView

urlpatterns = [
    path('', TextConverterView.as_view(), name='text-to-audio'),
    path('audio-input/', TextConverterLoginAudioView.as_view(), name='audio-input')
]
