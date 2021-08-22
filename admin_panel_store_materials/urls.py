from django.urls import path
from admin_panel_store_materials import views

app_name = "admin_panel_materials"

urlpatterns = [

	path('', views.panel_materials , name="panel_materials"),
	path('edit/<int:pk>/', views.materials_edit , name="materials_edit"),
	path('remove/<int:pk>/', views.materials_remove , name="materials_remove"),
	path('add/', views.materials_add , name="materials_add"),
	path('export/xls/', views.export_materials_xls, name='export_materials_xls'),
	# دفتر روزنامه
	path('document/', views.panel_document , name="panel_document"),
	path('document/add/', views.document_add , name="document_add"),
	path('document/edit/<int:pk>/', views.document_edit , name="document_edit"),
	path('document/remove/<int:pk>/', views.document_remove , name="document_remove"),
	path('document/export/xls/', views.export_document_xls , name="export_document_xls"),
	# # مرور حساب
	path('check_materials/', views.check_materials , name="check_materials"),
	path('check_materials/export/xls/', views.export_check_materials_xls, name='export_check_materials_xls'),
	
	path('report_one/', views.report_one, name='report_one'),
	path('report_one/export/xls/<int:pk>/', views.export_check_report_xls, name='export_check_report_xls'),

]