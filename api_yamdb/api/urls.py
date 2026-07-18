from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('genres', views.GenreViewSet, basename='genres')
router.register('titles', views.TitleViewSet, basename='titles')
router.register('users', views.UserViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews',
)
router.register(
    (
        r'titles/(?P<title_id>\d+)/reviews/'
        r'(?P<review_id>\d+)/comments'
    ),
    views.CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/auth/signup/', views.SignupAPIView.as_view(), name='signup'),
    path('v1/auth/token/', views.TokenAPIView.as_view(), name='token'),
    path('v1/', include(router.urls)),
]
