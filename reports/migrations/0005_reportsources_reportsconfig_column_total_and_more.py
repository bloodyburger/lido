# Generated by Django 4.1.7 on 2023-04-10 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0004_reportsconfig_value_col"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReportSources",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("table_name", models.TextField()),
            ],
            options={
                "verbose_name_plural": "Reports Sources",
                "db_table": "reports_source",
            },
        ),
        migrations.AddField(
            model_name="reportsconfig",
            name="column_total",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")], default=False
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="reportsconfig",
            name="field_chooser",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")], default=False
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="reportsconfig",
            name="row_total",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")], default=False
            ),
            preserve_default=False,
        ),
    ]
