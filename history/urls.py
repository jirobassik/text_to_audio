from django.urls import path
from history.views import HistoryView, HistoryAiSearchView, HistorySearchView, HistoryDetailView, HistoryDeleteView

urlpatterns = [
    path('', HistoryView.as_view(), name='history-view'),
    path('search', HistorySearchView.as_view(), name='history-search'),
    path('search-ai', HistoryAiSearchView.as_view(), name='history-ai-search'),
    path('detail/<int:pk>', HistoryDetailView.as_view(), name='history-detail'),
    path('delete/<int:pk>', HistoryDeleteView.as_view(), name='history-delete'),
]
