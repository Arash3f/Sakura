from product.serializer import (
    product_group_serializer ,
    product_list_serializer,
    product_serializer,
    product_search_group_serializer,
    comments_serializer,
    )
from product import models
from rest_framework import generics , mixins
from django.db.models import Q
from django.shortcuts import get_object_or_404
# for decode url slug :
from urllib.parse import unquote
from random import randint

# Pagination :
# override PageNumberPagination for product list :
from rest_framework.pagination import PageNumberPagination
class Standard_Results_Set_Pagination(PageNumberPagination):
    page_size_query_param = 'page_size'

# all product list :
class product_list(generics.GenericAPIView , mixins.ListModelMixin):
    serializer_class = product_list_serializer
    queryset = models.product.objects.all()
    pagination_class = Standard_Results_Set_Pagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# top product (sort by sell field)
class top_product(generics.GenericAPIView , mixins.ListModelMixin):
    serializer_class = product_list_serializer
    queryset = models.product.objects.all().order_by('-sell')[0:9]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# best product (sort by group [0])
class best_product(generics.GenericAPIView , mixins.ListModelMixin):
    serializer_class = product_list_serializer
    
    def get_queryset(self):
        group = models.product_group.objects.filter(group__isnull=True)
        if group.count() >= 1 :
            i = randint(0, group.count()-1)
            queryset = models.product.objects.filter(group__group=group[i])[0:9]
        # not have any group yet .
        else:
            queryset = models.product.objects.all().order_by('-sell')[0:9]

        return queryset
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# product page :
class product_page(generics.GenericAPIView , mixins.RetrieveModelMixin):
    serializer_class = product_serializer
    queryset = models.product.objects.all()
    lookup_field = 'slug'

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        new_lookup = self.kwargs[lookup_url_kwarg]
        new_lookup = unquote(new_lookup)
        new_lookup = unquote(new_lookup)
        filter_kwargs = {self.lookup_field: new_lookup}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

# similar product :
class similar_product(generics.GenericAPIView , mixins.ListModelMixin):
    serializer_class = product_list_serializer
    queryset = models.product.objects.all()

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        slug = unquote(slug)
        slug = unquote(slug)
        pd = models.product.objects.get(slug=slug)
        gp = pd.group.group
        return self.queryset.filter(~Q(slug = slug),group__group=gp).order_by("-sell")[0:9]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# search product :
class product_search(generics.GenericAPIView , mixins.ListModelMixin):
    serializer_class = product_list_serializer
    queryset = models.product.objects.all()
    pagination_class = Standard_Results_Set_Pagination

    def get_queryset(self):
        query_name = self.kwargs.get('slug')
        query_name = unquote(query_name)
        query_name = unquote(query_name)
        return self.queryset.filter(slug__contains=query_name)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# group :
class group_list(generics.GenericAPIView , mixins.ListModelMixin):
    serializer_class = product_group_serializer
    queryset = models.product_group.objects.all().order_by("-group")

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class product_search_group(generics.GenericAPIView , mixins.ListModelMixin):
    serializer_class = product_search_group_serializer
    queryset = models.product_group.objects.all()
    pagination_class = Standard_Results_Set_Pagination

    def get_queryset(self):
        query_name = self.kwargs.get('slug')
        query_name = unquote(query_name)
        query_name = unquote(query_name)
        return self.queryset.filter(slug=query_name)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class comments(generics.GenericAPIView , mixins.ListModelMixin):
    serializer_class = comments_serializer
    queryset = models.comment.objects.filter(active=True)
    pagination_class = Standard_Results_Set_Pagination

    def get_queryset(self):
        query_name = self.kwargs.get('slug')
        query_name = unquote(query_name)
        query_name = unquote(query_name)
        return self.queryset.filter(product__slug=query_name)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)