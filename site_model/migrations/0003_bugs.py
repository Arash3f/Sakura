# Generated by Django 3.2.5 on 2021-08-21 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_model', '0002_auto_20210813_1927'),
    ]

    operations = [
        migrations.CreateModel(
            name='BUGS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام')),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='فامیل')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='bugs/', verbose_name='عکس')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='عنوان')),
                ('body', models.TextField(blank=True, null=True, verbose_name='متن')),
            ],
            options={
                'verbose_name': 'باگ ها',
                'verbose_name_plural': 'مشکل باگ',
            },
        ),
    ]