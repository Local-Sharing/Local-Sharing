# Generated by Django 4.2 on 2024-07-25 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='accounts/static/user_icon.png/', null=True, upload_to='media/accounts/'),
        ),
    ]