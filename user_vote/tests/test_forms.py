from user_vote.forms import UserVoteForm
from django.test import TestCase


class CreateUserVoice(TestCase):

    def test_audio_name_label(self):
        form = UserVoteForm()
        self.assertTrue(
            form.fields['audio_name'].label is None or
            form.fields['audio_name'].label == 'Название голоса')

    def test_tags_label(self):
        form = UserVoteForm()
        self.assertTrue(
            form.fields['tags'].label is None or form.fields['tags'].label == 'Тэги')

    def test_not_valid_exist_voice(self):
        form_data = {'audio_name': 'Даниэль'}
        form = UserVoteForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_not_valid_tags(self):
        form_data = {'audio_name': 'Даниэль2', 'tags': ['Неизвестный', ]}
        form = UserVoteForm(data=form_data)
        self.assertFalse(form.is_valid())
