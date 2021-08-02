from django.contrib import admin
from shopping import models

@admin.register(models.OrderRow)
class OrderRow(admin.ModelAdmin):
    field = "__all__"
    list_display = ['Order_row_user' , 'product' , 'amount' , 'product_cost'  , 'price' ]
    list_filter = ("product",)

@admin.register(models.Order)
class Order(admin.ModelAdmin):
    list_display = ['Order_user' , 'order_time' , 'status' , 'total_price' , 'location' ]
    list_filter = ["status",'order_time']

@admin.register(models.province)
class province(admin.ModelAdmin):
    list_display = ['name' , 'cost']