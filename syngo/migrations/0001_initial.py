# Generated by Django 3.2.15 on 2022-08-26 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Captcha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secret', models.CharField(max_length=5)),
                ('image', models.ImageField(blank=True, upload_to='')),
            ],
        ),
    ]
