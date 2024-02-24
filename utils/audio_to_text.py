import speech_recognition as sr
from django.core.files.uploadedfile import InMemoryUploadedFile

from text_to_audio_manager.models import TaskAudioManagerModel


def audio_to_text(file_object):
    r = sr.Recognizer()
    with sr.AudioFile(file_object) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        print(text)
        return text


def check_text_type(text, pk):
    if isinstance(text, InMemoryUploadedFile):
        audio_res = audio_to_text(text)
        TaskAudioManagerModel.objects.filter(id=pk).update(text=audio_res)
        return audio_res
    else:
        return text
