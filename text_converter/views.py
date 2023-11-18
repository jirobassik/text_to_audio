import logging

from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView
from requests.exceptions import SSLError, ConnectionError

from text_converter.forms import TextConverterLoginForm, TextConverterForm
from utils.server_converter.send import send_converter
from utils.server_converter.server_error import SendError
from vote.models import VoteModel
from user_vote.models import UserVoteModel
from text_converter.tasks import add_response_api_converter


class TextConverterView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return TextConverterLoginFormView.as_view()(request, *args, **kwargs)
        else:
            return TextConverterFormView.as_view()(request, *args, **kwargs)


class TextConverterLoginFormView(FormView):
    form_class = TextConverterLoginForm
    template_name = 'text_converter/text_to_audio.html'
    success_url = reverse_lazy('text-to-audio')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        queryset_rel_file_vote_model = VoteModel.objects.annotate(num_related=Count('audiofilemodel')).filter(
            num_related__gt=0)
        queryset_rel_file_user_vote_model = UserVoteModel.objects.access_user(self.request.user).annotate(
            num_related=Count('useraudiofile')).filter(num_related__gt=0)
        kwargs['votes'] = queryset_rel_file_vote_model.values('id', 'audio_name')
        kwargs['user_votes'] = queryset_rel_file_user_vote_model.values('id', 'audio_name')
        return kwargs

    @staticmethod
    def _get_optgroup_name(form):
        voice_choices = form.fields['voice'].choices
        selected_voice = int(form.cleaned_data.get('voice'))
        name_optgroup = {'Стандартные голоса': 'standart_v', 'Пользовательские голоса': 'user_v'}
        for optgroup, choices in voice_choices:
            for choice_id, choice_name in choices:
                if choice_id == selected_voice:
                    return name_optgroup.get(optgroup)
        return None

    def form_valid(self, form):
        optgroup_name = self._get_optgroup_name(form)
        text = form.cleaned_data.get('text')
        voice_id = form.cleaned_data.get('voice')
        preset = form.cleaned_data.get('preset')
        add_response_api_converter(text, voice_id, preset, optgroup_name, self.request.user)
        messages.success(self.request, 'Результат работы можно будет увидеть в истории')
        return HttpResponseRedirect(self.get_success_url())


class TextConverterFormView(FormView):
    form_class = TextConverterForm
    template_name = 'text_converter/text_to_audio.html'
    success_url = reverse_lazy('text-to-audio')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        queryset_rel_file_vote_model = VoteModel.objects.annotate(num_related=Count('audiofilemodel')).filter(
            num_related__gt=0)
        kwargs['votes'] = queryset_rel_file_vote_model.values('id', 'audio_name')
        return kwargs

    def form_valid(self, form):
        optgroup_name = 'standart_v'
        text = form.cleaned_data.get('text')
        voice_id = form.cleaned_data.get('voice')
        preset = form.cleaned_data.get('preset')
        voice_object = VoteModel.objects.get(id=voice_id)
        try:
            response_converter = send_converter(text, voice_object, preset, optgroup_name)
            return response_converter
        except (SSLError, ConnectionError, SendError) as e:
            messages.error(self.request, 'Что-то пошло не так, попробуйте позже')
            logging.error(e)
        return HttpResponseRedirect(self.get_success_url())
