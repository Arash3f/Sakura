# Generated by Django 3.2.5 on 2021-08-25 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_model', '0004_auto_20210825_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='private_site_information',
            name='site_img',
            field=models.ImageField(blank=True, null=True, upload_to='site/', verbose_name='عکس  '),
        ),
        migrations.AlterField(
            model_name='private_site_information',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='logo/', verbose_name='عکس لوگو'),
        ),
        migrations.AlterField(
            model_name='private_site_information',
            name='product_img_1',
            field=models.ImageField(blank=True, null=True, upload_to='main_site/', verbose_name='۱ عکس'),
        ),
        migrations.AlterField(
            model_name='private_site_information',
            name='product_img_2',
            field=models.ImageField(blank=True, null=True, upload_to='main_site/', verbose_name='۲ عکس'),
        ),
        migrations.AlterField(
            model_name='private_site_information',
            name='product_img_3',
            field=models.ImageField(blank=True, null=True, upload_to='main_site/', verbose_name='۳ عکس'),
        ),
        migrations.AlterField(
            model_name='private_site_information',
            name='sign_one',
            field=models.ImageField(blank=True, null=True, upload_to='sign/', verbose_name='عکس نماد'),
        ),
        migrations.AlterField(
            model_name='private_site_information',
            name='sign_two',
            field=models.ImageField(blank=True, null=True, upload_to='sign/', verbose_name='عکس نماد '),
        ),
    ]
