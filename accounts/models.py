from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# unique User email field 
User._meta.get_field('email')._unique = True

# Create your models here.
class users(models.Model):
    # Validator for customize phone field
    phone_regex = RegexValidator(regex=r'((\+|00)98|0)9\d{9}', message="Phone number must be entered in the format: '09176666666'. Up to 11 digits allowed.")

    user     = models.OneToOneField(User , related_name='user',  on_delete=models.CASCADE)
    phone    = models.CharField(validators=[phone_regex], max_length=11, blank=True)
    money    = models.IntegerField("money" , default=0 )
    registration_date = models.DateField("registration date" , auto_now_add=True)
    picture  = models.ImageField("picture" , upload_to = "users_picture/" , null=True , blank=True)

    class Meta:
        verbose_name = ("کاربر")
        verbose_name_plural = ("کاربران")

    def __str__(self):
        return self.user.username
        
    def email(self):
        return self.user.email

class image_section(models.Model):
    login_img       = models.ImageField("login"       , upload_to = "login_img/" , null=True , blank=True ,help_text = "عکس برای صفحه لاگین ")
    register_img    = models.ImageField("register"    , upload_to = "register_img/" , null=True , blank=True ,help_text = "عکس برای صفحه ثبت نام ")
    re_password_img = models.ImageField("re password" , upload_to = "re_password_img/" , null=True , blank=True ,help_text = "عکس برای صفحه فراموشی رمز ")
    
    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = ("تصویر")
        verbose_name_plural = ("تصاویر")