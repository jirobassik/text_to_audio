from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from taggit.models import Tag

from user_vote.models import UserVoteModel


class UserVoteView(LoginRequiredMixin, ListView):
    model = UserVoteModel
    template_name = 'user_vote/user_votes.html'
    context_object_name = 'user_vote'

    def get_queryset(self):
        return self.model.objects.access_user(self.request.user)

class UserVoteDetailView(LoginRequiredMixin, DetailView):
    model = UserVoteModel
    template_name = 'user_vote/user_vote_detail.html'
    context_object_name = 'user_vote_detail'

    def get_object(self, queryset=None):
        queryset = self.model.objects.access_user(self.request.user)
        return super().get_object(queryset)

class UserVoteTagView(LoginRequiredMixin, ListView):
    model = UserVoteModel
    template_name = 'user_vote/user_votes.html'
    context_object_name = 'user_vote'

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['tag'])
        return self.model.objects.access_user(self.request.user).filter(tags__in=[tag])

class CreateVoteView(LoginRequiredMixin, CreateView):
    model = UserVoteModel
    fields = ['audio_name', 'user_audio_file', 'tags']
    template_name = 'user_vote/vote_form.html'

    def form_valid(self, form):
        form.instance.user_vote = self.request.user
        return super().form_valid(form)
