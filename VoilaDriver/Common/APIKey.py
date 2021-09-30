from rest_framework import exceptions
from VoilaDriver.LoginModule.DriverLoginModel import DriverInfo
from VoilaRider.RiderLoginModule.RiderLoginModel import RiderLogin


# ---------- provide a api key to access third party services------
def SMSServiceApiKey():
    return "06fe377d-7a20-11ea-9fa5-0200cd936042"


# --------- provide a google api key to access google cloud services ---------
def MAPApiKey():
    return "AIzaSyCvT8vf4j7X6p-d21NvnX3qVdAL5xd5wiY"


# -------- authenticate the API-request -------------
def IsAuthenticated(request):
    token = request.data.get('api_token')

    if not token:  # no username passed in request headers
        raise exceptions.AuthenticationFailed("api_token missing")  # authentication did not succeed
    try:
        user = DriverInfo.objects.get(api_token=token)  # get the user
    except DriverInfo.DoesNotExist:
        raise exceptions.AuthenticationFailed("UnAuthorized request")  # raise exception if user does not exist

    return user, None


# ------------- authenticate to rider api request -------------
def IsRiderRequestAuthenticate(request):
    token = request.META['HTTP_AUTHORIZATION']

    if not token:
        raise exceptions.AuthenticationFailed("api_token missing")  # authentication did not

    try:
        rider = RiderLogin.objects.get(api_token=token)
    except RiderLogin.DoesNotExist:
        raise exceptions.AuthenticationFailed("UnAuthorized request")  # raise exception if user does not

    return rider, None
