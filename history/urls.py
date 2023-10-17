from django.urls import path
from history.views import HistoryView, HistorySearchView

urlpatterns = [
    path('', HistoryView.as_view(), name='history-view'),
    path('search', HistorySearchView.as_view(), name='history-search'),
]
