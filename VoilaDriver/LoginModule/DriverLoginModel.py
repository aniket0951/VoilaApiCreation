from django.db import models


# ----------  Driver login or driver info module --------------------
class DriverInfo(models.Model):
    phone_number = models.CharField(max_length=120)
    driver_name = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    current_address = models.CharField(max_length=120)
    vehicle_reg_number = models.CharField(max_length=120)
    rc = models.CharField(max_length=120)
    vehicle_color = models.CharField(max_length=15)
    vehicle_model = models.CharField(max_length=120)
    make_year = models.IntegerField()
    vehicle_type = models.CharField(max_length=120)
    api_token = models.CharField(max_length=120)
    firebase_token = models.CharField(max_length=120)
    driver_ratings = models.CharField(max_length=120)
    global_vehicle_id = models.CharField(max_length=120)


# ------------------ driver rate card -------------------------------
class DriverRateCard(models.Model):
    driver_id = models.CharField(max_length=1200, null=True, blank=True)
    min_rate = models.CharField(max_length=1200, null=True, blank=True)
    max_rate = models.CharField(max_length=1200, null=True, blank=True)
    system_rate = models.CharField(max_length=1200, null=True, blank=True)
    canceled_trips = models.CharField(max_length=1200, null=True, blank=True)
    canceled_trip_limit = models.CharField(max_length=1200, null=True, blank=True)
