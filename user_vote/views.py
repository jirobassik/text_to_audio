import logging
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from requests.exceptions import SSLError, ConnectionError
from taggit.models import Tag
from overrides import override
from user_vote.forms import UserVoteForm, UserVoteInlineFormat
from user_vote.models import UserVoteModel, UserAudioFile
from utils.server_converter.send import send_voice, del_voice
from utils.server_converter.init_json_ser_req import add_delete_voice_request_user
from utils.server_converter.server_error import SendError


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
        queryset = self.model.objects.filter(user_vote=self.request.user).prefetch_related(
            'useraudiofile_set')
        return super().get_object(queryset)


class UserVoteTagView(LoginRequiredMixin, ListView):
    model = UserVoteModel
    template_name = 'user_vote/user_votes.html'
    context_object_name = 'user_vote'

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['tag'])
        return self.model.objects.access_user(self.request.user).filter(tags__in=[tag])


class CreateVoteView(LoginRequiredMixin, CreateView):
    form_class = UserVoteForm
    template_name = 'user_vote/vote_form.html'
    success_url = reverse_lazy('vote-view-user')

    def __init__(self, **kwargs):
        super().__init__()
        self.object = None

    def get_context_data(self, **kwargs):
        context = super(CreateVoteView, self).get_context_data(**kwargs)
        context['form_file'] = UserVoteInlineFormat
        return context

    def custom_context(self, **kwargs):
        context = super(CreateVoteView, self).get_context_data(**kwargs)
        context['form_file'] = kwargs.get('form_file')
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form_file = UserVoteInlineFormat(data=self.request.POST, files=self.request.FILES)
        if form.is_valid() and form_file.is_valid():
            return self.form_valid(form, form_file)
        else:
            return self.form_invalid(form, form_file)

    @override(check_signature=False)
    def form_invalid(self, form, form_file):
        return self.render_to_response(
            self.custom_context(form=form,
                                form_file=form_file
                                )
        )

    @override(check_signature=False)
    def form_valid(self, form, form_file):
        audio_name = form.cleaned_data.get('audio_name')
        files = form_file.cleaned_data.get('audio_file')
        try:
            send_voice(files, audio_name, add_delete_voice_request_user)
            form.instance.user_vote = self.request.user
            self.object = form.save()  # TODO Разобраться с save
            for file in files:
                UserAudioFile.objects.create(user_voice_name=self.object, audio_file=file)
        except (SSLError, ConnectionError, SendError) as e:
            messages.error(self.request, 'Что-то пошло не так, попробуйте позже')
            logging.error(e)
        return HttpResponseRedirect(self.success_url)


class UserVoteDeleteView(LoginRequiredMixin, DeleteView):
    model = UserVoteModel
    success_url = reverse_lazy("vote-view-user")
    template_name = 'user_vote/user_vote_confirm_delete.html'

    def get_object(self, queryset=None):
        queryset = self.model.objects.access_user(self.request.user)
        return super().get_object(queryset)

    def form_valid(self, form):
        audio_name = self.object.audio_name
        try:
            del_voice(audio_name, add_delete_voice_request_user)
            return super().form_valid(form)
        except (SSLError, ConnectionError, SendError) as e:
            messages.error(self.request, 'Что-то пошло не так, попробуйте позже')
            logging.error(e)
            return HttpResponseRedirect(self.success_url)
