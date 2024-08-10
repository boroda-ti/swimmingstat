from django.urls import path

from .views import LoginAPIView, UserDetailUpdateAPIView

urlpatterns = [
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('users/<int:pk>/', UserDetailUpdateAPIView.as_view(), name='user-detail-update'),
]
