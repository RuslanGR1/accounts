# Generated by Django 2.1 on 2018-08-28 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20180828_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounttypegroup',
            name='types',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.AccountType'),
        ),
    ]
