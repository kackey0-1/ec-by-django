from django.urls import path

from .views import SignupView, LoginView, LogoutView, PasswordResetView, activate, PasswordEditView

app_name = 'user'
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('activate/<emailb64>/<token>/', activate, name='activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset/', PasswordResetView.as_view(), name='reset'),
    path('edit/password/<emailb64>/<token>/', PasswordEditView.as_view(), name='edit_password_get'),
    path('edit/password/', PasswordEditView.as_view(), name='edit_password'),
]