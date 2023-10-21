from django.urls import path
from user_vote.views import UserVoteTagView, UserVoteView, CreateVoteView

urlpatterns = [
    path('', UserVoteView.as_view(), name='vote-view-user'),
    path('tag/<tag>/', UserVoteTagView.as_view(), name='vote-tag-view-user'),  # TODO разобраться с slug
    path('create/', CreateVoteView.as_view(), name='vote-create-user')
]