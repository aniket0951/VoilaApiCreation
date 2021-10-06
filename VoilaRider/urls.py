from django.urls import path
from django.urls import path
from VoilaDriver.Common.APIKey import IsAuthenticated
from VoilaRider.views import sendOtpToRider, verifyOtp, createNewRiderAccount, FindVehicles, FindDriver

urlpatterns = [
    #    ----- send otp to and verify  rider --------------------
    path('sendOtpToRider', sendOtpToRider),
    path('verifyOtpToRider', verifyOtp),

    #     --------- create a rider account ----------------
    path('createRiderAccount', createNewRiderAccount),

    #     -------- to find the vehicle for the ride -----------
    path('findVehicles', FindVehicles),

    #     -------- to find the driver after selecting the vehicle -----------
    path('findDriver', FindDriver)

]
