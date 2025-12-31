from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserSerializer,UserRegisterSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth.models import  User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache


class UserPagination(PageNumberPagination):
    max_page_size = 50
    page_size = 50
    page_size_query_param = 'size'

class UserView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        cache_key = f"UserView:{request.get_full_path()}"
        cache_response = cache.get(cache_key)
        if cache_response:
            return Response(cache_response,status=200)
        users = User.objects.all()
        userpagination = UserPagination()
        paginated_data = userpagination.paginate_queryset(users,request=request)
        serializer = UserSerializer(paginated_data,many=True)
        response = userpagination.get_paginated_response(serializer.data).data
        cache.set(cache_key,response,timeout=60*60)
        return Response(response,status=200)
    
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    
class UserLogin(APIView):
    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username = username,password = password)
        if user is None:
            return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)    
        return Response({
        "message": "Login successful",
        "access": access,
        "refresh": str(refresh),
        "user": {
            "id": user.pk,
            "username": user.get_username(),
            "email": user.email, # type: ignore
        }
    })
class UserRegister(APIView):
    serializer_class = UserRegisterSerializer
    def post(self,request):
        # username = request.data.get("username")
        # email = request.data.get("email")
        # first_name = request.data.get("first_name")
        # last_name = request.data.get("last_name")
        # password = request.data.get("password")
        serializer = UserRegister.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)



class UserLogout(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist() # type: ignore
            return Response({"message": "Logout successful"}, status=200)
        except Exception as e:
           return Response({"error": "Invalid refresh token"}, status=400)
    

class RefreshTokenView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            access = RefreshToken(token=request.data["refresh"])
            return Response({"message":"ACCESS TOKEN GENERATED","access":str(access)},status=200)
        except:
            return Response({"message":"invalid token"},status=401)



   