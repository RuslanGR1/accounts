# Generated by Django 2.1 on 2018-08-24 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(default=None, max_length=254),
        ),
    ]
