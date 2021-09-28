from django.db import models


# -------- Driver online offline status --------------------------------
class OnlineOfflineModel(models.Model):
    driver_id = models.IntegerField(null=True, blank=True)
    driver_current_latitude = models.CharField(max_length=120)
    driver_current_longitude = models.CharField(max_length=120)
    driver_current_address = models.CharField(max_length=1120, null=True, blank=True)
    on_off_status = models.IntegerField(null=True, blank=True)
    driver_vehicle_type_id = models.IntegerField(null=True, blank=True)
    global_vehicle_id = models.IntegerField(null=True, blank=True)

