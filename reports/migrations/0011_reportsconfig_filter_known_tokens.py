# Generated by Django 4.1.7 on 2023-04-12 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0010_reportsconfig_show_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="reportsconfig",
            name="filter_known_tokens",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")], default=False
            ),
            preserve_default=False,
        ),
    ]
