from VoilaRider.RiderLoginModule.RiderLoginModel import RiderLogin
from VoilaRider.Rider.RiderModels import RiderTripLocation, NewTripAvailable


# ------- login module -------------------------
def RiderLoginModel():
    return RiderLogin


# ---------- rider trip location module ------------
def RiderTripLocationModel():
    return RiderTripLocation


# -------- to create a new trip for driver ----------
def NewTripAvailableModel():
    return NewTripAvailable
