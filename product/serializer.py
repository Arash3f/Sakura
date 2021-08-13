from product.models import (
    product ,
    Packs ,
    Product_Cost , 
    ProductGallery ,
    product_group,
    comment,
)
from rest_framework import serializers

class product_serializer_helper_picture(serializers.ModelSerializer):
    class Meta:
        model = ProductGallery
        fields =('picture',)
        
class product_list_serializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField()
    
    class Meta:
        model = product
        fields = ('slug','name','show_cost','available','picture')

    def get_picture(self, obj):
        query = ProductGallery.objects.filter(product=obj , active=True)[:2] 
        serializer = product_serializer_helper_picture(query, many=True)
        return serializer.data

# ************************************************************************

class product_serializer_helper_cost(serializers.ModelSerializer):
    class Meta:
        model = Product_Cost
        fields = ('id','pack' , 'cost' ,'discount' , 'available' )
        depth = 1

class product_serializer(serializers.ModelSerializer):
    product_cost = product_serializer_helper_cost(many=True)
    picture = product_serializer_helper_picture(many=True )

    class Meta:
        model = product
        fields = ('id','name','inventory','available','product_cost','picture' ,'description')
        

# ************************************************************************

class product_group_serializer(serializers.ModelSerializer):

    class Meta:
        model = product_group
        fields = ('id','name' ,'group'  , 'picture' , 'slug')


class product_search_group_serializer(serializers.ModelSerializer):
    products = product_list_serializer(many=True)
    class Meta:
        model = product_group
        fields = ('id','name' ,'products' )

class comments_serializer(serializers.ModelSerializer):

    class Meta:
        model = comment
        fields = ('user','parent' ,'body'  , 'created')