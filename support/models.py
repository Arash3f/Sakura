from django.db import models
from accounts.models import users
from django.contrib.auth.models import User

class Conversation(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    MY_CHOICES_TITLE = [("1",'پیشنهاد'),
                ("2",'انتقاد یا شکایت'),
                ("3","مدیریت"),
                ("4",'حسابداری'),
                ("5",'سایر موضوعات')]
    MY_CHOICES_STATUS = [("1",'باز'),
                ("2",'بسته')]

    title = models.CharField(verbose_name="عنوان" ,choices=MY_CHOICES_TITLE , max_length = 100 , blank=True , null = True )
    status = models.CharField(verbose_name="وضعیت" ,choices=MY_CHOICES_STATUS , max_length = 100 , default=1)
    date = models.DateTimeField(verbose_name="تاریخ تشکیل مکالمه " , auto_now=True)

    class Meta:
        verbose_name = ("مکالمه های پشتیبانی ")
        verbose_name_plural = ("مکالمه")
    
    def __str__(self):
        return self.title

    def get_user_username(self):
        return self.user.username

class Message(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(verbose_name="تاریخ تشکیل مکالمه " , auto_now=True)
    conversation = models.ForeignKey('Conversation' , on_delete=models.CASCADE , related_name="messages")

    class Meta:
        verbose_name = ("پیام های مکالمه پشتیبانی ")
        verbose_name_plural = ("پیام")
        ordering = ['-date']

    def get_user_username(self):
        return self.user.username