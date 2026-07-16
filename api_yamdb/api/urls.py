from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('v1/auth/signup/', views.SignupAPIView.as_view(), name='signup'),
    path('v1/auth/token/', views.TokenAPIView.as_view(), name='token'),
]
