from site_model.serializer import(site_model_serializer ,
                                    about_we_serializer ,
                                    contact_us_serializer,
                                    FAQ_serializer,
                                    site_information_gallery_serializer,
                                    )
from site_model.models import (Private_Site_Information ,
                                About_Us ,
                                Contact_Us , 
                                FAQ_model,
                                Site_Information_Gallery,
                                )
from rest_framework import (generics,
                            mixins,
                            status
                            )
from rest_framework.response import Response

class site_information(generics.GenericAPIView , mixins.ListModelMixin):
    serializer_class = site_model_serializer
    queryset = Private_Site_Information.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # create site_ditaio (have jast 1 object)
    # def post(self, request, *args, **kwargs):
    #     if Private_Site_Information.objects.all().count() >= 1 :
    #         text = "Cannot create a new object. Please modify or delete object 1"
    #         return Response({text},status=status.HTTP_406_NOT_ACCEPTABLE)
    #     else:
    #         return self.create(request, *args, **kwargs)

class slider_gallery(generics.GenericAPIView , mixins.ListModelMixin):
    serializer_class = site_information_gallery_serializer
    queryset = Site_Information_Gallery.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
        
class About_Us(generics.GenericAPIView , mixins.ListModelMixin , mixins.CreateModelMixin):
    serializer_class = about_we_serializer
    queryset = About_Us.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class contact_us(generics.GenericAPIView , mixins.ListModelMixin , mixins.CreateModelMixin):
    serializer_class = contact_us_serializer
    queryset = Contact_Us.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class FAQ(generics.GenericAPIView , mixins.ListModelMixin):
    serializer_class = FAQ_serializer
    queryset = FAQ_model.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)