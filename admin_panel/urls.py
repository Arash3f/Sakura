from django.urls import path , include
from admin_panel import views

urlpatterns = [

	path('login/', views.login, name='panel_login'),
	path('logout/', views.logout_user),
	path('', views.panel , name="panel"),

	# include :
	path('accounts/', include('admin_panel_accounts.urls')),
	path('accounting/', include('admin_panel_accounting.urls')),
	path('materials/', include('admin_panel_store_materials.urls')),
	path('product/', include('admin_panel_store_product.urls')),
	path('product_karaj/', include('admin_panel_store_karaj.urls')),


]