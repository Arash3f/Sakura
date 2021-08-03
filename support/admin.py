from django.contrib import admin
from support import models


@admin.register(models.Conversation)
class Conversation(admin.ModelAdmin):
    field = "__all__"
    list_display=[ 'get_user_username' , 'title' , 'status' , 'date' ]
    list_filter = ['title' , 'status']

@admin.register(models.Message)
class Message(admin.ModelAdmin):
    field = "__all__"
    list_display=[ 'get_user_username' , 'conversation']
    list_filter = ['conversation',]
