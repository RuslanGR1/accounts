# Generated by Django 2.1 on 2018-08-26 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20180826_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='download_code',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
    ]
