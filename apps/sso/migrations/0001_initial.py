# Generated by Django 4.2.6 on 2023-10-23 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('redirection_url', models.CharField(max_length=500)),
                ('app_key', models.CharField(max_length=200)),
                ('app_secret', models.CharField(max_length=200)),
            ],
        ),
    ]
