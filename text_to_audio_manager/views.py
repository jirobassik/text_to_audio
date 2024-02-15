from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from text_to_audio_manager.models import TaskAudioManagerModel


class AudioManagerView(LoginRequiredMixin, ListView):
    model = TaskAudioManagerModel
    context_object_name = 'audio_manager'
    template_name = 'text_to_audio_manager/text_to_audio_manager.html'

    def get_queryset(self):
        if self.request.htmx:
            self.template_name = 'text_to_audio_manager/status_table.html'
        return self.model.objects.filter(rel_user=self.request.user, is_deleted=False)
