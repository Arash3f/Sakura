from django.shortcuts import render
from support.models import (
    Conversation,
    Message,
)
from support.serializer import (
    create_conversation_serializer,
    conversation_serializer,
    create_message_serializer,
)
from rest_framework import (generics,
                            mixins,
                            status,
                            )
from product.views import Standard_Results_Set_Pagination

class support_create_conversation(generics.GenericAPIView , mixins.CreateModelMixin):
    serializer_class = create_conversation_serializer
    queryset = Conversation.objects.all()
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class support_conversation(generics.GenericAPIView , mixins.ListModelMixin):
    serializer_class = conversation_serializer
    queryset = Conversation.objects.all()
    pagination_class = Standard_Results_Set_Pagination

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class support_create_message(generics.GenericAPIView , mixins.CreateModelMixin):
    serializer_class = create_message_serializer
    queryset = Message.objects.all()
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)