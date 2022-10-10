from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                    ReviewsViewSet, TitleViewSet, UserViewSet, get_token,
                    signup)

app_name = 'api'
router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments')
router_v1.register('categories', CategoryViewSet, basename='сategories')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')

AUTHORIZATION_PATHS = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', get_token, name='token'),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include(AUTHORIZATION_PATHS))
]
