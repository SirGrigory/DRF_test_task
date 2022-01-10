from rest_framework import serializers
from .models import Client, Profile

class CreateClientSerializer(serializers.ModelSerializer):

    password = serializers.CharField(min_length=5)
    
    class Meta:
        model = Client
        fields = ('email', 'first_name', 'second_name', 'gender', 'password', 'image')
        # exclude = ('is_staff',)

    def create(self, validated_data):
        return Client.objects.create_client(**validated_data)
    
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('first_name', 'second_name', 'gender', 'image')
        # exclude = ('is_staff',)

    
    
class ClientMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = []
        
    def update(self, instance, validated_data):
        username = self.context.get('request').user
        instance.likes.add(username)
        instance.save()
        return instance
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# class ClientMatchSerializer2(serializers.ModelSerializer):
#     # owner = serializers.SlugRelatedField(slug_field='email', read_only=True)
#     class Meta:
#         model = Profile
#         fields = []
        
#     def update(self, instance, validated_data):
#         print(validated_data)
        
#         # username = validated_data.get('likes')
#         # instance.likes.add(username)
        
#         # print (f'username : {username}')
#         instance.save()
#         return instance
        
        