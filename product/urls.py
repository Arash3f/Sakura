from django.urls import path , re_path
from product import views

urlpatterns = [

    # product :
    path('api/v1/product_list/', views.product_list.as_view() , name="product_list"),
    path('api/v1/top_product/' , views.top_product.as_view()  , name="top_product"),
    path('api/v1/last_product/', views.last_product.as_view() , name="last_product"),
    
    re_path(r'api/v1/product/(?P<slug>([^/]+))/comments/', views.comments.as_view() , name="comments"),
    re_path(r'api/v1/product/(?P<slug>([^/]+))/', views.product_page.as_view()),
    re_path(r'api/v1/similar_product/(?P<slug>([^/]+))/', views.similar_product.as_view(), name="similar_product"),
	re_path(r'api/v1/search/group/(?P<slug>([^/]+))/' , views.product_search_group.as_view() , name = "product_search_group"),
	re_path(r'api/v1/search/(?P<slug>([^/]+))/' , views.product_search.as_view() , name = "search_product"),
    
    # groups :
    path('api/v1/group_list/', views.group_list.as_view()),
]