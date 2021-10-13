from VoilaDriver.Common import APIResponses
from VoilaDriver.Common.APIKey import IsValidParam
from VoilaDriver.LoginModule.DriverLoginModel import DriverRateCard
from VoilaDriver.OnlineOfflineModule.OnlineOfflineModel import BiddingRates
from VoilaDriver.OnlineOfflineModule.TripDetailsSerilizer import BiddingRatesSerializer
from VoilaRider.Rider.RiderModels import NewTripAvailable
from VoilaDriver.OnlineOfflineModule.OnlineOfflineModel import OnlineOfflineModel
from VoilaDriver.OnlineOfflineModule.OnlineOfflineSerializer import OnlineOfflineSerializer
from django.http import HttpResponse, JsonResponse


# ----------- accept trip with current rate -------------
def acceptTripWithCurrentRate(request):
    driver_id = request.data.get('driver_id')
    trip_id = request.data.get('trip_id')
    if IsValidParam(driver_id, request):
        if IsValidParam(trip_id, request):

            try:
                tripInfo = NewTripAvailable.objects.get(driver_id=driver_id, trip_id=trip_id)
                rider_id = tripInfo.rider_id
                trip_id = tripInfo.trip_id
                live_bidding_rate = tripInfo.trip_min_rate
            except NewTripAvailable.DoesNotExist:
                return APIResponses.failure_result(False, "Failed to accept the trip please try again")

            createBiddingRate = BiddingRates.objects.create(driver_id=driver_id, rider_id=rider_id, trip_id=trip_id,
                                                            live_bidding_rate=live_bidding_rate,
                                                            driver_status=0)

            # --- update busy status ---
            try:
                ofm = OnlineOfflineModel.objects.filter(driver_id=driver_id)
            except OnlineOfflineModel.DoesNotExist:
                return APIResponses.failure_result(False, "Failed to accept the trip please try again")
            ofm.update(is_busy=1)
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
            # print(newTripAvailable.rider_id)
        except NewTripAvailable.DoesNotExist:
            return APIResponses.failure_result(False,
                                               "Failed to accept the trip please try again or check your internet connection")

            #     -- create a new bidding with user ratecards min rate and max rate --
        biddingRates = BiddingRates.objects.create(rider_id=rider_id, driver_id=driver_id, trip_id=trip_id,
                                                   live_bidding_rate=min_rate, driver_status=0)

        # --- update busy status ---
        try:
            ofm = OnlineOfflineModel.objects.filter(driver_id=driver_id)
        except OnlineOfflineModel.DoesNotExist:
            return APIResponses.failure_result(False, "Failed to accept the trip please try again")
        ofm.update(is_busy=1)

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


# ------ apply min rate to current trip if bidding rate is max
def applyMinRate(request):
    driver_id = request.data.get('driver_id')
    trip_id = request.data.get('trip_id')
    if IsValidParam(driver_id, request):
        if IsValidParam(trip_id, request):

            try:
                biddingRates = BiddingRates.objects.get(driver_id=driver_id, trip_id=trip_id)
                allBiddingRates = BiddingRates.objects.filter(trip_id=trip_id)
            except BiddingRates.DoesNotExist:
                return APIResponses.failure_result(False, "Failed to apply min rate please try again...")

            # --- get min and max rates from driver rate card ----------
            try:
                driverRateCard = DriverRateCard.objects.get(driver_id=driver_id)
                rate_card_min = driverRateCard.min_rate
            except DriverRateCard.DoesNotExist:
                return APIResponses.unauthorized_user()

            serializer = BiddingRatesSerializer(allBiddingRates, many=True)

            # ---- get current bidding min rate ------
            currentMinRate = []
            for items in serializer.data:
                currentMinRate.append(items["live_bidding_rate"])

            # --- compare a current bidding min and driver min rate ---
            if int(rate_card_min) < int(min(currentMinRate)):
                data = {"live_bidding_rate": rate_card_min}
                updateSerializer = BiddingRatesSerializer(biddingRates, data=data, partial=True)
                if updateSerializer.is_valid():
                    updateSerializer.save()
                    return APIResponses.success_result_with_array(True, "Bidding rate apply successfully", "applyRate",
                                                                  updateSerializer.data)
                else:
                    return APIResponses.failure_result(False, "Internal sever error please try again")
            else:
                return APIResponses.failure_result(False, "Oops your rate card is not a min rate for this trip")


# ---- reject the trip ----
def canceledTrip(request):
    driver_id = request.data.get('driver_id')
    if IsValidParam(driver_id, request):
        try:
            newTripAvailable = NewTripAvailable.objects.get(driver_id=driver_id)
        except NewTripAvailable.DoesNotExist:
            return APIResponses.failure_result(False, "Failed to canceled the trip please try again")

        newTripAvailable.delete()
        return APIResponses.success_result(True, "Successfully canceled the trip")
