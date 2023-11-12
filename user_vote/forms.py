from django import forms
from django.forms import inlineformset_factory
from taggit.models import Tag

from .models import UserVoteModel, UserAudioFile

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class FileFieldForm(forms.ModelForm):
    audio_file = MultipleFileField(label='Аудио файлы',
                                   help_text='Файлы формата .wav размера не более 2 мб')

    class Meta:
        model = UserAudioFile
        fields = ['audio_file']


class UserVoteForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(label='Тэги', queryset=Tag.objects.all())

    class Meta:
        model = UserVoteModel
        fields = ['audio_name', 'tags']

    def clean_audio_name(self):
        cd = self.cleaned_data['audio_name']
        if UserVoteModel.objects.filter(audio_name=cd).exists():
            self.add_error('audio_name', forms.ValidationError('Голос с таким названием уже существует'))
        return cd


UserVoteInlineFormat = inlineformset_factory(UserVoteModel, UserAudioFile, form=FileFieldForm, formset=FileFieldForm,
                                             can_delete=False, extra=1, fields=('audio_file',), max_num=5)
