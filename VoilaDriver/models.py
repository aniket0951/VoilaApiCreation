from django.db import models
from VoilaDriver.LoginModule.DriverLoginModel import DriverInfo, DriverRateCard
from VoilaDriver.OnlineOfflineModule.OnlineOfflineModel import OnlineOfflineModel, BiddingRates


# Create your models here.

# -------- driver login models --------------------
def DriverInfoModel():
    return DriverInfo


# ------------ driver rate card --------------------
def DriverRateCardModel():
    return DriverRateCard


# ----------- driver online offline models --------------------
def OnlineOfflineModel():
    return OnlineOfflineModel


# ------------ trip bidding rate ---------------------
def BiddingRateModel():
    return BiddingRates
