# coding: utf-8

from django.urls import path
from postman import views


urlpatterns = [
    # path('', views.contact, name='contact'),
    path('process-message/', views.process_message, name='process_message'),
]
