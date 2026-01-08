from rest_framework import serializers
from django.contrib.auth.models import  User

class UserSerializer(serializers.ModelSerializer):
    class Meta: # type: ignore
        model = User
        fields = ["first_name","last_name","username","email"]
    
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta: # type: ignore
        model = User
        fields = ["password","first_name","last_name","username","email"]
    def validate_first_name(self,value):
        if len(value) == 0 or value == " ":
            raise serializers.ValidationError("First name cannot be empty.")
        return value
    def validate_last_name(self,value):
        if len(value) == 0 or value == " ":
            raise serializers.ValidationError("First name cannot be empty.")
        return value
    def validate_email(self,value):
        if User.objects.filter(value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)  
        user.save()
        return user

