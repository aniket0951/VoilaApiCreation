from django.db import models
from VoilaDriver.LoginModule.DriverLoginModel import DriverInfo
from VoilaDriver.OnlineOfflineModule.OnlineOfflineModel import OnlineOfflineModel


# Create your models here.

# -------- driver login models --------------------
def DriverInfoModel():
    return DriverInfo


# ----------- driver online offline models --------------------
def OnlineOfflineModel():
    return OnlineOfflineModel
