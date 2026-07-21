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
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments',
)

auth_urlpatterns = [
    path('signup/', views.SignupAPIView.as_view(), name='signup'),
    path('token/', views.TokenAPIView.as_view(), name='token'),
]

v1_urlpatterns = [
    path('auth/', include(auth_urlpatterns)),
    path('', include(router.urls)),
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns)),
]
