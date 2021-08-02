from rest_framework import serializers , status
from accounts.models import users
from shopping.models import OrderRow , Order
from product.models import Packs, ProductGallery, Product_Cost, product
from accounts.views import CustomValidation

class Order_Row_serializer(serializers.ModelSerializer):

    def create(self, validated_data):

        user = users.objects.get(user_id = self.context['request'].user.id)
        product = validated_data['product']
        amount = validated_data['amount']
        product_cost = validated_data['product_cost']

        # check pack match product :
        if product_cost.product == product :
            # check user status :
            if Order.objects.filter(user = user, status= 1).count() == 1 :

                user_order = Order.objects.get(user = user)
                old_row = OrderRow.objects.filter(
                    product = product,
                    order = user_order,
                    product_cost = product_cost,
                    )

                # check user have old order row with this product and pack :
                if old_row.count() == 1:

                    if product.inventory < amount+old_row[0].amount :
                        raise CustomValidation('Product inventory is not enough ','inventory', status_code=status.HTTP_400_BAD_REQUEST)
                    
                    user_order.Increase_total_price(product_cost.cost,amount)
                    user_row = old_row[0]
                    user_row.Increase_amount(amount)
                    user_row.Increase_price(product_cost.cost , amount)
                    return user_row

                # no order row :
                else:

                    if product.inventory < amount :
                        raise CustomValidation('Product inventory is not enough ','inventory', status_code=status.HTTP_400_BAD_REQUEST)
                    
                    user_order.Increase_total_price(product_cost.cost,amount)

                    new_order_row = OrderRow.objects.create(
                        product = product,
                        order = user_order ,
                        amount = amount,
                        product_cost = product_cost,
                        price = product_cost.cost*amount,
                    )
                    return new_order_row

            # user have no order (impossible :) )
            else:
                raise CustomValidation('User shoud have one Order','Order', status_code=status.HTTP_400_BAD_REQUEST)
        
        # product not match to pack
        else : 
            raise CustomValidation('pack not match to product','Invalid data', status_code=status.HTTP_400_BAD_REQUEST)
    
    class Meta:
        model = OrderRow
        fields = ('product' , 'amount' , 'product_cost')

# ************************************************************************     
class Order_serializer_helper_picture(serializers.ModelSerializer):

    class Meta:
        model = ProductGallery
        fields =('picture',)

class Order_serializer_helper_product(serializers.ModelSerializer):
    picture = Order_serializer_helper_picture(many=True )
    class Meta:
        model = product
        fields =("id","name" ,"slug" , "picture" , "available")

class Order_serializer_helper_pack(serializers.ModelSerializer):
    class Meta:
        model = Packs
        fields =('id' , "title", "weight" )

class Order_serializer_helper_product_cost(serializers.ModelSerializer):
    pack = Order_serializer_helper_pack()
    class Meta:
        model = Product_Cost
        fields =("pack", "discount" ,"available" ,  "cost" )

class Order_serializer_helper_rows(serializers.ModelSerializer):
    product = Order_serializer_helper_product()
    product_cost = Order_serializer_helper_product_cost()
    
    class Meta:
        model = OrderRow
        fields =("amount" ,"price" ,  "product" , "product_cost")

class Order_serializer(serializers.ModelSerializer):
    rows = Order_serializer_helper_rows(many=True)

    class Meta:
        model = Order
        fields = ('total_price' , 'rows')
        