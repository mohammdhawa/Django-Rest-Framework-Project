from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegistrationAPIView, LogoutAPIView


urlpatterns = [
    # path('login/', obtain_auth_token, name='login'),
    path('register', RegistrationAPIView.as_view(), name='register'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
]
