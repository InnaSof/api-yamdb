from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('genres', views.GenreViewSet, basename='genres')
router.register('titles', views.TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/auth/signup/', views.SignupAPIView.as_view(), name='signup'),
    path('v1/auth/token/', views.TokenAPIView.as_view(), name='token'),
    path('v1/', include(router.urls)),
]
