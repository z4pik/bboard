from django.urls import path

from .views import index, other_page, BbLoginView, profile, BbLogoutView, ChangeUserInfoView, \
    BbPasswordChangeView, RegisterUserView, RegisterDoneView, user_activate, DeleteUserView, by_rubric

app_name = 'main'

urlpatterns = [
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    # Указан именно данный путь (accounts/profile), потому что по умолчанию django выполняет перенаправление
    # именно на этот адрес, после успешного входа
    path('accounts/profile/', profile, name='profile'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register', RegisterUserView.as_view(), name='register'),
    # Указан именно данный путь (accounts/login/), потому что по умолчанию django выполняет перенаправление
    # именно на этот адрес, когда пользователь хочет получить доступ к закрытой странице
    path('accounts/login/', BbLoginView.as_view(), name='login'),
    path('accounts/logout/', BbLogoutView.as_view(), name='logout'),
    path('accounts/password/change/', BbPasswordChangeView.as_view(), name='password_change'),
    path('<int:pk>/', by_rubric, name='by_rubric'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index')
]