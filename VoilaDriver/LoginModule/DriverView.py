import http.client
import json
import random
from VoilaDriver.Common import APIResponses
from VoilaDriver.Common.APIKey import SMSServiceApiKey
from VoilaDriver.LoginModule.DriverLoginModel import DriverInfo
from VoilaDriver.LoginModule.DriverSerializer import DriverInfoSerializer


# ----------  send otp to driver --------------------
def send_otp(request):
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
        return APIResponses.failure_result(False, "Please enter mobile_number, mobile_number is required")


# ---------- verify the otp -------------
def verifyOtp(request):
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
            return isOldPartner(request)
    else:
        return APIResponses.success_missing_data(False, "otp")


def isOldPartner(request):
    phone_number = request.data.get("mobile_number")

    if DriverInfo.objects.filter(phone_number=phone_number).exists():
        try:
            drivers = DriverInfo.objects.get(phone_number=phone_number)
        except DriverInfo.DoesNotExist:
            return APIResponses.unauthorized_user()
        serializer = DriverInfoSerializer(drivers)
        return APIResponses.success_result_with_array(True, "User found", "driverInfo", serializer.data)
    else:
        return APIResponses.unauthorized_user()
