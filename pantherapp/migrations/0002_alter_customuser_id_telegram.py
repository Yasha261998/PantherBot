# Generated by Django 3.2.14 on 2022-07-07 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pantherapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='id_telegram',
            field=models.IntegerField(unique=True, verbose_name='ID пользователя в Telegram'),
        ),
    ]
