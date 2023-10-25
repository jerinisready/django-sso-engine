# Generated by Django 4.2.6 on 2023-10-25 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sso', '0002_accessagreement_authtransaction_feature_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='login_description',
            field=models.TextField(blank=True, help_text='Anything to display at login page', null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='client-logo/'),
        ),
        migrations.AddField(
            model_name='client',
            name='permission_description',
            field=models.TextField(blank=True, help_text='Anything to display at permission page', null=True),
        ),
    ]