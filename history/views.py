from django.shortcuts import render
from django.views.generic import ListView
from .models import HistoryModel

def history_page(request):
    history_entries = HistoryModel.objects.all()
    return render(request, 'history/history.html', {'history_entries': history_entries})

class HistoryView(ListView):
    model = HistoryModel
    context_object_name = 'history_entries'
    template_name = 'history/history.html'
