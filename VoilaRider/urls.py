from django.urls import path
from django.urls import path
from VoilaDriver.Common.APIKey import IsAuthenticated
from VoilaRider.views import sendOtpToRider, verifyOtp, createNewRiderAccount, FindVehicles, FindDriver, \
    GetTripAcceptedDrivers, SelectDriver

urlpatterns = [
    #    ----- send otp to and verify  rider --------------------
    path('sendOtpToRider', sendOtpToRider),
    path('verifyOtpToRider', verifyOtp),

    #     --------- create a rider account ----------------
    path('createRiderAccount', createNewRiderAccount),

    #     -------- to find the vehicle for the ride -----------
    path('findVehicles', FindVehicles),

    #     -------- to find the driver after selecting the vehicle -----------
    path('findDriver', FindDriver),

    #     -------- to get the driver who accepted the trip -----------
    path('getTripAcceptedDrivers', GetTripAcceptedDrivers),

    #     ------ select driver to trip -------------
    path('selectDriver', SelectDriver)
]
