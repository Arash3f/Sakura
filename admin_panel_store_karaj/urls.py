from django.urls import path
from admin_panel_store_karaj import views

urlpatterns = [

	path('', views.panel_product , name="panel_product"),
	path('edit/<int:pk>/', views.product_edit , name="product_edit"),
	path('remove/<int:pk>/', views.product_remove , name="product_remove"),
	path('add/', views.product_add , name="product_add"),
	path('export/xls/', views.export_product_xls, name='export_product_xls'),
	# دفتر روزنامه
	path('document/', views.panel_document , name="panel_document"),
	path('document/add/', views.document_add , name="document_add"),
	path('document/edit/<int:pk>/', views.document_edit , name="document_edit"),
	path('document/export/xls/', views.export_document_xls , name="export_document_xls"),
	# # مرور حساب
	path('check_product/', views.check_product , name="check_product"),
	path('check_product/export/xls/', views.export_check_product_xls, name='export_check_product_xls'),
	
	path('report_one/', views.report_one, name='report_one'),

]