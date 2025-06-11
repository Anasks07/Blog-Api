from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication
from .models import User,Blog
from .serializer import UserSerializer, BlogSerializer
from django.contrib.auth import authenticate 
from rest_framework.authtoken.models import Token

# Create your views here.


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        data = request.data 
        serializer = UserSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)


class UserloginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({"Message:","Username and Password are required."})
        
        user = authenticate(username = username, password = password)    
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)
            return Response({"message": "Login successful","user": serializer.data,"token":token.key},status=status.HTTP_200_OK)
        
        return Response({"error":"Invalid credentials"})
             
    


class DisplayUser(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        queryset = User.objects.all()
        serializer = UserSerializer(instance = queryset,many=True)
        return Response(serializer.data)

class CreateBlogView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        data = request.data 
        serializer = BlogSerializer(data = data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ListBlogView(APIView):
    permission_classes = [AllowAny]
    
    def get(self,request,id=None):
        
        if id:
            blog = Blog.objects.filter(id=id).first()
            
            if blog is None:
                return Response({"error":"blog not found."},status=status.HTTP_404_NOT_FOUND)
            
            serializer = BlogSerializer(instance=blog) 
            return Response(serializer.data)
        
        else:  
            queryset = Blog.objects.all()
            serializer = BlogSerializer(instance=queryset,many=True)
            return Response(serializer.data)


class DeleteBlogView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,id):
        
        try:
            blog = Blog.objects.get(id=id)
            
            if request.user == blog.user:
                blog.delete()
                return Response({"Message":"Blog delete."},status=status.HTTP_200_OK)
            else:
                return Response({"Message":"Blog cannot be deleted as you are not the author of this blog."},status=status.HTTP_403_FORBIDDEN)
        
        except Blog.DoesNotExist:
            return Response({"Message":"Blog not found."},status=status.HTTP_404_NOT_FOUND)


class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,id):
        try:
            user = User.objects.get(id=id)
            
            if request.user == user:
                user.delete()
                return Response({"Message":"User deleted successfully."},status=status.HTTP_200_OK)
            else:
                return Response({"Message":"You have no permission."},status=status.HTTP_403_FORBIDDEN)
            
        except User.DoesNotExist:
            return Response({"Message":"User doesnot exist."},status=status.HTTP_404_NOT_FOUND)

