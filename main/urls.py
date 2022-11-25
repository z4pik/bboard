from django.urls import path

from .views import index, other_page, BbLoginView, profile, BbLogoutView, ChangeUserInfoView, BbPasswordChangeView

app_name = 'main'

urlpatterns = [
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    # Указан именно данный путь (accounts/profile), потому что по умолчанию django выполняет перенаправление
    # именно на этот адрес, после успешного входа
    path('accounts/profile/', profile, name='profile'),
    # Указан именно данный путь (accounts/login/), потому что по умолчанию django выполняет перенаправление
    # именно на этот адрес, когда пользователь хочет получить доступ к закрытой странице
    path('accounts/login/', BbLoginView.as_view(), name='login'),
    path('accounts/logout/', BbLogoutView.as_view(), name='logout'),
    path('accounts/password/change/', BbPasswordChangeView.as_view(), name='password_change'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index')
]