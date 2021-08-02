

from rest_framework import serializers 
from django.contrib.auth.models import User
from accounts.models import users
from django.contrib.auth import logout
from shopping.models import Order, OrderRow
from shopping.serializer import Order_serializer_helper_rows
from accounts.mail import send_email
from Sakura import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse

class User_Informations_Helper_Serialiaer(serializers.ModelSerializer): 

    username = serializers.CharField()
    email=serializers.EmailField()

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name" , "email")

class User_Informations_Serialiaer(serializers.ModelSerializer):

    user = User_Informations_Helper_Serialiaer(many=False)
    money = serializers.IntegerField(read_only=True)
    phone = serializers.CharField(read_only=True)

    class Meta:
        model = users
        fields = ("user", "phone", "money")
    
    
    def update(self, instance, validated_data):
        # for email :
        confirm_email = False
        current_site = settings.SITE_URL
        absurl = 'http://'+current_site

        request = self.context.get("request")

        new_first_name = validated_data['user']['first_name']
        new_last_name = validated_data['user']['last_name']
        new_email = validated_data['user']['email']
        new_username = validated_data['user']['username']

        user = request.user
        user.first_name=new_first_name
        user.last_name=new_last_name
        user.email=new_email
        user.username=new_username
        
        if new_email != instance.user.email :
            # for email :
            token = RefreshToken.for_user(user)
            relativeLink = reverse('email_confirm')
            absurl = 'http://'+current_site+relativeLink+str(token)
            confirm_email = True

            user.is_active = False
            logout(request)

        user.save()

        instance.user.first_name =new_first_name
        instance.user.last_name = new_last_name
        instance.user.email = new_email
        instance.user.username = new_username

        data={
            "username" : new_username,
            "confirm_email":confirm_email,
            "absurl":absurl
        }
        send_email(new_email , "change_user_informations.html" , data , "پشتیبانی" )

        instance.save()

        return instance

class User_Orders_Helper_Serialiaer(serializers.ModelSerializer):
    class Meta:
        model = OrderRow
        fields = ("product", "product_cost", "amount" , "price")
  
class User_Orders_Serialiaer(serializers.ModelSerializer):
    rows = Order_serializer_helper_rows(many=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("order_time", "status", "total_price" , "rows" ,"location")

    def get_status(self,obj):
        return obj.get_status_display()
    