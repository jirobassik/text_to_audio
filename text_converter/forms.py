from django import forms


class TextConverterForm(forms.Form):
    text = forms.CharField(max_length=1000, min_length=1, required=True)
    voice = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'id': 'voice-select'}))
    preset = forms.ChoiceField(choices=[('ultra_fast', 'Ultra fast'), ('fast', 'Fast'),
                                        ('quality', 'Quality'), ('high_quality', 'High quality')])

    def __init__(self, *args, **kwargs):
        votes = kwargs.pop('votes', [])
        user_votes = kwargs.pop('user_votes', [])
        super(TextConverterForm, self).__init__(*args, **kwargs)
        self.fields['voice'].choices = self.get_choices(votes, user_votes)

    @staticmethod
    def get_choices(votes, user_votes):
        choices = [('Стандартные голоса', [(vote.get('id'), vote.get('audio_name')) for vote in votes]),
                   ('Пользовательские голоса', [(vote.get('id'), vote.get('audio_name')) for vote in user_votes])]
        return choices
