from django.urls import path
from admin_panel_accounting import views

urlpatterns = [

	path('account/', views.panel_accounting , name="panel_accounting"),
	path('account/edit/<int:pk>/', views.account_edit , name="account_edit"),
	path('account/remove/<int:pk>/', views.account_remove , name="account_remove"),
	path('account/add/', views.account_add , name="account_add"),
	path('account/export/xls/', views.export_accounts_xls, name='export_accounts_xls'),
	# دفتر روزنامه
	path('document/', views.panel_document , name="panel_document"),
	path('document/add/', views.document_add , name="document_add"),
	path('document/edit/<int:pk>/', views.document_edit , name="document_edit"),
	path('document/export/xls/', views.export_document_xls , name="export_document_xls"),
	# مرور حساب
	path('check_accounts/', views.check_accounts , name="check_accounts"),
	path('check_accounts/export/xls/', views.export_check_accounts_xls, name='export_check_accounts_xls'),
	
	path('report_one/', views.report_one, name='report_one'),

]