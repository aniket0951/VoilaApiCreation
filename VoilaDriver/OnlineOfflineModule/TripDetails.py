from rest_framework.parsers import JSONParser
from VoilaDriver.Common import APIResponses
from VoilaDriver.OnlineOfflineModule.OnlineOfflineModel import BiddingRates
from VoilaRider.Rider.RiderModels import NewTripAvailable
from VoilaDriver.LoginModule.DriverLoginModel import DriverRateCard
from django.http import HttpResponse, JsonResponse
from VoilaDriver.Common.APIKey import IsValidParam
from VoilaDriver.OnlineOfflineModule.TripDetailsSerilizer import BiddingRatesSerializer


# ----------- accept trip with current rate -------------
def acceptTripWithCurrentRate(request):
    driver_id = request.data.get('driver_id')
    if IsValidParam(driver_id, request):
        try:
            tripInfo = NewTripAvailable.objects.get(driver_id=driver_id)
            rider_id = tripInfo.rider_id
            trip_id = tripInfo.trip_id
            live_bidding_rate = tripInfo.trip_min_rate

        except NewTripAvailable.DoesNotExist:
            return APIResponses.failure_result(False, "Failed to accept the trip please try again")

        createBiddingRate = BiddingRates.objects.create(driver_id=driver_id, rider_id=rider_id, trip_id=trip_id,
                                                        live_bidding_rate=live_bidding_rate,
                                                        driver_status=0)

        if createBiddingRate:
            return APIResponses.success_result(True,
                                               "Trip accepted successfully. For bidding please refresh the bidding rates")
        else:
            return APIResponses.failure_result(False,
                                               " Failed to accept the trip please try again..check your internet connection")


# -------- accept trip with rate card -------------
def acceptTripWithRateCard(request):
    driver_id = request.data.get('driver_id')
    if IsValidParam(driver_id, request):
        try:
            driverRateCard = DriverRateCard.objects.get(driver_id=driver_id)
            min_rate = driverRateCard.min_rate
        except DriverRateCard.DoesNotExist:
            return APIResponses.failure_result(False,
                                               "Failed to accept the trip please try again or check your internet connection")

        try:
            newTripAvailable = NewTripAvailable.objects.get(driver_id=driver_id)
            rider_id = newTripAvailable.rider_id
            trip_id = newTripAvailable.trip_id
            print(newTripAvailable.rider_id)
        except NewTripAvailable.DoesNotExist:
            return APIResponses.failure_result(False,
                                               "Failed to accept the trip please try again or check your internet connection")

            #     -- create a new bidding with user ratecards min rate and max rate --
        biddingRates = BiddingRates.objects.create(rider_id=rider_id, driver_id=driver_id, trip_id=trip_id,
                                                   live_bidding_rate=min_rate, driver_status=0)

        if biddingRates:
            return APIResponses.success_result(True, "Trip is accepted with rate card")
        else:
            return APIResponses.failure_result(False, "Failed to accept the trip please try again...")


# ------ refresh the bidding rates --------
def refreshBiddingRates(request):
    trip_id = request.data.get('trip_id')
    if IsValidParam(trip_id, request):

        biddingRates = BiddingRates.objects.filter(trip_id=trip_id)

        if biddingRates:
            serializer = BiddingRatesSerializer(biddingRates, many=True)

            allMinRate = []
            for item in serializer.data:
                allMinRate.append(item["live_bidding_rate"])

            currentMinRate = ({"currentBiddingRate": min(allMinRate)})
            return APIResponses.success_result_with_array(True, "New Bidding live rate available", "currentBiddingRate",
                                                          currentMinRate)
        else:
            return APIResponses.failure_result(False, "Failed to refresh the bidding rates please check")
