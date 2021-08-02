from django.shortcuts import get_object_or_404, render
from rest_framework import (
                            generics,
                            mixins ,
                            status,
                            )
from panel.serializer import User_Informations_Serialiaer , User_Orders_Serialiaer
from accounts.models import users
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
                                        api_view, 
                                        permission_classes,
                                        )
from accounts.views import CustomValidation
from rest_framework.response import Response
from django.contrib.auth import logout
from shopping.models import Order
from django.db.models import Q

class user_information(generics.GenericAPIView ,mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
    serializer_class = User_Informations_Serialiaer
    queryset = users.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

@api_view(('PUT',))
@permission_classes([IsAuthenticated])
def change_password(request):
    try:
        old_password = request.data['old_password']
        new_password = request.data['new_password']
    except KeyError :
        raise CustomValidation('KeyError','error', status_code=status.HTTP_404_NOT_FOUND)

    user = request.user

    if user.check_password(old_password) :
        if len(new_password) >= 5 :
            user.set_password(new_password)
            user.save()
            logout(request)
            return Response({"success"} , status=status.HTTP_200_OK) 
        else:
            raise CustomValidation('Invalid new password','error', status_code=status.HTTP_404_NOT_FOUND)
    else:
        raise CustomValidation('Invalid old password','error', status_code=status.HTTP_404_NOT_FOUND)
    
class user_orders(generics.GenericAPIView ,mixins.ListModelMixin):
    serializer_class = User_Orders_Serialiaer
    queryset = Order.objects.filter(~Q(status=1))
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user_user=self.request.user)
        return obj

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    