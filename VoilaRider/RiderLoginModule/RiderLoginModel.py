from django.db import models


class RiderLogin(models.Model):
    mobile_number = models.CharField(max_length=120, null=True, blank=True)
    rider_name = models.CharField(max_length=120, null=True, blank=True)
    rider_rating = models.CharField(max_length=120, null=True, blank=True)
    api_token = models.CharField(max_length=320, null=True, blank=True)
    login_status = models.IntegerField(null=True, blank=True)
    fcm_token = models.CharField(max_length=220, null=True, blank=True)
