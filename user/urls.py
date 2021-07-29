from django.urls import path

from .views import RegisterView, LoginView, LogoutView, ProfileView

app_name = 'user'
urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('reset/', RegisterView.as_view(), name='reset'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]