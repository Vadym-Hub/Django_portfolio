# Generated by Django 3.1.5 on 2021-01-29 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='user/avatar/', verbose_name='аватарка'),
        ),
    ]
