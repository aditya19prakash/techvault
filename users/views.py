from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import  User
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def users_view(request)-> Response:
    serializer = None
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    return Response({},status=400)

@api_view(['POST'])
def login(request):
    username = request.data["username"] 
    password = request.data["password"] 
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
            "email": user.get_email_field_name(),
        }
    })

@api_view(["POST"])
def logout(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logout successful"}, status=200)

    except Exception as e:
        return Response({"error": "Invalid refresh token"}, status=400)
    
@api_view(["POST"])
def refresh_token(request):
    try:
      access = RefreshToken(request.data["refresh"])
      return Response({"message":"ACCESS TOKEN GENERATED","access":str(access)},status=200)
    except:
        return Response({"message":"invalid token"},status=401)
    

   