from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CreateClientSerializer, ClientMatchSerializer, ClientSerializer
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response
from .models import Client, Profile
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import mixins
# from .service import ClientFilter



# class ListCreateViewset(viewsets.ViewSet):
class ListCreateViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Client.objects.all().filter(is_staff=False)
    
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['first_name', 'second_name', 'gender']

    # def list(self, request):
    #     queryset = Client.objects.all().filter(is_staff=False)
    #     serializer = ClientSerializer(queryset, many=True)
    #     return Response(serializer.data)

    # def create(self, request):
    #     data = request.data
    #     serializer = CreateClientSerializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
    
    def get_serializer_class(self):
        print(self.request.method)
        if self.request.method == 'GET':
            return ClientSerializer
        elif self.request.method == 'POST':
            return CreateClientSerializer


class ClientMatch(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientMatchSerializer
    queryset = Profile.objects.all()

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        auth_user = get_object_or_404(Profile, owner=request.user)
        liked_profile = get_object_or_404(Profile, pk=kwargs.get('pk'))
        if liked_profile.owner in auth_user.likes.all():
            print(dir(self.serializer_class))
            print(self.serializer_class.validated_data)
            return Response({'email': liked_profile.owner.email})
        return Response('Match send')  # message response

# class ClientListCreate(ListCreateAPIView):

#     serializer_class = CreateClientSerializer
#     permission_classes = [AllowAny]
#     queryset = Client.objects.all()

#     # def post(self,request):
#     #     client = request.data
#     #     serializer = RegisterUserSerializer(data=client)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     return Response(serializer.data,status=HTTP_201_CREATED)
#         # print(dir(request))
#         # print(vars(request).keys())


# class ClientMatch(APIView):

#     def put(self, request, pk):
#         # liked_profile = get_object_or_404(Profile, pk = kwargs.get('pk'))
#         liked_profile = Profile.objects.get(pk=pk)
#         auth_user = get_object_or_404(Profile, owner=request.user)
#         data = request.data
#         data['likes'] = auth_user
#         data['owner'] = liked_profile.owner.pk
#         print(data)
#         serializer = ClientMatchSerializer2(
#             instance=liked_profile, data=data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         print(serializer.validated_data)
#         for value in serializer.validated_data.values():
#             print(value)
#         serializer.save()

#         if liked_profile.owner in auth_user.likes.all():
#                 # print(dir(self.serializer_class))
#                 # print(self.serializer_class.validated_data)
#             return Response({'email': liked_profile.owner.email})
#         return Response('Match send')  # message response
