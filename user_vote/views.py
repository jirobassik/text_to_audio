from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from user_vote.models import UserVoteModel
from vote.views import TagAudioView


class UserVoteView(LoginRequiredMixin, ListView):
    model = UserVoteModel
    template_name = 'user_vote/user_votes.html'
    context_object_name = 'user_vote'

    def get_queryset(self):
        return self.model.objects.filter(user_vote=self.request.user)


class UserVoteTagView(LoginRequiredMixin, TagAudioView):
    model = UserVoteModel
    template_name = 'user_vote/user_votes.html'
    context_object_name = 'user_vote'


class CreateVoteView(LoginRequiredMixin, CreateView):
    model = UserVoteModel
    fields = ['audio_name', 'user_audio_file', 'tags']
    template_name = 'user_vote/vote_form.html'

    def form_valid(self, form):
        form.instance.user_vote = self.request.user
        return super().form_valid(form)
