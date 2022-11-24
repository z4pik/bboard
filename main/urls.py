from django.urls import path

from .views import index, other_page, BbLoginView

app_name = 'main'

urlpatterns = [

    # Указан именно данный путь (accounts/login/), потому что по умолчанию django выполняет перенаправление
    # именно на этот адрес, когда пользователь хочет получить доступ к закрытой странице
    path('accounts/login/', BbLoginView.as_view(), name='login'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index')
]