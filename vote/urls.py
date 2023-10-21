from django.urls import path
from vote.views import AudioView, TagAudioView

urlpatterns = [
    path('', AudioView.as_view(), name='vote-view'),
    path('tag/<tag>/', TagAudioView.as_view(), name='vote-tag-view'),  # TODO разобраться с slug
]
