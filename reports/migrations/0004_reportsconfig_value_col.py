# Generated by Django 4.1.7 on 2023-04-10 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0003_reportsconfig"),
    ]

    operations = [
        migrations.AddField(
            model_name="reportsconfig",
            name="value_col",
            field=models.TextField(default="VALUE_BASE_TOKEN"),
            preserve_default=False,
        ),
    ]
