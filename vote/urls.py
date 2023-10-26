from django.urls import path
from vote.views import AudioView, TagAudioView, DetailAudioView

urlpatterns = [
    path('', AudioView.as_view(), name='vote-view'),
    path('detail/<int:pk>', DetailAudioView.as_view(), name='vote-detail-view'),
    path('tag/<tag>/', TagAudioView.as_view(), name='vote-tag-view'),  # TODO разобраться с slug
]
