from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator , MinValueValidator
from ckeditor.fields import RichTextField

class product(models.Model):
    name        = models.CharField("نام کالا" ,max_length = 100 )
    slug        = models.SlugField(unique=True, allow_unicode=True, max_length=255)
    description = RichTextField(blank=True , null = True)
    inventory   = models.PositiveIntegerField(verbose_name='موجودی',validators=[MinValueValidator(1)] )
    available   = models.BooleanField(verbose_name="(موجودی)وضعیت" , default=True )
    sell        = models.IntegerField(verbose_name='تعداد فروش'  , default= 0 )
    show_cost   = models.IntegerField(verbose_name='قیمت نمایشی' , default= 0)
    # relations :
    group = models.ForeignKey('product_group' , verbose_name="گروه" , on_delete=models.CASCADE , related_name="products" )

    class Meta:
        unique_together = ['slug', 'name']
        verbose_name = ("کالا")
        verbose_name_plural = ("کالا ها")

    def __str__(self):
        return self.name

class ProductGallery(models.Model):
    picture = models.ImageField("عکس" ,upload_to = 'product/', blank=True , null = True)
    product = models.ForeignKey('Product', related_name="picture", on_delete=models.CASCADE)
    active = models.BooleanField(default=False, blank=True , null = True)

    class Meta:
        verbose_name = ("عکس ")
        verbose_name_plural = ("عکس ها")

class Packs(models.Model):
    title = models.CharField(verbose_name="عنوان" , max_length = 100 , blank=True , null = True )
    weight = models.PositiveIntegerField(verbose_name='اندازه' , blank=True , null = True)
    parent = models.ForeignKey('self' , verbose_name = "نوع" , on_delete=models.CASCADE , blank = True , null = True)

    class Meta:
        verbose_name = ("بسته")
        verbose_name_plural = ("بسته ها")

    def __str__(self):
        return self.title

class Product_Cost(models.Model):
    # relations :
    product = models.ForeignKey('product' ,related_name = "product_cost", verbose_name="کالا" , on_delete=models.CASCADE )
    pack = models.ForeignKey('packs' ,related_name = "product_cost", verbose_name="بسته" , on_delete=models.CASCADE )
    discount = models.PositiveIntegerField(verbose_name='تخفیف' ,default = 0 ,validators=[MaxValueValidator(99)])
    cost = models.IntegerField(verbose_name='قیمت' )
    # available for pack
    available = models.BooleanField(verbose_name="(بسته)وضعیت" , default=True  )
    
    class Meta:
        unique_together = [['product', 'pack']]
        verbose_name = ("قیمت")
        verbose_name_plural = ("قیمت ها")

    def __str__(self):
        return self.pack.title
    
    def p_cost(self):
        return "{:,}".format(int(self.cost))
    p_cost.short_description = "قیمت"

class product_group(models.Model):
    name = models.CharField("متن" ,max_length = 100 , blank=True , null = True ,help_text = "متن نمایشی")  
    slug        = models.SlugField(unique=True, allow_unicode=True, max_length=255)
    group = models.ForeignKey('self' ,related_name = "sub_group" ,verbose_name="سر گروه", on_delete=models.CASCADE , null=True , blank = True ,help_text = "درصورت داشتن سر گروه ، وارد شود ")
    picture = models.ImageField("عکس" ,upload_to = 'product_group/', blank=True , null = True)

    class Meta:
        unique_together = ['slug', 'name']
        verbose_name = ("دسته بندی")
        verbose_name_plural = ("دسته بندی ها")
    
    def __str__(self):
        return self.name

class comment(models.Model):
    product = models.ForeignKey("product", on_delete=models.CASCADE )
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = ("نظر")
        verbose_name_plural = ("نظرات")

    def __str__(self):
        return self.product.name