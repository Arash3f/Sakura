# Generated by Django 3.2.5 on 2021-08-18 02:26

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', django_jalali.db.models.jDateField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='journal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('debtor', models.IntegerField()),
                ('creditor', models.IntegerField()),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journals', to='admin_panel_store_karaj.document')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journals', to='admin_panel_store_karaj.product')),
            ],
        ),
    ]