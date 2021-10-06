from VoilaRider.RiderLoginModule.RiderLoginModel import RiderLogin
import http.client
import json
import random
from django.views.decorators.csrf import csrf_exempt
from VoilaDriver.Common import APIResponses
from VoilaDriver.Common.APIKey import SMSServiceApiKey
from VoilaRider.RiderLoginModule.RiderLoginSerializer import RiderLoginSerializer
from django.utils.crypto import get_random_string


# ------------- send otp to riders --------------------
def sendOtpToRider(request):
    mobile_number = request.data.get('mobile_number')
    otp = random.randint(1111, 9999)
    if mobile_number is not None:
        conn = http.client.HTTPConnection("2factor.in")
        APIKEY = SMSServiceApiKey()
        payload = ""
        headers = {'content-type': "application/x-www-form-urlencoded"}
        conn.request("GET", f"/API/V1/{APIKEY}/SMS/{mobile_number}/{otp}", payload,
                     headers)
        res = conn.getresponse().read()
        logRes = json.loads(res)
        if logRes is not None:
            sendOtpStatus = logRes["Status"]
            if sendOtpStatus == "Error":
                return APIResponses.failure_result(False, "Failed to send otp please try again")
            else:
                return APIResponses.success_result_with_array(True, "Otp send successfully", "OtpDetails", logRes)
        else:
            return APIResponses.failure_result(False, "Please try again...")
    else:
        return APIResponses.success_missing_data(False, "MobileNumber")


# ------------- verify the otp ----------------------
def verifyRiderOtp(request):
    otp = request.data.get("otp")
    session_id = request.data.get("session_id")

    if otp is not None and session_id is not None:
        conn = http.client.HTTPConnection("2factor.in")
        APIKEY = SMSServiceApiKey()
        payload = ""

        headers = {'content-type': "application/x-www-form-urlencoded"}

        conn.request("GET",
                     f"/API/V1/{APIKEY}/SMS/VERIFY/{session_id}/{otp}",
                     payload, headers)

        res = conn.getresponse()
        data = res.read()
        decodeJson = json.loads(data)
        requestStatus = decodeJson["Status"]

        if requestStatus == "Error":
            return APIResponses.failure_result(False, decodeJson["Details"])
        else:
            return isOldRider(request)
    else:
        return APIResponses.success_missing_data(False, "otp")


def isOldRider(request):
    mobile_number = request.data.get('mobile_number')

    try:
        rider = RiderLogin.objects.get(mobile_number=mobile_number)
        riderName = rider.rider_name
    except RiderLogin.DoesNotExist:
        return APIResponses.unauthorized_user()

    if RiderLogin.objects.filter(mobile_number=mobile_number).exists():
        serializer = RiderLoginSerializer(rider)
        return APIResponses.success_result_with_array(True, f"Welcome back{riderName}", "riderDetails", serializer.data)


# ------- create a new rider --------------
def createNewRider(request):
    mobile_number = request.data.get('mobile_number')
    rider_name = request.data.get('rider_name')
    fcm_token = request.data.get('fcm_token')

    if mobile_number is not None and rider_name is not None and fcm_token is not None:
        api_token = get_random_string(32)

        newRider = RiderLogin.objects.create(mobile_number=mobile_number, rider_name=rider_name, fcm_token=fcm_token,
                                             api_token=api_token, login_status=1)

        newRider.save()
        try:
            riderInfo = RiderLogin.objects.get(mobile_number=mobile_number)
        except RiderLogin.DoesNotExist:
            return APIResponses.failure_result("Failed to create a account")
        serializer = RiderLoginSerializer(riderInfo)

        return APIResponses.success_result_with_array(True, "Your account is create successfully", "riderInfo",
                                                      serializer.data)
    else:
        return APIResponses.failure_result(False, "Failed to create a account")
