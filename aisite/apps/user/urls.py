from django.urls import path
from .views import SignupView, SigninView, logout

urlpatterns = [
    path('register/', SignupView.as_view(), name='register'),
    path('login/', SigninView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
]
