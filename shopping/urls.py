from django.urls import path
from shopping import views

urlpatterns = [
    path("api/v1/new_Order_Row/" , views.Add_Order_Row.as_view() , name='Add_Order_Row'),
    path("api/v1/Show_Order/" , views.Show_Order.as_view() , name='Show_Order'),
    path("api/v1/modify_Order_Row/" , views.modify_Order_row , name='modify_Order'),
    path("api/v1/Cancel_Order_Row/" , views.Cancel_Order_Row , name='Cancel_Order_Row'),
    
    # path("v1/Show_all_Order/" , views.Show_all_Order.as_view() , name='Show_all_Order'),
]