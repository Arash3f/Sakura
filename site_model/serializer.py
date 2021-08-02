from site_model.models import (Private_Site_Information ,
                                About_Us ,
                                Contact_Us,
                                FAQ_model,
                                )
from rest_framework import serializers

from accounts.mail import send_email
from Sakura import settings

class site_model_serializer(serializers.ModelSerializer):
    
    class Meta:
        model = Private_Site_Information
        fields = '__all__'

class about_we_serializer(serializers.ModelSerializer):
    
    class Meta:
        model = About_Us
        fields = '__all__'

class contact_us_serializer(serializers.ModelSerializer):
    
    class Meta:
        model = Contact_Us
        fields = '__all__'

    def create(self, validated_data):
        current_site = settings.SITE_URL
        absurl = 'http://'+current_site
        email = validated_data["email"]
        data={
            "name" : validated_data["name"],
            'email' : validated_data["email"],
            "absurl":absurl
        }
        send_email(email , "contact.html" , data , "پشتیبانی" )
        super().create(validated_data)
        return validated_data

class FAQ_serializer(serializers.ModelSerializer):

    class Meta :
        model = FAQ_model 
        fields= '__all__'