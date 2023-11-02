from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from taggit.models import Tag
from overrides import override
from user_vote.forms import UserVoteForm, UserVoteInlineFormat
from user_vote.models import UserVoteModel, UserAudioFile
from utils.server_converter.init_json_ser_req import text_converter_serializer, add_voice_serializer, add_voice_request


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


# class CreateVoteView(LoginRequiredMixin, CreateView): # TODO Добавить запрос на доб файлов
#     model = UserVoteModel
#     fields = ['audio_name', 'user_audio_file', 'tags']
#     template_name = 'user_vote/vote_form.html'
#     success_url = reverse_lazy('vote-view-user')
#
#     def form_valid(self, form):
#         form.instance.user_vote = self.request.user
#         audio_name = form.cleaned_data['audio_name']
#         user_audio_file = form.cleaned_data['user_audio_file']
#         data_json = add_voice_serializer.encode(audio_name=audio_name)
#         audio_file = user_audio_file
#         print(audio_file)
#         payload = {
#             'data': (None, data_json, 'application/json'),
#             'file1': (audio_file.name, audio_file.read(), 'audio/wav'),
#         }
#         add_voice_request.get_request_data(payload)
#         return super().form_valid(form)

class CreateVoteView(LoginRequiredMixin, CreateView):
    form_class = UserVoteForm
    template_name = 'user_vote/vote_form.html'
    success_url = reverse_lazy('vote-view-user')

    def __init__(self, **kwargs):
        super().__init__()
        self.object = None

    def get_context_data(self, **kwargs):
        context = super(CreateVoteView, self).get_context_data(**kwargs)
        context['form_file'] = UserVoteInlineFormat()
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form_file = UserVoteInlineFormat(data=self.request.POST, files=self.request.FILES)
        if form.is_valid() and form_file.is_valid():
            return self.form_valid(form, form_file)
        else:
            return self.form_invalid(form, form_file)

    @override(check_signature=False)
    def form_invalid(self, form, form_file):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  product_meta_formset=form_file
                                  )
        )

    @override(check_signature=False)
    def form_valid(self, form, form_file):
        form.instance.user_vote = self.request.user
        self.object = form.save(commit=False)
        self.object.save()
        files = form_file.cleaned_data[0].get('audio_file')
        for file in files:
            UserAudioFile.objects.create(user_voice_name=self.object, audio_file=file)
        return HttpResponseRedirect(self.success_url)
