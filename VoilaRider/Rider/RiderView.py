from MySQLdb.constants.FIELD_TYPE import JSON
from VoilaRider.Rider.RiderModels import RiderTripLocation
from VoilaDriver.Common import APIResponses
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from VoilaDriver.OnlineOfflineModule.OnlineOfflineView import getAllDriverWithRadius, getAllAvailableVehicles
from VoilaRider.Rider.Serializers import RiderTripLocationSerializer
from VoilaDriver.OnlineOfflineModule.OnlineOfflineModel import BiddingRates
from VoilaDriver.OnlineOfflineModule.TripDetailsSerilizer import BiddingRatesSerializer
from VoilaDriver.Common.APIKey import IsValidParam


# ---- find the driver --------------
def findDriver(request):
    pickup_lat = request.data.get('pickup_lat')
    pickup_lng = request.data.get('pickup_lng')
    destination_lat = request.data.get('destination_lat')
    destination_lng = request.data.get('destination_lng')
    pickup_address = request.data.get('pickup_address')
    destination_address = request.data.get('destination_address')

    if pickup_lat is not None and destination_lat is not None and pickup_address is not None:
        try:
            riderLocation = RiderTripLocation.objects.get(rider_id=request.data.get('rider_id'))
        except RiderTripLocation.DoesNotExist:
            return CreateNewRideToRider(request)

        return UpdateRiderRide(request, riderLocation)

    else:
        return APIResponses.failure_result(False, "No driver available at this time")


def UpdateRiderRide(request, riderLocation):
    serializer = RiderTripLocationSerializer(riderLocation, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return getAllAvailableVehicles(request)
    else:
        return APIResponses.failure_result(False, "Failed to update ride")


def CreateNewRideToRider(request):
    serializer = RiderTripLocationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return getAllAvailableVehicles(request)
    else:
        return APIResponses.failure_result(False, "Failed to trip saved")


# ----------- get all driver of selected vehicle type --------------------
def GetDriversByVehicleType(request):
    global_vehicle_id = request.data.get('global_vehicle_id')
    rider_id = request.data.get('rider_id')

    if global_vehicle_id is not None and rider_id is not None:
        return getAllDriverWithRadius(request)
    else:
        return APIResponses.failure_result(False, "No Drivers Available at this time please try again")


# --------- get trip accepted drivers -------
def GetTripAcceptedDrivers(request):
    rider_id = request.data.get('rider_id')
    trip_id = request.data.get('trip_id')
    if IsValidParam(rider_id, request):
        if IsValidParam(trip_id, request):

            try:
                biddingRates = BiddingRates.objects.filter(rider_id=rider_id, trip_id=trip_id, driver_status=0)
            except BiddingRates.DoesNotExist:
                return APIResponses.failure_result(False, "No Drivers Available at this time please try again")

            serializer = BiddingRatesSerializer(biddingRates, many=True)
            newDrivers = serializer.data
            biddingRates.update(driver_status=1)

            if newDrivers:
                return APIResponses.success_result_with_data(True, "New drivers available", "newDrivers", newDrivers)
            else:
                return APIResponses.failure_result(False, "Please wait we are finding driver for you")


# ----- select the driver for trip --------
def SelectDriver(request):
    driver_id = request.data.get('driver_id')
    rider_id = request.data.get('rider_id')

    if IsValidParam(driver_id, request):
        if IsValidParam(rider_id, request):

            try:
                riderInfo = RiderTripLocation.objects.get(rider_id=rider_id)
            except RiderTripLocation.DoesNotExist:
                return APIResponses.failure_result(False, "Failed to select driver please try again")

            serializer = RiderTripLocationSerializer(riderInfo)
            return JsonResponse(serializer.data)

