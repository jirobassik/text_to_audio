from django.urls import path
from text_converter.views import TextConverterView

urlpatterns = [
    path('', TextConverterView.as_view(), name='text-to-audio'),
]
