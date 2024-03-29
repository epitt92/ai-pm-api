from django.urls import path
from .views import SignupView, SigninView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='singup'),
    path('signin/', SigninView.as_view(), name='singin'),
]
