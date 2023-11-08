from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from text_converter.forms import TextConverterForm
from vote.models import VoteModel
from user_vote.models import UserVoteModel
from utils.server_converter.init_json_ser_req import text_converter_serializer, text_converter_request
from text_converter.tasks import add_response_api_converter

class TextConverterFormView(FormView):
    form_class = TextConverterForm
    template_name = 'text_converter/text_to_audio.html'
    success_url = reverse_lazy('text-to-audio')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['votes'] = VoteModel.objects.values('id', 'audio_name')
        kwargs['user_votes'] = UserVoteModel.objects.values('id', 'audio_name')
        return kwargs

    @staticmethod
    def get_optgroup_name(form):
        voice_choices = form.fields['voice'].choices
        selected_voice = int(form.cleaned_data.get('voice'))
        name_optgroup = {'Стандартные голоса': 'standart_v', 'Пользовательские голоса': 'user_v'}
        for optgroup, choices in voice_choices:
            for choice_id, choice_name in choices:
                if choice_id == selected_voice:
                    return name_optgroup.get(optgroup)
        return None

    def form_valid(self, form):
        optgroup_name = self.get_optgroup_name(form)
        text = form.cleaned_data.get('text')
        voice_id = form.cleaned_data.get('voice')
        preset = form.cleaned_data.get('preset')
        add_response_api_converter(text, voice_id, preset, optgroup_name)
        messages.success(self.request, 'Результат работы можно будет увидеть в истории')
        return HttpResponseRedirect(self.get_success_url())

def text_to_audio(request, voice=None):
    votes = VoteModel.objects.values('id', 'audio_name')
    print(votes)
    print('----------------')
    user_votes = UserVoteModel.objects.values('id', 'audio_name')
    print(user_votes)
    print('-----------------')
    all_votes = votes.union(user_votes, all=True)
    print(all_votes)

    if 'converter' in request.POST:

        pass
        # text = request.POST.get('text', '')
        # voice = request.POST.get('voice', 'emma')
        # preset = request.POST.get('preset', 'ultra_fast')
        # data_json = text_converter_serializer.encode(text=text, voice=voice, preset=preset)
        # audio_file = VoteModel.objects.get(id=voice).audio_file
        # payload = {
        #     'data': (None, data_json, 'application/json'),
        #     'file1': (audio_file.name, audio_file.read(), 'audio/mp3'),
        #     'file2': (audio_file.name, audio_file.read(), 'audio/mp3')
        # }

        # text_converter_request.get_request_data(payload)
        # add_response_api_converter(text, voice, request.user)

    # text = 'Hello my name Emma'
    # preset = 'fast'
    # audio_file = VoteModel.objects.get(id=3).audio_file
    # res = text_converter_serializer.encode(text=text, voice='emma', preset=preset)
    # print(res)

    # context = {"votes": votes, "voice": voice}
    context = {
        'votes': votes,
        'user_votes': user_votes,
    }
    # print(context)
    return render(request, 'text_converter/text_to_audio.html', context)
