from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
)
from .serializers import (
    ListCustomUserSerializer,
    CustomUserSerializer,
    CustomTokenObtainPairSerializer,
    SubRedditSerializer,
    PostSerializer,
    CommentSerializer,
    PostVoteSerializer,
    RulesSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from accounts.models import CustomUser
from subreddit.models import SubReddit, Post, Comment, Rules
from rest_framework.response import Response
from .pagination import CustomPagination


class CreateCustomUserApiView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        email = request.data.get("email")

        if CustomUser.objects.filter(username=username).exists():
            return Response({"message": "Username already exists"}, status=400)

        if CustomUser.objects.filter(email=email).exists():
            return Response({"message": "Email already exists"}, status=400)

        return super().post(request, *args, **kwargs)


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = []


class ListCustomUsersApiView(ListAPIView):
    serializer_class = ListCustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["username", "email"]
    ordering_fields = ["username", "email"]
    search_fields = ["username", "email"]


class UserProfileApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class SubRedditListCreateApiView(ListCreateAPIView):
    serializer_class = SubRedditSerializer
    queryset = SubReddit.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["name", "description"]
    ordering_fields = ["name", "description"]
    search_fields = ["name", "description"]
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class SubRedditRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubRedditSerializer
    queryset = SubReddit.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(creator=self.request.user)


class PostListCreateApiView(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["title", "content"]
    ordering_fields = ["title", "content"]
    search_fields = ["title", "content"]
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class PostRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(creator=self.request.user)


class RulesListCreateApiView(ListCreateAPIView):
    serializer_class = RulesSerializer
    queryset = Rules.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["rule"]
    ordering_fields = ["rule"]
    search_fields = ["rule"]
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class RetrieveRulesApiView(RetrieveAPIView):
    serializer_class = RulesSerializer
    queryset = Rules.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
