# Generated by Django 2.1 on 2018-08-30 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20180828_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='accounttype',
            name='description',
            field=models.CharField(max_length=200, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='accounttype',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='accounttype',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='За 1 шт.'),
        ),
        migrations.AddField(
            model_name='accounttype',
            name='group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Group'),
        ),
    ]
