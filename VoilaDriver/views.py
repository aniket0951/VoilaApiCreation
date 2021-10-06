from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from VoilaDriver.Common.APIKey import IsAuthenticated
from VoilaDriver.LoginModule.DriverView import send_otp, verifyOtp
from VoilaDriver.OnlineOfflineModule import OnlineOfflineView, TripDetails


# ------- fro driver  login ------------
# otp send to driver
@csrf_exempt
@api_view(["POST"])
def sendOtpDriver(request):
    return send_otp(request)


@csrf_exempt
@api_view(["POST"])
def verifyDriverOtp(request):
    return verifyOtp(request)


@api_view(["POST"])
def GoOnline(request):
    if IsAuthenticated(request):
        return OnlineOfflineView.GoOnline(request)


@api_view(["POST"])
def UpdateDriverLocation(request):
    if IsAuthenticated(request):
        return OnlineOfflineView.updateDriverLocation(request)


@api_view(["GET"])
def IsNewTripAvailable(request):
    if IsAuthenticated(request):
        return OnlineOfflineView.isNewTripAvailable(request)


# ------ accept the trip with current rate --------
@api_view(["POST"])
def AcceptTripWithCurrentRate(request):
    if IsAuthenticated(request):
        return TripDetails.acceptTripWithCurrentRate(request)


# ------ accept trip with rate card --------
@api_view(["POST"])
def AcceptTripWithRateCard(request):
    if IsAuthenticated(request):
        return TripDetails.acceptTripWithRateCard(request)


# ------------- refresh the bidding rates ----------
@api_view(["POST"])
def RefreshBiddingRates(request):
    if IsAuthenticated(request):
        return TripDetails.refreshBiddingRates(request)
