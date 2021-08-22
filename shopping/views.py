from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import (generics,
                            mixins,
                            status,
                            )
from rest_framework.decorators import (api_view, 
                                        permission_classes,
                                        )
from product.models import Product_Cost , product
from shopping.serializer import Order_Row_serializer , Order_serializer
from shopping.models import OrderRow , Order
from accounts.views import CustomValidation
from accounts.models import users

class Add_Order_Row(generics.GenericAPIView , mixins.CreateModelMixin ):
    serializer_class = Order_Row_serializer
    permission_classes = [IsAuthenticated,]
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs )
    
# ************************************************************************

class Show_Order(generics.GenericAPIView  , mixins.ListModelMixin):
    serializer_class = Order_serializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated,]
    
    def get_queryset(self):
        user = self.request.user
        user = users.objects.get(user=user)
        user_order = Order.objects.filter(user_id = user.id , status = 1)
        return user_order
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# ************************************************************************
   
@api_view(('POST',))
@permission_classes([IsAuthenticated])
def modify_Order_row(request):
    user = request.user
    try:
        request_product_id = request.data["product"]
        pack = request.data["pack"]
        amount =  request.data["amount"]
    
        request_product = product.objects.get(id = request_product_id )
        th_user = users.objects.get(user=user)
        order = Order.objects.get(user = th_user , status=1)
        cost = Product_Cost.objects.get(product_id = request_product.id , pack_id = pack).cost
        order_row =OrderRow.objects.filter(order = order , product_id = request_product.id)[0]
    
    except :
        raise CustomValidation('Incomplete information','error', status_code=status.HTTP_400_BAD_REQUEST)


    new_amount = int(amount[1:])
    if amount[0] == "-":

        if order_row.amount <= new_amount:
            order.Decrease_total_price( int(order_row.amount),cost )
            order_row.delete()
        else : 
            order_row.Decrease_amount(new_amount)
            order_row.Decrease_price(new_amount , cost)
            order.Decrease_total_price(new_amount,cost)
        
    elif amount[0] == "+":

        if request_product.inventory < order_row.amount + int(amount[1:]) :
            raise CustomValidation('Product inventory is not enough','inventory', status_code=status.HTTP_400_BAD_REQUEST)
        else : 
            order_row.Increase_amount(new_amount)
            order_row.Increase_price(new_amount , cost)
            order.Increase_total_price(new_amount , cost)
    
    else:
        raise CustomValidation('Incomplete information','error', status_code=status.HTTP_400_BAD_REQUEST)
    
    return Response({"Success"} , status=status.HTTP_200_OK)

# ************************************************************************

@api_view(('POST',))
@permission_classes([IsAuthenticated]) 
def Cancel_Order_Row(request):
    user = request.user
    try:
        user = users.objects.get(user = user)
        request_product_id = request.data["product"]
        pack = request.data["pack"]
        order = Order.objects.get(user_id = user.id , status=1)
        request_product = product.objects.get(id = request_product_id )
        cost = Product_Cost.objects.get(product_id = request_product.id , pack_id = pack).cost
        order_row =OrderRow.objects.filter(order = order , product_id = request_product.id)[0]
        order.Decrease_total_price(int(order_row.amount) , cost)
        order_row.delete()
        return Response({"order_row deleted"} , status=status.HTTP_200_OK)
    except:
        raise CustomValidation('Incomplete information','error', status_code=status.HTTP_400_BAD_REQUEST)

class Show_all_Order(generics.GenericAPIView  , mixins.ListModelMixin):
    serializer_class = Order_serializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated,]
    
    def get_queryset(self):
        user = self.request.user
        user = users.objects.get(user=user)
        order = Order.objects.filter(user= user )
        return order
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)