# Generated by Django 3.2.5 on 2021-08-12 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accounting_score_rows',
            name='accounting_score',
        ),
        migrations.RemoveField(
            model_name='accounting_score_rows',
            name='accounts_form',
        ),
        migrations.DeleteModel(
            name='Accounting_Score',
        ),
        migrations.DeleteModel(
            name='Accounting_Score_Rows',
        ),
        migrations.DeleteModel(
            name='Accounts_Form',
        ),
    ]