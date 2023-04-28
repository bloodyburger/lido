# Generated by Django 4.1.7 on 2023-04-13 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0012_reportsconfig_fold_primary"),
    ]

    operations = [
        migrations.AddField(
            model_name="reportsconfig",
            name="expand_account",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")], default=False
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="reportsconfig",
            name="expand_category",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")], default=False
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="reportsconfig",
            name="expand_primary",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")], default=False
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="reportsconfig",
            name="expand_secondary",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")], default=False
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="reportsconfig",
            name="expand_subcategory",
            field=models.BooleanField(
                choices=[(True, "Yes"), (False, "No")], default=False
            ),
            preserve_default=False,
        ),
    ]
