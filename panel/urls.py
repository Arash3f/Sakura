from django.urls import path
from panel import views

urlpatterns = [

	path("api/v1/user_information/" , views.user_information.as_view() , name = "user_information"),
	path("api/v1/change_password/" , views.change_password , name = "change_password"),
	path("api/v1/user_orders/" , views.user_orders.as_view() , name = "user_orders"),

]