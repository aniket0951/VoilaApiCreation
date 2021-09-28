from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from VoilaDriver.Common.APIKey import IsAuthenticated
from VoilaRider.RiderLoginModule import RiderLoginView
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

# ---------- send otp to riders -------------
@csrf_exempt
@api_view(['POST'])
def sendOtpToRider(request):
    return RiderLoginView.sendOtpToRider(request)


# ----------- verify the rider otp ------------
@csrf_exempt
@api_view(['POST'])
def verifyOtp(request):
    return RiderLoginView.verifyRiderOtp(request)


# -------------- create a new rider account --------------
@api_view(['POST'])
def createNewRiderAccount(request):
    return RiderLoginView.createNewRider(request)
