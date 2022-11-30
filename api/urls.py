from django.urls import path
from .views import bbs, BbDetailView, view_comments

urlpatterns = [
    path('bbs/<int:pk>/comments/', view_comments),
    path('bbs/<int:pk>/', BbDetailView.as_view()),
    path('bbs/', bbs),
]
