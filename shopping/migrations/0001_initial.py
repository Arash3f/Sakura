# Generated by Django 3.2.5 on 2021-08-02 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_time', models.DateTimeField(null=True)),
                ('status', models.IntegerField(choices=[(1, 'در حال خرید'), (2, 'ثبت\u200cشده'), (3, 'لغوشده'), (4, 'ارسال\u200cشده')])),
                ('total_price', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'سبد',
                'verbose_name_plural': 'سبد ها',
            },
        ),
        migrations.CreateModel(
            name='province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('cost', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'موقعیت',
                'verbose_name_plural': 'موقعیت ها',
            },
        ),
        migrations.CreateModel(
            name='OrderRow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('price', models.IntegerField(default=0)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rows', to='shopping.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('product_cost', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.product_cost')),
            ],
            options={
                'verbose_name': 'ردیف',
                'verbose_name_plural': 'ردیف ها',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='location',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='shopping.province'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.users'),
        ),
    ]
