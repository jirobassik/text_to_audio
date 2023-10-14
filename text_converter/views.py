from django.shortcuts import render
from vote.models import VoteModel

def text_to_audio(request):
    votes = VoteModel.objects.all()
    return render(request, 'text_converter/text_to_audio.html', {"votes": votes})
