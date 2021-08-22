from django.urls import path
from admin_panel_accounts import views

urlpatterns = [

	path('', views.panel_accounts , name="panel_accounts"),
	path('user/detail/<int:pk>/', views.user_detail , name="user_detail"),
	path('user/edit/<int:pk>/', views.user_edit , name="user_edit"),
	path('export/xls/', views.export_users_xls, name='export_users_xls'),

]