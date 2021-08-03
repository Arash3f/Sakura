from site_model.models import (
    Private_Site_Information ,
    About_Us ,
)
from support.models import (
    Conversation,
    Message,
)
from rest_framework import serializers, status
from accounts.views import CustomValidation
from django.contrib.auth.models import User

class create_conversation_serializer(serializers.Serializer):
    MY_CHOICES_TITLE = [("1",'پیشنهاد'),
                ("2",'انتقاد یا شکایت'),
                ("3","مدیریت"),
                ("4",'حسابداری'),
                ("5",'سایر موضوعات')]

    body = serializers.CharField(style={'base_template': 'textarea.html'} )
    title = serializers.ChoiceField(choices=MY_CHOICES_TITLE)

    def create(self, validated_data):
        user = self.context['request'].user
        body =validated_data['body']
        title =validated_data['title']
        try:
            new_conversation = Conversation.objects.create(user =user , title = title )
            new_conversation.save()

            new_message = Message.objects.create(user=user , body = body , conversation = new_conversation)
            new_message.save()
        except:
            raise CustomValidation('Cant create !','error', status_code=status.HTTP_400_BAD_REQUEST)

        return validated_data

class conversation_serializer_Helper_User(serializers.ModelSerializer):
    class Meta:
            model = User
            fields = ('username',)
 

class conversation_serializer_Helper_Messages(serializers.ModelSerializer):
    user = conversation_serializer_Helper_User()
    # user = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='email'
    #  )
    class Meta:
            model = Message
            fields = ('body' , 'date' ,'user')

class conversation_serializer(serializers.ModelSerializer):
    messages = conversation_serializer_Helper_Messages(many=True)
    class Meta:
        model = Conversation
        fields = ('id','title' , 'status' , 'date' , 'messages')

class create_message_serializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = ('body' , 'conversation')

    def create(self, validated_data):
        conversation = validated_data['conversation']
        user = self.context['request'].user
        body =validated_data['body']
        
        try:
            new_message = Message.objects.create(user=user , body = body , conversation = conversation)
            new_message.save()

        except:
            raise CustomValidation('Cant create !','error', status_code=status.HTTP_400_BAD_REQUEST)

        return validated_data