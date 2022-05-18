from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from datetime import date



# Create your models here.

class User(models.Model):
    user_username = models.TextField()
    user_password = models.TextField()
    user_role = models.TextField()
    user_company = models.TextField()


class Xbarr(models.Model):
    xbarr_survey_id = models.IntegerField()
    xbarr_nkaryawan = models.IntegerField()
    xbarr_npart = models.IntegerField()
    xbarr_ntrial = models.IntegerField()
    xbarr_stdev = models.FloatField(null=True)
    xbarr_stdevmax = models.FloatField(null=True)
    xbarr_stdevmin = models.FloatField(null=True)
    xbarr_karyawan = models.JSONField(null=True)
    xbarr_all = models.JSONField(null=True)
    xbarr_resume = models.JSONField(null=True)
    xbarr_psvc = models.TextField(null=True)
    xbarr_rva = models.TextField(null=True)
    xbarr_xva = models.TextField(null=True)
    xbarr_dbs = models.TextField(null=True)
    xbarr_dba = models.TextField(null=True)
    xbarr_aabp = models.TextField(null=True)
    xbarr_recommendation = models.JSONField(null=True)


class Cross(models.Model):
    cross_survey_id = models.IntegerField()
    cross_nkaryawan = models.IntegerField()
    cross_npart = models.IntegerField()
    cross_ntrial = models.IntegerField()
    cross_stdev = models.FloatField()
    cross_stdevmax = models.FloatField()
    cross_stdevmin = models.FloatField()
    cross_karyawan = models.JSONField(null=True)
    cross_all = models.JSONField(null=True)
    cross_resume = models.JSONField(null=True)
    cross_psvc = models.TextField(null=True)
    cross_rva = models.TextField(null=True)
    cross_xva = models.TextField(null=True)
    cross_dbs = models.TextField(null=True)
    cross_dba = models.TextField(null=True)
    cross_aabp = models.TextField(null=True)
    cross_recommendation = models.JSONField(null=True)

class Nested(models.Model):
    nested_survey_id = models.IntegerField()
    nested_nkaryawan = models.IntegerField()
    nested_npart = models.IntegerField()
    nested_ntrial = models.IntegerField()
    nested_stdev = models.FloatField()
    nested_stdevmax = models.FloatField()
    nested_stdevmin = models.FloatField()
    nested_karyawan = models.JSONField(null=True)
    nested_all = models.JSONField(null=True)
    nested_resume = models.JSONField(null=True)
    nested_psvc = models.TextField(null=True)
    nested_rva = models.TextField(null=True)
    nested_xva = models.TextField(null=True)
    nested_dbs = models.TextField(null=True)
    nested_dba = models.TextField(null=True)
    nested_aabp = models.TextField(null=True)
    nested_recommendation = models.JSONField(null=True)

class Linearity(models.Model):
    linearity_survey_id = models.IntegerField()
    linearity_npart = models.IntegerField()
    linearity_nmeasurement = models.IntegerField()
    linearity_confidence = models.FloatField()
    linearity_working_max = models.FloatField()
    linearity_working_min = models.FloatField()
    linearity_ref = models.TextField()
    linearity_master = models.JSONField(null=True)
    linearity_average = models.JSONField(null=True)
    linearity_all = models.JSONField(null=True)
    linearity_biasref = models.TextField(null=True)
    linearity_recommendation = models.TextField(null=True)
    linearity_ave_sn = models.TextField(null=True)
    linearity_ave_res = models.TextField(null=True)
    linearity_ave_measured = models.TextField(null=True)
    linearity_reviewed = models.TextField()
    linearity_measured = models.TextField()

class Vxbarr(models.Model):
    vxbarr_survey_id = models.IntegerField()
    vxbarr_lsl = models.IntegerField()
    vxbarr_usl = models.IntegerField()
    vxbarr_subgroup = models.IntegerField()
    vxbarr_unit = models.TextField()
    vxbarr_all = models.JSONField(null=True)
    vxbarr_measured = models.TextField()
    vxbarr_reviewed = models.TextField()

class Survey(models.Model):
    survey_user_id = models.IntegerField()
    survey_date_project = models.DateField()
    survey_data = models.TextField()
    survey_cust_name = models.TextField()
    survey_part_name = models.TextField()
    survey_part_number = models.TextField()
    survey_character = models.TextField()
    survey_name = models.TextField()
    survey_category = models.TextField()
    survey_sn = models.TextField()
    survey_process_name = models.TextField()
    survey_resolution = models.TextField()
    survey_symbol = models.TextField()
    survey_unit = models.TextField()
    survey_ref = models.TextField()
    survey_next_cal = models.DateField()
    survey_range_max = models.TextField() #text atau float?
    survey_range_min = models.TextField()
    survey_fmea = models.TextField()
    survey_control_plan = models.TextField()
    survey_plan = models.DateField(null=True)
    survey_actual = models.DateField(null=True)
    survey_reason = models.TextField(null=True)
    survey_att_prod_unit = models.TextField(null=True)
    survey_att_qty = models.TextField(null=True)
    survey_att_cat = models.TextField(null=True)
    survey_var_bias_working = models.TextField(null=True)
    survey_var_bias_over = models.TextField(null=True)
    survey_var_variation = models.TextField(null=True)
    survey_var_review = models.TextField(null=True)
    survey_var_part_sample = models.TextField(null=True)
    survey_var_homogen = models.TextField(null=True)
    survey_var_subgroup = models.TextField(null=True)
    survey_var_ave = models.TextField(null=True)
    survey_study = models.JSONField(null=True)
    @property
    def is_past_due(self):
        return date.today() > self.survey_next_cal