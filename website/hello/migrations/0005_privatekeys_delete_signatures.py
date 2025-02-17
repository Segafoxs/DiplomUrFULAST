# Generated by Django 5.1.4 on 2025-01-04 10:49

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0004_historypermit_signature_executor'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateKeys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('private_key', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(50, 'the field must contain at least 50 characters')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expired_at', models.DateTimeField()),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Signatures',
        ),
    ]
