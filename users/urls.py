app_name = 'users'

from django.urls import path
from .views import ProfileView, RegisterView, AdminUserUpdateView, BanUserView, LogoutView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('<uuid:pk>/', AdminUserUpdateView.as_view(), name='admin'),
    path('<uuid:pk>/ban/', BanUserView.as_view(), name='ban-user'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
