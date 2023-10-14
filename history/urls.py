from django.urls import path
from history.views import history_page, HistoryView

urlpatterns = [
    path('', HistoryView.as_view(), name='history-view'),
]