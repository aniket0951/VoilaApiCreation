from django.db import models


class RiderTripLocation(models.Model):
    rider_id = models.IntegerField()
    pickup_lat = models.CharField(max_length=210, null=True, blank=True)
    pickup_lng = models.CharField(max_length=210, null=True, blank=True)
    destination_lat = models.CharField(max_length=210, null=True, blank=True)
    destination_lng = models.CharField(max_length=210, null=True, blank=True)
    pickup_address = models.CharField(max_length=1210, null=True, blank=True)
    destination_address = models.CharField(max_length=1210, null=True, blank=True)
    distance = models.IntegerField(null=True, blank=True)
