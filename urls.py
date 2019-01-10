# coding: utf-8

from django.urls import path
from django.utils.translation import gettext_lazy as _
from postman import views


urlpatterns = [
    path(_('contact/'), views.contact, name='contact'),
    path('process-message/', views.process_message, name='process_message'),
]
