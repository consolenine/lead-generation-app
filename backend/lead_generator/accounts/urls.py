from django.urls import path

from knox import views as knox_views

from accounts.views import CreateUserView, LoginView, ManageUserView, UserView

app_name = 'accounts'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('user/', UserView.as_view(), name='user'),
    path('profile/', ManageUserView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]