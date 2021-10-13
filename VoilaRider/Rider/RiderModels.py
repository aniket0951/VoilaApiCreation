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


# ---------- create a new trip for drivers --------------------
class NewTripAvailable(models.Model):
    rider_id = models.IntegerField()
    driver_id = models.IntegerField()
    rider_pickup_lat = models.CharField(max_length=1220, null=True, blank=True)
    rider_pickup_lng = models.CharField(max_length=1220, null=True, blank=True)
    rider_pickup_address = models.CharField(max_length=1210, null=True, blank=True)
    trip_id = models.CharField(max_length=310, null=True, blank=True)
    trip_min_rate = models.CharField(max_length=310, null=True, blank=True)
    trip_max_rate = models.CharField(max_length=310, null=True, blank=True)
    trip_status = models.CharField(max_length=310, null=True, blank=True)


# ---------- pre-conform trips --------------------------------
class PreConformTrips(models.Model):
    rider_id = models.IntegerField()
    driver_id = models.IntegerField()
    rider_pickup_lat = models.CharField(max_length=1220, null=True, blank=True)
    rider_pickup_lng = models.CharField(max_length=1220, null=True, blank=True)
    rider_pickup_address = models.CharField(max_length=1210, null=True, blank=True)
    rider_destination_address = models.CharField(max_length=1210, null=True, blank=True)
    driver_current_latitude = models.CharField(max_length=1210, null=True, blank=True)
    driver_current_longitude = models.CharField(max_length=1210, null=True, blank=True)
    trip_id = models.IntegerField(null=True, blank=True)
    trip_rate = models.IntegerField(null=True, blank=True)
    trip_status = models.IntegerField(null=True, blank=True)
    otp = models.IntegerField(null=True, blank=True)
