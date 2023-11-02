from django.urls import path
from user_vote.views import UserVoteTagView, UserVoteView, CreateVoteView, UserVoteDetailView, UserVoteDeleteView

urlpatterns = [
    path('', UserVoteView.as_view(), name='vote-view-user'),
    path('create/', CreateVoteView.as_view(), name='vote-create-user'),
    path('detail/<int:pk>', UserVoteDetailView.as_view(), name='vote-detail-user'),
    path('delete/<int:pk>', UserVoteDeleteView.as_view(), name='vote-delete-user'),
    path('tag/<tag>/', UserVoteTagView.as_view(), name='vote-tag-view-user'),  # TODO разобраться с slug
]
