from django.urls import path
from django.conf.urls.static import static
from reddit_clone import settings
from . views import LoginView, RegisterUser
import django.contrib.auth.views as AuthViews


urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', AuthViews.LogoutView.as_view(), name='logout'),
    path('register', RegisterUser.as_view(), name='register'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)