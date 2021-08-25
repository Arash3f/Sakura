from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# site detail ...
class Private_Site_Information(models.Model):
    # site_information :
    name          = models.CharField(verbose_name="نام سایت" ,max_length = 100 , blank=True , null = True )
    motto         = models.TextField(verbose_name="شعار" , blank=True , null = True)
    phone         = models.CharField(verbose_name="تلفون سایت" , max_length=11 , blank=True , null = True)
    email         = models.EmailField(verbose_name = "ایمیل سایت" ,max_length = 100 , blank=True , null = True)
    telegram_id   = models.CharField(verbose_name="آدرس تلگرام سایت" ,max_length = 100 , blank=True , null = True)
    instagram_id  = models.CharField(verbose_name="آدرس اینستاگرام سایت" ,max_length = 100 , blank=True , null = True)
    whatsapp_id   = models.CharField(verbose_name="آدرس واتس آپ سایت" ,max_length = 100 , blank=True , null = True)

    # part one (img) :
    product_img_1 = models.ImageField(verbose_name="۱ عکس" ,upload_to = 'main_site/', blank=True , null = True)
    product_img_2 = models.ImageField(verbose_name="۲ عکس" ,upload_to = 'main_site/', blank=True , null = True)
    product_img_3 = models.ImageField(verbose_name="۳ عکس" ,upload_to = 'main_site/', blank=True , null = True)
    
    # part one (img) :
    logo = models.ImageField(verbose_name="عکس لوگو" ,upload_to = 'logo/', blank=True , null = True)
    sign_one = models.ImageField(verbose_name="عکس نماد" ,upload_to = 'sign/', blank=True , null = True)
    sign_two = models.ImageField(verbose_name="عکس نماد " ,upload_to = 'sign/', blank=True , null = True)
    site_img = models.ImageField(verbose_name="عکس  " ,upload_to = 'site/', blank=True , null = True)

    # part one (body) :
    title_1       = models.CharField(verbose_name="سر تیتر" ,max_length = 100 , blank=True , null = True )
    body_1        = models.TextField(verbose_name="متن" , blank=True , null = True)
    title_2       = models.CharField(verbose_name="سر تیتر" ,max_length = 100 , blank=True , null = True )
    body_2        = models.TextField(verbose_name="متن" , blank=True , null = True)

    class Meta:
        verbose_name = ("اطلاعات")
        verbose_name_plural = ("اطلاعات")

    def __str__(self):
        return self.name

class Site_Information_Gallery(models.Model):
    picture = models.ImageField("عکس" ,upload_to = 'main_site/gallery/', blank=True , null = True)

    class Meta:
        verbose_name = ("عکس ")
        verbose_name_plural = ("عکس ها")

class About_Us(models.Model):
    title = models.CharField(verbose_name="سر تیتر" ,max_length = 100 , blank=True , null = True )
    sub_title = models.CharField(verbose_name="توضیح کوتاه" ,max_length = 100 , blank=True , null = True )
    body = models.TextField(verbose_name="متن" , blank=True , null = True)
    picture = models.ImageField(verbose_name="عکس" ,upload_to = 'About_Us/', blank=True , null = True)

    class Meta:
        verbose_name = ("دربارهی ما")
        verbose_name_plural = ("درباره ی ما")

    def __str__(self):
        return self.title


class Contact_Us(models.Model):
    MY_CHOICES = [("1",'پیشنهاد'),
                    ("2",'انتقاد یا شکایت'),
                    ("3","مدیریت"),
                    ("4",'حسابداری'),
                    ("5",'سایر موضوعات')]

    title = models.CharField(verbose_name="عنوان" ,choices=MY_CHOICES , max_length = 100 , blank=True , null = True )
    name = models.CharField(verbose_name="نام" ,max_length = 100 , blank=True , null = True )
    email = models.EmailField(verbose_name="ایمیل" ,max_length = 100 , blank=True , null = True)
    phone = models.CharField(verbose_name="شماره تماس" , max_length=11 , blank=True , null = True)
    body = models.TextField(verbose_name="متن" , blank=True , null = True)

    class Meta:
        verbose_name = ("ارتباط با ما")
        verbose_name_plural = ("ارتباط با ما")

    def __str__(self):
        return self.title

class FAQ_model(models.Model):
    title = models.CharField(verbose_name="عنوان" , max_length = 100 , blank=True , null = True )
    body = RichTextField(verbose_name="متن" , blank=True , null = True)

    class Meta:
        verbose_name = ("سوالات متداول")
        verbose_name_plural = ("سوالات")

    def __str__(self):
        return self.title

class BUGS(models.Model):
    name = models.CharField(verbose_name="نام" ,max_length = 100 , blank=True , null = True )
    last_name = models.CharField(verbose_name="فامیل" ,max_length = 100 , blank=True , null = True )
    picture = models.ImageField(verbose_name="عکس" ,upload_to = 'bugs/', blank=True , null = True)
    title = models.CharField(verbose_name="عنوان" , max_length = 100 , blank=True , null = True )
    body = models.TextField(verbose_name="متن" , blank=True , null = True)

    class Meta:
        verbose_name = ("باگ ها")
        verbose_name_plural = ("مشکل باگ")

    def __str__(self):
        return self.title
    
    