from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import (
    ListCustomUserSerializer,
    CustomUserSerializer,
    CustomTokenObtainPairSerializer,

)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from accounts.models import CustomUser
from rest_framework.response import Response
from . pagination import CustomPagination


class CreateCustomUserApiView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = []


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = []


class ListCustomUsersApiView(ListAPIView):
    serializer_class = ListCustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['username', 'email']
    ordering_fields = ['username', 'email']
    search_fields = ['username', 'email']