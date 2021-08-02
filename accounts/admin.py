from django.contrib import admin
from accounts import models

@admin.register(models.image_section)
class image_section(admin.ModelAdmin):
    field = "__all__"

@admin.register(models.users)
class users(admin.ModelAdmin):
    field = "__all__"
    list_display = ['__str__' ,'email', 'money' , 'registration_date']