from django.urls import path

from .views import AthleteCRUDAPIView

urlpatterns = [
    path('athletes/', AthleteCRUDAPIView.as_view(), name='athlete-list'),
    path('athletes/<int:pk>/', AthleteCRUDAPIView.as_view(), name='athlete-detail'),
]
