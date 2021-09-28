from rest_framework import exceptions
from VoilaDriver.LoginModule.DriverLoginModel import DriverInfo


# ---------- provide a api key to access third party services------
def SMSServiceApiKey():
    return "06fe377d-7a20-11ea-9fa5-0200cd936042"


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

