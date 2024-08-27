# Generated by Django 4.2 on 2024-08-26 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0002_map_latitude_map_longitude_map_url_alter_map_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherCategoryMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weather', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
            ],
        ),
    ]
