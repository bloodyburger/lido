# import the standard Django Model
# from built-in library
from django.db import models

YN_CHOICES = [("YES", "Yes"), ("NO", "No")]
BOOL_CHOICES = [(True, "Yes"), (False, "No")]
CURR_CHOICES = [("currency", "Yes"), ("fixedPoint", "No")]

# declare a new model with a name "GeeksModel"
class Reports(models.Model):
    # fields of the model
    report_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default=None)
    subheading = models.TextField(blank=True, default=None)
    # renames the instances of the model
    # with their title name
    def __str__(self):
        return self.report_name + " / " + self.subheading

    class Meta:
        db_table = "reports"
        verbose_name_plural = "Reports"


class ReportSources(models.Model):
    # fields of the model
    table_name = models.TextField()
    # renames the instances of the model
    # with their title name
    def __str__(self):
        return self.table_name

    class Meta:
        db_table = "reports_source"
        verbose_name_plural = "Reports Sources"


class ReportsConfig(models.Model):
    # fields of the model
    report = models.ForeignKey(Reports, on_delete=models.CASCADE)
    primary_filters = models.TextField(blank=True, default=None, null=True)
    secondary_filters = models.TextField(blank=True, default=None, null=True)
    account_filters = models.TextField(blank=True, default=None, null=True)
    category_filters = models.TextField(blank=True, default=None, null=True)
    subcategory_filters = models.TextField(blank=True, default=None, null=True)
    show_primary = models.CharField(
        max_length=3, choices=YN_CHOICES, blank=True, default=None
    )
    show_secondary = models.CharField(
        max_length=3, choices=YN_CHOICES, blank=True, default=None
    )
    show_account = models.CharField(
        max_length=3, choices=YN_CHOICES, blank=True, default=None
    )
    show_category = models.CharField(
        max_length=3, choices=YN_CHOICES, blank=True, default=None
    )
    show_subcategory = models.CharField(
        max_length=3, choices=YN_CHOICES, blank=True, default=None
    )
    show_token = models.CharField(max_length=3, choices=YN_CHOICES)
    base_token = models.TextField(blank=True, default=None)
    value_col = models.TextField()
    field_chooser = models.BooleanField(choices=BOOL_CHOICES)
    row_total = models.BooleanField(choices=BOOL_CHOICES)
    column_total = models.BooleanField(choices=BOOL_CHOICES)
    source_table = models.ForeignKey(ReportSources, on_delete=models.CASCADE)
    show_as_dollar = models.CharField(max_length=20, choices=CURR_CHOICES)
    value_as_cumulative = models.BooleanField(choices=BOOL_CHOICES)
    filter_known_tokens = models.BooleanField(choices=BOOL_CHOICES)
    fold_primary = models.TextField(blank=True, default=None, null=True)
    expand_primary = models.BooleanField(choices=BOOL_CHOICES)
    expand_secondary = models.BooleanField(choices=BOOL_CHOICES)
    expand_account = models.BooleanField(choices=BOOL_CHOICES)
    expand_category = models.BooleanField(choices=BOOL_CHOICES)
    expand_subcategory = models.BooleanField(choices=BOOL_CHOICES)
    drilldown_cols = models.TextField()
    # renames the instances of the model
    # with their title name
    def __str__(self):
        return self.report.report_name + " / " + self.report.subheading

    class Meta:
        db_table = "reports_config"
        verbose_name_plural = "Report Config"


class Uploads(models.Model):
    # fields of the model
    document = models.FileField(upload_to="documents/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # renames the instances of the model
    # with their title name
    def __str__(self):
        return self.created_at

    class Meta:
        verbose_name_plural = "File Uploads"
