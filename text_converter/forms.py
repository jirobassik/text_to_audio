from django import forms
from operator import getitem
from utils.file_validation import extension_validation, content_validation, max_size_validation


class TextConverterForm(forms.Form):
    text = forms.CharField(max_length=400, min_length=1, required=True, widget=forms.Textarea, initial='Hello world',
                           label='Текст')
    voice = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'id': 'voice-select'}),
                              label='Голос', )
    preset = forms.ChoiceField(choices=[('ultra_fast', 'Очень быстро'), ('fast', 'Быстро'),
                                        ('quality', 'Качество'), ('high_quality', 'Высокое качество')],
                               label='Скорость/Качество')

    def __init__(self, *args, **kwargs):
        self.votes = kwargs.pop('votes', [])
        self.user_votes = kwargs.pop('user_votes', [])
        super(TextConverterForm, self).__init__(*args, **kwargs)
        self.fields['voice'].choices = self.get_choices()

    def get_choices(self):
        choices = [('Стандартные голоса', [(vote.get('id'), vote.get('audio_name')) for vote in self.votes]), ]
        return choices


class TextConverterLoginForm(TextConverterForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_choices(self):
        voice_choice = (('Стандартные голоса', [(vote.get('id'), vote.get('audio_name')) for vote in self.votes]),
                        ('Пользовательские голоса', [(vote.get('id'), vote.get('audio_name'))
                                                     for vote in self.user_votes]))
        choices = [choice for choice in voice_choice if getitem(choice, 1)]
        return choices


class TextConverterFormAudioUpload(TextConverterLoginForm):
    text = forms.FileField(label='Загрузка аудио файла',
                           help_text='Файл формата .wav, размера не более 2 мб',
                           validators=(extension_validation, content_validation,
                                       max_size_validation))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
