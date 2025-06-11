from rest_framework import serializers 
from .models import User,Blog 
from django.contrib.auth.hashers import make_password  



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User 
        fields = ['username','password']
    
    def validate_username(self,data):
        if len(data)<2:
            raise serializers.ValidationError("Name must be longer than 2 words.")
        return data 
    
    def create(self,validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data) 


class BlogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Blog
        fields = ['title','content','user']
    
    def create(self,validated_data):
        request = self.context.get('request')
        blog = Blog.objects.create(
            title = validated_data['title'],
            content = validated_data['content'],
            user = request.user
        )
        return blog
        