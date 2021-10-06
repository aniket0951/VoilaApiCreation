from django.urls import path
from django.urls import path
from VoilaDriver.Common.APIKey import IsAuthenticated
from VoilaDriver.views import sendOtpDriver, verifyDriverOtp, GoOnline, UpdateDriverLocation, IsNewTripAvailable, \
    AcceptTripWithCurrentRate, AcceptTripWithRateCard, RefreshBiddingRates

urlpatterns = [
    path('send_otp', sendOtpDriver),
    path('verify_otp', verifyDriverOtp),
    #     ----- to go-online or offline -----
    path('move_online', GoOnline),

    #     --------- update driver location ----------
    path('update_location', UpdateDriverLocation),

    #     -------- check is any new trip available for driver ---------------
    path('isNewTripAvailable', IsNewTripAvailable),

    #     --------- accept the trip with current rate --------
    path("AcceptTripWithCurrentRate", AcceptTripWithCurrentRate),

    #     ------- accept trip with rate card ----------
    path('acceptTripWithRateCard', AcceptTripWithRateCard),

    #     -------- refresh the bidding rates -----
    path('refreshBiddingRates', RefreshBiddingRates)
]
