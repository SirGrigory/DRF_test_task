from django.urls import path
from .views import ClientMatch , ListCreateViewset



urlpatterns = [
    # path('',ClientListCreate.as_view(),name='create_client'),
    path('like/<int:pk>/',ClientMatch.as_view(),name='like_client'),
    path('',ListCreateViewset.as_view({'get': 'list','post': 'create'})),
]
