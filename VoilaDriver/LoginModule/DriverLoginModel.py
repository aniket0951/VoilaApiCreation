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
