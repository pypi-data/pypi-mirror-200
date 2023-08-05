# Generated by Django 4.1.4 on 2023-01-12 11:20

import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("netbox_celery", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="celeryresult",
            old_name="data",
            new_name="kwargs",
        ),
        migrations.AddField(
            model_name="celeryresult",
            name="args",
            field=models.JSONField(
                blank=True,
                encoder=django.core.serializers.json.DjangoJSONEncoder,
                null=True,
            ),
        ),
    ]
