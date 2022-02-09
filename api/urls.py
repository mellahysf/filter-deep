from django.urls import path

from . import views

urlpatterns = [
    path('filter/', views.Filter.as_view()),
    path('clear/', views.clear),
]
