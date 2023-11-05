from django.urls import path
from . import views

urlpatterns = [
    path('', views.TextConverterFormView.as_view(), name='text-to-audio'),
]
