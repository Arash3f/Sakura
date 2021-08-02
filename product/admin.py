from django.contrib import admin
from product import models
   
@admin.register(models.product)
class product(admin.ModelAdmin):
    field = "__all__"
    list_display=[ 'name' ,"inventory","sell","group","available" ]
    prepopulated_fields = {'slug': ('name',), }
    list_filter = ('group' , 'available')

@admin.register(models.ProductGallery)
class ProductGallery(admin.ModelAdmin):
    field = "__all__"
    list_display=[ 'product' ,"picture"]
    list_filter = ("product",)

@admin.register(models.Packs)
class Packs(admin.ModelAdmin):
    field = "__all__"
    list_display=[ 'title' ,"weight","parent"]
    list_filter = ("parent",)

@admin.register(models.Product_Cost)
class Product_Cost(admin.ModelAdmin):
    field = "__all__"
    list_display=[ 'product' ,"pack","discount",'available' , 'cost']
    list_filter = ("product",)

@admin.register(models.product_group)
class product_group(admin.ModelAdmin):
    field = "__all__"
    list_display=['name' , 'group']
    list_filter = ("group",)

@admin.register(models.comment)
class comment(admin.ModelAdmin):

    field = "__all__"
    list_display=['product' , 'user' , 'created' , 'active']
    list_filter = ("active",)