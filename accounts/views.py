import os
import jwt
from Sakura import settings
from coreapi.compat import force_text
from datetime import datetime

# django :
from django.http import request
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import (
                                urlsafe_base64_decode, 
                                urlsafe_base64_encode,
                                )
from django.utils.encoding import (
                                DjangoUnicodeDecodeError, 
                                smart_bytes,
                                smart_str,
                                )

# rest :
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import (
                            generics,
                            mixins ,
                            status,
                            )
from rest_framework.decorators import (
                                        api_view, 
                                        permission_classes,
                                        )

# model : 
from shopping.models import Order, OrderRow
from accounts.models import (
                            image_section ,
                            users,
                            )

# serializer : 
from accounts.serializer import (
                        User_Register_Serialiaer ,
                        Request_Password_Reset_Email_Serializer , 
                        Set_New_Password_Serializer,
                        Check_Confirm_Email_serializer,
                        )

from accounts.mail import send_email

# custom validation :
class CustomValidation(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad request'

    def __init__(self, detail, field, status_code):
        if status_code is not None:self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_text(detail)}
        else: self.detail = {'detail': force_text(self.default_detail)}

# user register section :
class register_user(generics.GenericAPIView , mixins.CreateModelMixin):
    serializer_class = User_Register_Serialiaer
    
    
    def post(self, request, *args, **kwargs):
        try:
            username = request.data['username']
            email = request.data['email']
        except KeyError as e :
            raise CustomValidation('Incomplete information','error', status_code=status.HTTP_400_BAD_REQUEST)
        
        all_user = User.objects.all()
        new_json = {}

        # check available user with this username
        if all_user.filter(username = username):
            new_json['user'] = False
            # check available user with this email
            if all_user.filter(email = email):
                new_json['email'] = False
            else:
                new_json['email'] = True
            return Response(new_json , status=status.HTTP_200_OK)
        else:
            new_json['user'] = True
            # check available user with this email
            if all_user.filter(email = email):
                new_json['email'] = False
                return Response(new_json , status=status.HTTP_200_OK)
            else:
                # create user :
                self.create(request, *args, **kwargs)
                user = User.objects.get(email=email)
                token = RefreshToken.for_user(user)
                current_site = settings.SITE_URL
                relativeLink = reverse('email_confirm')
                absurl = 'http://'+current_site+relativeLink+str(token)
                data={
                        'username': user.username ,
                        'absurl' : absurl,
                        }
                send_email(email , "confirm_email.html" , data , "تایید ایمیل" )
                return Response({"success" : "Email sent "} , status=status.HTTP_200_OK)

# first user request for give email  
class Request_Password_Reset_Email(generics.GenericAPIView):
    serializer_class = Request_Password_Reset_Email_Serializer

    def post(self , request):

        serializer = self.serializer_class(request.data)
        try:
            email = request.data['email']
        except KeyError as e :
            raise CustomValidation('Incomplete information','error', status_code=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            request_user = User.objects.get(email=email)
# SEND EMAIL ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            uidb64 = urlsafe_base64_encode(smart_bytes(request_user.id))
            token = PasswordResetTokenGenerator().make_token(request_user)
            current_site = settings.SITE_URL
            relativeLink = reverse('check_reset_token' , kwargs={"uidb64" : uidb64 , "token" : token})
            absurl = 'http://'+current_site+relativeLink

            data = {
                    'username': request_user.username ,
                    'date' : datetime.now(),
                    'absurl' : absurl,
                    }

            send_email(email , "email_reset_password.html" , data ,"درخواست تغییر رمز")

        return Response({"success" : "Email sent "} , status=status.HTTP_200_OK)

# just check token for reset password :
@api_view(('GET',))
def Password_Token_Check(request, uidb64, token):
    try:
        id = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id =id )
        if not PasswordResetTokenGenerator().check_token(user , token):
            raise CustomValidation('token not vaid','error', status_code=status.HTTP_200_OK)

        return Response({  
            "success":True , 
            "message":"valid",
            "uidb64" : uidb64 , 
            "token" : token
        } , status = status.HTTP_200_OK)

    except DjangoUnicodeDecodeError:
        if not PasswordResetTokenGenerator().check_token(user):
            return Response({"error":"Unicode decoding error"} , status = status.HTTP_200_OK)

# change password
class Set_New_Password(generics.GenericAPIView):
    serializer_class = Set_New_Password_Serializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"success":"Password changed "} , status = status.HTTP_200_OK)

# confirm users email :
class Check_Confirm_Email(generics.GenericAPIView):
    serializer_class = Check_Confirm_Email_serializer

    def post(self, request):
        serializer =  self.serializer_class(request.data)
        try:
            token = request.data['token']
            pyload = jwt.decode(token,settings.SECRET_KEY)
            user = User.objects.get(id =pyload["user_id"] )

            if not user.is_active:
                user.is_active = True
                user.save()
                user2 = users.objects.create(user = user )
                Order.objects.create(
                    user = user2 ,
                    status = 1 ,
                )

            return Response({"success":"email activated"} , status = status.HTTP_200_OK)

        except jwt.ExpiredSignature as identifier:
            raise CustomValidation('activate expired','error', status_code=status.HTTP_200_OK)
        except jwt.exceptions.DecodeError as identifier:
            raise CustomValidation('token not vaid','error', status_code=status.HTTP_200_OK)
        except KeyError as e :
            raise CustomValidation('Incomplete information','error', status_code=status.HTTP_400_BAD_REQUEST)

@api_view(('GET',))
def login_pic(request):
    try:
        img = image_section.objects.all()[0].login_img
    except:
        raise CustomValidation('Not Found IMG','error', status_code=status.HTTP_404_NOT_FOUND)
    return Response({"url":img.url} , status=status.HTTP_200_OK)

@api_view(('GET',))
def register_pic(request):
    try:
        img = image_section.objects.all()[0].register_img
    except:
        raise CustomValidation('Not Found IMG','error', status_code=status.HTTP_404_NOT_FOUND)
    return Response({"url":img.url} , status=status.HTTP_200_OK)

@api_view(('GET',))
def re_password_pic(request):
    try:
        img = image_section.objects.all()[0].re_password_img
    except:
        raise CustomValidation('Not Found IMG','error', status_code=status.HTTP_404_NOT_FOUND)
    return Response({"url":img.url} , status=status.HTTP_200_OK)

@api_view(('GET',))
@permission_classes([IsAuthenticated])
def get_user_username(request):
    user = request.user
    rows = OrderRow.objects.filter(order__user__user = user).count()
    if user.first_name:
        return Response({"username":user.first_name,"order rows":rows} , status=status.HTTP_200_OK) 
    else:
        return Response({"username":user.username,"order rows":rows} , status=status.HTTP_200_OK) 