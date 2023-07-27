from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Tweets.as_view()),
]