from django.urls import path
from django.urls import path
from VoilaDriver.Common.APIKey import IsAuthenticated
from VoilaDriver.views import sendOtpDriver, verifyDriverOtp, GoOnline, UpdateDriverLocation

urlpatterns = [
    path('send_otp', sendOtpDriver),
    path('verify_otp', verifyDriverOtp),
    #     ----- to go-online or offline -----
    path('move_online', GoOnline),

    #     --------- update driver location ----------
    path('update_location', UpdateDriverLocation)
]
