from django.urls import path , include
from admin_panel import views

urlpatterns = [

	path('login/', views.login, name='panel_login'),
	path('logout/', views.logout_user),
	path('', views.panel , name="panel"),

	# include :
	path('accounts/', include('admin_panel_accounts.urls')),


]