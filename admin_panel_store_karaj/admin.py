from django.contrib import admin
from admin_panel_store_karaj import models
# Register your models here.

@admin.register(models.product)
class product(admin.ModelAdmin):
    field = "__all__"
@admin.register(models.journal)
class journal(admin.ModelAdmin):
    field = "__all__"
@admin.register(models.document)
class document(admin.ModelAdmin):
    field = "__all__"