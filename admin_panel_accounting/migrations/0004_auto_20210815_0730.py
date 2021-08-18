# Generated by Django 3.2.5 on 2021-08-15 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel_accounting', '0003_alter_account_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='journal',
            name='date',
        ),
        migrations.AddField(
            model_name='journal',
            name='document',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='journals', to='admin_panel_accounting.document'),
            preserve_default=False,
        ),
    ]
