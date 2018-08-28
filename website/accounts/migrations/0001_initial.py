# Generated by Django 2.1 on 2018-08-24 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='name of type')),
                ('description', models.CharField(max_length=200, verbose_name='description')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
            ],
            options={
                'verbose_name': 'Account type',
                'verbose_name_plural': 'Account types',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('pay_comment', models.CharField(max_length=20, verbose_name='Qiwi comment')),
                ('paid', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254)),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.AccountType')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.AccountType'),
        ),
    ]
