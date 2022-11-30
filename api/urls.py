from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import bbs, BbDetailView, view_comments
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('bbs/<int:pk>/comments/', view_comments),
    path('bbs/<int:pk>/', BbDetailView.as_view()),
    path('bbs/', bbs),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += doc_urls
