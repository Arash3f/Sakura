from django.db import models
from django_jalali.db import models as jmodels
# Create your models here.


class account(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length= 30 , unique=True)

    def __str__(self):
        return str(self.id)

class document(models.Model):
    date = date = jmodels.jDateField()
    description = models.TextField()

    def __str__(self):
        return str(self.id)

class journal2(models.Model):
    document = models.ForeignKey('document' , on_delete=models.CASCADE , related_name='journals')
    account = models.ForeignKey('account' , related_name="journals" , on_delete=models.CASCADE)
    description = models.TextField()
    debtor = models.IntegerField()
    creditor = models.IntegerField()

    def __str__(self):
        return str(self.account.id)
