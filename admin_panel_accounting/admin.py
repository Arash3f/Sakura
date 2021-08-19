from django.contrib import admin
from admin_panel_accounting import models
# Register your models here.

@admin.register(models.account)
class account(admin.ModelAdmin):
    field = "__all__"
@admin.register(models.journal2)
class journal2(admin.ModelAdmin):
    field = "__all__"
@admin.register(models.document)
class document(admin.ModelAdmin):
    field = "__all__"


    