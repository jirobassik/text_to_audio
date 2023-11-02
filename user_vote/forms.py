from django import forms
from django.forms import inlineformset_factory
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
    class Meta:
        model = UserAudioFile
        fields = ['audio_file']

    audio_file = MultipleFileField()


class UserVoteForm(forms.ModelForm):
    class Meta:
        model = UserVoteModel
        fields = ['audio_name', 'tags']


UserVoteInlineFormat = inlineformset_factory(UserVoteModel, UserAudioFile, form=FileFieldForm,
                                             can_delete=False, extra=1, fields=('audio_file',), max_num=5)
