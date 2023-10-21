from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from user_vote.models import UserVoteModel
from taggit.models import Tag


class UserVoteView(LoginRequiredMixin, ListView):
    model = UserVoteModel
    template_name = 'user_vote/user_votes.html'
    context_object_name = 'user_vote'

    def get_queryset(self):
        return self.model.objects.filter(user_vote=self.request.user)

# TODO можно наследоваться?
class UserVoteTagView(LoginRequiredMixin, ListView):
    model = UserVoteModel
    template_name = 'user_vote/user_votes.html'
    context_object_name = 'user_vote'

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['tag'])
        return self.model.objects.filter(tags__in=[tag])


class CreateVoteView(LoginRequiredMixin, CreateView):
    model = UserVoteModel
    fields = ['audio_name', 'user_audio_file', 'tags']
    template_name = 'user_vote/vote_form.html'

    def form_valid(self, form):
        form.instance.user_vote = self.request.user
        return super().form_valid(form)
