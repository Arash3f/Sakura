from site_model.models import (Private_Site_Information ,
                                About_Us ,
                                Contact_Us,
                                FAQ_model,
                                Site_Information_Gallery,
                                BUGS,
                                )
from rest_framework import serializers

from accounts.mail import send_email
from Sakura import settings

class site_model_serializer(serializers.ModelSerializer):
    product_img_1 =serializers.SerializerMethodField('get_product_img_1_url')
    product_img_2 =serializers.SerializerMethodField('get_product_img_2_url')
    product_img_3 =serializers.SerializerMethodField('get_product_img_3_url')
    logo =serializers.SerializerMethodField('get_logo_url')
    sign_one =serializers.SerializerMethodField('get_sign_one_url')
    sign_two =serializers.SerializerMethodField('get_sign_two_url')
    site_img =serializers.SerializerMethodField('get_site_img_url')
    class Meta:
        model = Private_Site_Information
        fields = ["name","motto","phone","email","telegram_id","instagram_id","whatsapp_id","product_img_1" ,"product_img_2" ,"product_img_3" ,"logo"  ,"sign_one"  ,"sign_two"  ,"site_img" ,"title_1"   ,"body_1"     , "title_2"   ,   "body_2"  ]

    def get_product_img_1_url(self, obj):
        return obj.product_img_1.url
    def get_product_img_2_url(self, obj):
        return obj.product_img_2.url
    def get_product_img_3_url(self, obj):
        return obj.product_img_3.url
    def get_logo_url(self, obj):
        return obj.logo.url
    def get_sign_one_url(self, obj):
        return obj.sign_one.url
    def get_sign_two_url(self, obj):
        return obj.sign_two.url
    def get_site_img_url(self, obj):
        return obj.site_img.url

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

class bugs_serializer(serializers.ModelSerializer):
    
    class Meta:
        model = BUGS
        fields = '__all__'

class FAQ_serializer(serializers.ModelSerializer):

    class Meta :
        model = FAQ_model 
        fields= '__all__'

class site_information_gallery_serializer(serializers.ModelSerializer):
    class Meta :
        model = Site_Information_Gallery 
        fields= '__all__'