# Generated by Django 3.2.14 on 2022-07-07 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pantherapp', '0005_alter_customuser_id_telegram'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='id_telegram',
            field=models.IntegerField(verbose_name='ID пользователя в Telegram'),
        ),
    ]
