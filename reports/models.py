# import the standard Django Model
# from built-in library
from django.db import models

BOOL_CHOICES = [
    ("YES", "YES"),
    ("NO", "NO")
]

# declare a new model with a name "GeeksModel"
class Reports(models.Model):
		# fields of the model
	report_name = models.CharField(max_length = 255)
	description = models.TextField(blank=True,default=None)
	subheading = models.TextField(blank=True,default=None)
		# renames the instances of the model
		# with their title name
	def __str__(self):
		return self.report_name
	
	class Meta:
		db_table = "reports"
		verbose_name_plural = "Reports"

class ReportsConfig(models.Model):
		# fields of the model
	report = models.ForeignKey(Reports, on_delete=models.CASCADE)
	primary_filters = models.TextField(blank=True,default=None,null=True)
	secondary_filters = models.TextField(blank=True,default=None,null=True)
	account_filters = models.TextField(blank=True,default=None,null=True)
	category_filters = models.TextField(blank=True,default=None,null=True)
	subcategory_filters = models.TextField(blank=True,default=None,null=True)
	show_primary = models.CharField(max_length=3,choices=BOOL_CHOICES, blank=True,default=None)
	show_secondary = models.CharField(max_length=3,choices=BOOL_CHOICES, blank=True,default=None)
	show_account = models.CharField(max_length=3,choices=BOOL_CHOICES, blank=True,default=None)
	show_category = models.CharField(max_length=3,choices=BOOL_CHOICES, blank=True,default=None)
	show_subcategory = models.CharField(max_length=3,choices=BOOL_CHOICES, blank=True,default=None)
	base_token = models.TextField(blank=True,default=None)
		# renames the instances of the model
		# with their title name
	def __str__(self):
		return self.report.report_name
	
	class Meta:
		db_table = "reports_config"
		verbose_name_plural = "Report Config"