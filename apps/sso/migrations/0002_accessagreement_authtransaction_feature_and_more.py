# Generated by Django 4.2.6 on 2023-10-25 17:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sso', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessAgreement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_signed', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('signed_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='AuthTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.PositiveSmallIntegerField(choices=[(1, 'AUTH_REQ'), (2, 'AUTH_LOGIN'), (3, 'AUTH_ALREADY_LOGIN'), (4, 'SETTING_PERMISSIONS'), (5, 'ALREADY_HAVE_PERMISSION'), (6, 'RESPONSE_READY')], default=1)),
                ('txn_token', models.CharField(max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('agreement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sso.accessagreement')),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('name', models.CharField(max_length=120)),
                ('code', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='responsibility_bearer',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='AuthTransactionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prev', models.PositiveSmallIntegerField(choices=[(1, 'AUTH_REQ'), (2, 'AUTH_LOGIN'), (3, 'AUTH_ALREADY_LOGIN'), (4, 'SETTING_PERMISSIONS'), (5, 'ALREADY_HAVE_PERMISSION'), (6, 'RESPONSE_READY')])),
                ('curr', models.PositiveSmallIntegerField(choices=[(1, 'AUTH_REQ'), (2, 'AUTH_LOGIN'), (3, 'AUTH_ALREADY_LOGIN'), (4, 'SETTING_PERMISSIONS'), (5, 'ALREADY_HAVE_PERMISSION'), (6, 'RESPONSE_READY')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('txn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sso.authtransaction')),
            ],
        ),
        migrations.AddField(
            model_name='accessagreement',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sso.client'),
        ),
        migrations.AddField(
            model_name='accessagreement',
            name='permissions',
            field=models.ManyToManyField(blank=True, to='sso.feature'),
        ),
        migrations.AddField(
            model_name='accessagreement',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='client',
            name='required_features',
            field=models.ManyToManyField(blank=True, to='sso.feature'),
        ),
        migrations.AlterUniqueTogether(
            name='accessagreement',
            unique_together={('client', 'user')},
        ),
    ]