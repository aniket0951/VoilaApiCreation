from rest_framework import exceptions
from VoilaDriver.LoginModule.DriverLoginModel import DriverInfo
from VoilaRider.RiderLoginModule.RiderLoginModel import RiderLogin
from VoilaDriver.Common import APIResponses
from django.http import JsonResponse


# ---------- provide a api key to access third party services------
def SMSServiceApiKey():
    return "06fe377d-7a20-11ea-9fa5-0200cd936042"


# --------- provide a google api key to access google cloud services ---------
def MAPApiKey():
    return "AIzaSyCvT8vf4j7X6p-d21NvnX3qVdAL5xd5wiY"


# -------- authenticate the API-request -------------
def IsAuthenticated(request):
    api_token = request.headers.get('Authorization')
    token = api_token
    if token is not None:
        if not token:  # no username passed in request headers
            raise exceptions.AuthenticationFailed("api_token missing")  # authentication did not succeed
        try:
            user = DriverInfo.objects.get(api_token=token)  # get the user
        except DriverInfo.DoesNotExist:
            raise exceptions.AuthenticationFailed("UnAuthorized request")  # raise exception if user does not exist

        return user, None
    else:
        raise exceptions.AuthenticationFailed("api_token missing")


# ------------- authenticate to rider api request -------------
def IsRiderRequestAuthenticate(request):
    api_token = request.headers.get('Authorization')
    token = api_token
    if token is not None:
        if not token:
            raise exceptions.AuthenticationFailed("api_token missing")  # authentication did not

        try:
            rider = RiderLogin.objects.get(api_token=token)
        except RiderLogin.DoesNotExist:
            raise exceptions.AuthenticationFailed("UnAuthorized request")  # raise exception if user does not

        return rider, None
    else:
        raise exceptions.AuthenticationFailed("api token is missing")


# -------- to check empty values or null point check -------------
def IsValidParam(param, request):
    if request is not None:
        if not param:
            raise exceptions.NotFound("Please provide a valid params")
        else:
            return param, True
    else:
        return exceptions.NotFound("Please provide a validate param")
