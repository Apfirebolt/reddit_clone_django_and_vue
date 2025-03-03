from django.urls import path
from .views import (
    CreateCustomUserApiView,
    UserProfileApiView,
    SubRedditListCreateApiView,
    SubRedditRetrieveUpdateDestroyApiView,
    PostListCreateApiView,
    PostRetrieveUpdateDestroyApiView,
    RulesListCreateApiView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("register", CreateCustomUserApiView.as_view(), name="signup"),
    path("login", TokenObtainPairView.as_view(), name="signin"),
    path("refresh", TokenRefreshView.as_view(), name="refresh"),
    path("profile", UserProfileApiView.as_view(), name="profile"),
    path("subreddit", SubRedditListCreateApiView.as_view(), name="subreddit"),
    path(
        "subreddit/<int:pk>",
        SubRedditRetrieveUpdateDestroyApiView.as_view(),
        name="subreddit-crud",
    ),
    path("post", PostListCreateApiView.as_view(), name="post"),
    path("post/<int:pk>", PostRetrieveUpdateDestroyApiView.as_view(), name="post-crud"),
    path("rules", RulesListCreateApiView.as_view(), name="rules"),
]
