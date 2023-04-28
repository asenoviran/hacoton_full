from django.urls import path
from .views import RegistrationView, ActivationView, LoginView, LogoutView

urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('activation/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]