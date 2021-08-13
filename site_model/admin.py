from django.contrib import admin
from site_model import models

@admin.register(models.Private_Site_Information)
class Private_Site_Information(admin.ModelAdmin):
    field = "__all__"
    list_display=[ 'name' ]

@admin.register(models.About_Us)
class About_Us(admin.ModelAdmin):
    field = "__all__"
    list_display=[ 'title' , 'sub_title']

@admin.register(models.Contact_Us)
class Contact_Us(admin.ModelAdmin):
    field = "__all__"
    list_display=[ 'get_title_display' , 'name' , 'email' , 'phone']
    list_filter = ('title' , )

@admin.register(models.FAQ_model)
class FAQ_model(admin.ModelAdmin):
    field = "__all__"

@admin.register(models.Site_Information_Gallery)
class Site_Information_Gallery(admin.ModelAdmin):
    field = "__all__"
    