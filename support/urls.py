from django.urls import path
from support import views

urlpatterns = [

	path("api/v1/conversation/create" , views.support_create_conversation.as_view() , name = "support_create_conversation"),
	path("api/v1/conversation/" , views.support_conversation.as_view() , name = "support_conversation"),
	path("api/v1/message/create" , views.support_create_message.as_view() , name = "support_create_message"),

]