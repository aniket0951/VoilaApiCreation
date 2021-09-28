from django.urls import path
from django.urls import path
from VoilaDriver.Common.APIKey import IsAuthenticated
from VoilaRider.views import sendOtpToRider, verifyOtp, createNewRiderAccount

urlpatterns = [
    #    ----- send otp to and verify  rider --------------------
    path('sendOtpToRider', sendOtpToRider),
    path('verifyOtpToRider', verifyOtp),

    #     --------- create a rider account ----------------
    path('createRiderAccount', createNewRiderAccount)
]
