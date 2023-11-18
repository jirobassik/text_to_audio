from django import forms
from operator import getitem


class TextConverterLoginForm(forms.Form):
    text = forms.CharField(max_length=400, min_length=1, required=True, widget=forms.Textarea, initial='Привет мир',
                           label='Текст')
    voice = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'id': 'voice-select'}), label='Голос')
    preset = forms.ChoiceField(choices=[('ultra_fast', 'Очень быстро'), ('fast', 'Быстро'),
                                        ('quality', 'Качество'), ('high_quality', 'Высокое качество')],
                               label='Скорость/Качество')

    def __init__(self, *args, **kwargs):
        votes = kwargs.pop('votes', [])
        user_votes = kwargs.pop('user_votes', [])
        super(TextConverterLoginForm, self).__init__(*args, **kwargs)
        self.fields['voice'].choices = self.get_choices(votes, user_votes)

    @staticmethod
    def get_choices(votes, user_votes):
        voice_choice = (('Стандартные голоса', [(vote.get('id'), vote.get('audio_name')) for vote in votes]),
                        ('Пользовательские голоса', [(vote.get('id'), vote.get('audio_name')) for vote in user_votes]))
        choices = [choice for choice in voice_choice if getitem(choice, 1)]
        return choices


class TextConverterForm(forms.Form):
    text = forms.CharField(max_length=400, min_length=1, required=True, widget=forms.Textarea, initial='Привет мир',
                           label='Текст')
    voice = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'id': 'voice-select'}),
                              label='Голос', )
    preset = forms.ChoiceField(choices=[('ultra_fast', 'Очень быстро'), ('fast', 'Быстро'),
                                        ('quality', 'Качество'), ('high_quality', 'Высокое качество')],
                               label='Скорость/Качество')

    def __init__(self, *args, **kwargs):
        votes = kwargs.pop('votes', [])
        super(TextConverterForm, self).__init__(*args, **kwargs)
        self.fields['voice'].choices = self.get_choices(votes)

    @staticmethod
    def get_choices(votes):
        choices = [('Стандартные голоса', [(vote.get('id'), vote.get('audio_name')) for vote in votes]), ]
        return choices
