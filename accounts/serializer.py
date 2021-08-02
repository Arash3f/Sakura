from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed , NotAcceptable
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

class User_Register_Serialiaer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        username = validated_data['username']
        password = validated_data['password']
        email    = validated_data['email']

        try : 
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                is_active=False,
                is_staff=True,
            )
        except:
            raise NotAcceptable("Cant create User "  , code= 406)

        return user

    class Meta:
        model = User
        fields = ("username", "password", "email")
    
class Request_Password_Reset_Email_Serializer(serializers.Serializer):
    email = serializers.EmailField(min_length = 2)
    class Meta:
        fields = ['email']

class Check_Confirm_Email_serializer(serializers.Serializer):
    token = serializers.CharField(min_length = 1, write_only =True)
    class Meta:
        fields = ['token']

class Set_New_Password_Serializer(serializers.Serializer):
    password = serializers.CharField(min_length = 6 , max_length = 68 , write_only =True)
    token = serializers.CharField(min_length = 1, write_only =True)
    uidb64 = serializers.CharField(min_length = 1, write_only =True)

    class Meta:
        fields = ['password', 'token' ,'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get("token")
            uidb64 = attrs.get('uidb64')
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id =id)
            if not PasswordResetTokenGenerator().check_token(user , token):
                raise AuthenticationFailed("token not valid for this user !" , 401 )
            user.set_password(password)
            user.save()
            return user

        except Exception as e :
            raise AuthenticationFailed("token not valid " , 401)

        return super().validate(attrs)