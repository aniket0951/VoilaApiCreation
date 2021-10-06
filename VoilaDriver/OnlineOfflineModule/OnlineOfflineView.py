import self
from django.http import HttpResponse, JsonResponse
import json
from django.http import JsonResponse, HttpResponse
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from VoilaDriver.Common import APIResponses
from VoilaDriver.LoginModule.DriverSerializer import DriverRateCardSerializer
from VoilaDriver.LoginModule.DriverLoginModel import DriverInfo, DriverRateCard
from VoilaDriver.OnlineOfflineModule.OnlineOfflineSerializer import OnlineOfflineSerializer
from VoilaDriver.OnlineOfflineModule.OnlineOfflineModel import OnlineOfflineModel
from VoilaDriver.Common.APIKey import MAPApiKey
import requests
from django.views.decorators.csrf import csrf_exempt
from VoilaRider.Rider.RiderModels import RiderTripLocation, NewTripAvailable
from VoilaRider.Rider.Serializers import RiderTripLocationSerializer, NewTripAvailableSerializer
from django.utils.crypto import get_random_string
from django.db import connection


def GoOnline(request):
    latitude = request.data.get("driver_current_latitude")
    longitude = request.data.get('driver_current_longitude')
    on_off_status = request.data.get("on_off_status")

    if DriverInfo.objects.filter(id=request.data.get('driver_id')).exists():
        if latitude is not None and longitude is not None:
            if on_off_status is not None:
                if OnlineOfflineModel.objects.filter(driver_id=request.data.get("driver_id")).exists():
                    return updateDriverOnlineStatus(request)
                else:
                    return MoveDriverOnlineFirst(request)
            else:
                return APIResponses.success_missing_data(False, "online status")
        else:
            return APIResponses.success_missing_data(False, "latitude and longitude")
    else:
        return APIResponses.unauthorized_user()


# ------ update driver online status ------
def updateDriverOnlineStatus(request):
    try:
        onlineOffline = OnlineOfflineModel.objects.get(driver_id=request.data.get('driver_id'))
    except OnlineOfflineModel.DoesNotExist:
        return APIResponses.unauthorized_user()

    serializer = OnlineOfflineSerializer(onlineOffline, data=request.data, partial=True)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return APIResponses.success_result(True, "You are online")
    else:
        return APIResponses.failure_result(False, "You are not online")


# ------- when driver first time go online -------
def MoveDriverOnlineFirst(request):
    obj = DriverInfo.objects.get(id=request.data.get('driver_id'))
    Global_vehicle_id = obj.global_vehicle_id
    vehicle_type = obj.vehicle_type
    driver_id = request.data.get('driver_id')
    latitude = request.data.get('driver_current_latitude')
    longitude = request.data.get('driver_current_longitude')
    on_off_status = request.data.get('on_off_status')

    driver_location = OnlineOfflineModel.objects.create(driver_id=driver_id, driver_current_latitude=latitude,
                                                        driver_current_longitude=longitude,
                                                        on_off_status=on_off_status,
                                                        driver_vehicle_type_id=vehicle_type,
                                                        global_vehicle_id=Global_vehicle_id)
    driver_location.save()
    return APIResponses.success_result(True, "You are online")


# ------ update user location continuously -------
def updateDriverLocation(request):
    latitude = request.data.get('driver_current_latitude')
    longitude = request.data.get('driver_current_longitude')
    driver_id = request.data.get('driver_id')

    if latitude is not None and longitude is not None and driver_id is not None:
        try:
            onlineOffline = OnlineOfflineModel.objects.get(driver_id=driver_id)
        except OnlineOfflineModel.DoesNotExist:
            return APIResponses.unauthorized_user()

        serializer = OnlineOfflineSerializer(onlineOffline, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return APIResponses.success_result(True, "Location updated successfully")
        else:
            return APIResponses.failure_result(False, "Location not updated successfully")
    else:
        return APIResponses.success_missing_data(False, "location")


@csrf_exempt
def getAllAvailableVehicles(request):
    pickup_lat = request.data.get('pickup_lat')
    pickup_lng = request.data.get('pickup_lng')

    driverLatLng = OnlineOfflineModel.objects.all()
    serializer = OnlineOfflineSerializer(driverLatLng, many=True)

    for item in serializer.data:
        item["radiusKm"] = CalculateDistanceOfVehicle(pickup_lat, pickup_lng, item["driver_current_latitude"],
                                                      item["driver_current_longitude"], item["global_vehicle_id"])

    dict_obj = my_dictionary()
    addAuto_obj = autoDictionary()
    avaialabelList = []
    carRateList = []
    autoRateList = []
    for availableVehicles in serializer.data:
        if availableVehicles["radiusKm"] is not None:
            driver_id = availableVehicles["driver_id"]
            drivers = DriverRateCard.objects.values()
            if availableVehicles["radiusKm"] == 1:
                dict_obj.add("type", "cab")
                for item in drivers:
                    if item["driver_id"] == driver_id:
                        carRateList.append(item["min_rate"])
                        carRateList.append(item["max_rate"])

            elif availableVehicles["radiusKm"] == 2:
                addAuto_obj.addAuto("type", "auto")
                for item in drivers:
                    if item["driver_id"] == driver_id:
                        autoRateList.append(item["min_rate"])
                        autoRateList.append(item["max_rate"])

    if carRateList is not None and len(carRateList) != 0:
        carMinRate = min(carRateList)
        carMaxRate = max(carRateList)
        dict_obj.add("car_min", carMinRate)
        dict_obj.add("car_max", carMaxRate)
        dict_obj.add("global_vehicle_id", 1)
    if autoRateList is not None and len(autoRateList) != 0:
        autoMinRate = min(autoRateList)
        autoMaxRate = max(autoRateList)
        addAuto_obj.addAuto("auto_min", autoMinRate)
        addAuto_obj.addAuto("auto_max", autoMaxRate)
        addAuto_obj.addAuto("global_vehicle_id", 2)

    avaialabelList.append(dict_obj)
    avaialabelList.append(addAuto_obj)

    str_list = list(filter(None, avaialabelList))

    if avaialabelList is not None and len(avaialabelList) != 0:
        return APIResponses.success_result_with_data(True, "Available Vehicles", "availableVehicles", str_list)
    else:
        return APIResponses.failure_result(False, "No Vehicles Available at this time please try again")


class my_dictionary(dict):

    # __init__ function
    def __init__(self):
        self = dict()

    # Function to add key:value
    def add(self, key, value):
        self[key] = value


class autoDictionary(dict):
    # __init__ function
    def __init__(self):
        self = dict()

    # Function to add key:value
    def addAuto(self, key, value):
        self[key] = value


# --------- get all available vehicle in radius --------
def CalculateDistanceOfVehicle(pickup_lat, pickup_lng, destination_lat, destination_lng, global_vehicle_id):
    print(destination_lat, destination_lng, pickup_lat, pickup_lng)
    apikey = MAPApiKey()
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={pickup_lat}, {pickup_lng}&destination={destination_lat},  {destination_lng}&key={apikey}"
    response = requests.get(url)
    # print(response)
    dec = json.loads(response.content.decode())

    if dec is not None and dec != 0:
        km = (dec['routes'][0]['legs'][0]['distance']['text'])
        removeKm = km.removesuffix('km')
    else:
        print("list null")

    if int(float(removeKm)) <= 5:
        return global_vehicle_id


# -------- get all drivers in the radius --------------------
def getAllDriverWithRadius(request):
    getRiderLatLng = RiderTripLocation.objects.filter(rider_id=request.data.get('rider_id'))
    serializer = RiderTripLocationSerializer(getRiderLatLng, many=True)
    print(serializer.data[0]["pickup_lat"])
    print(serializer.data[0]["pickup_address"])

    pickup_lat = serializer.data[0]["pickup_lat"]
    pickup_lng = serializer.data[0]["pickup_lng"]

    try:
        driverLatLng = OnlineOfflineModel.objects.filter(global_vehicle_id=request.data.get("global_vehicle_id"))
    except OnlineOfflineModel.DoesNotExist:
        return APIResponses.failure_result(False, "Oops currently no drivers available, please try again")

    driverSerializer = OnlineOfflineSerializer(driverLatLng, many=True)

    trip_id = get_random_string(30)

    for item in driverSerializer.data:
        item["radiusKm"] = CalculateDistanceOfVehicle(pickup_lat, pickup_lng, item["driver_current_latitude"],
                                                      item["driver_current_longitude"], item["global_vehicle_id"])
        # --- after getting distance driver to rider
    for items in driverSerializer.data:
        if items["radiusKm"] is not None and items["radiusKm"] != 0:
            driver_id = items["driver_id"]
            result = createNewTripToDriver(driver_id, serializer, request, trip_id)
        else:
            return APIResponses.failure_result(False, "Currently no drivers available")

    if result:
        return APIResponses.success_result(True, "Please wait we are finding driver")
    else:
        return APIResponses.failure_result(False, "Currently no drivers available")


# ----- create a new trip to driver ---------
def createNewTripToDriver(driver_id, serializer, request, trip_id):
    rider_pickup_lat = serializer.data[0]["pickup_lat"]
    rider_pickup_lng = serializer.data[0]["pickup_lng"]
    rider_pickup_address = serializer.data[0]["pickup_address"]
    rider_id = request.data.get('rider_id')
    trip_min_rate = request.data.get('trip_min_rate')
    trip_max_rate = request.data.get('trip_max_rate')
    trip_id = trip_id

    createNewTrip = NewTripAvailable.objects.create(rider_id=rider_id, driver_id=driver_id,
                                                    rider_pickup_lat=rider_pickup_lat,
                                                    rider_pickup_lng=rider_pickup_lng,
                                                    rider_pickup_address=rider_pickup_address,
                                                    trip_id=trip_id, trip_min_rate=trip_min_rate,
                                                    trip_max_rate=trip_max_rate,
                                                    trip_status=1)
    if createNewTrip:
        return True
    else:
        return False


# ------- check new trip is available or not ---------
def isNewTripAvailable(request):
    driver_id = request.data.get('driver_id')
    if driver_id is not None:
        try:
            newTripAvailable = NewTripAvailable.objects.get(driver_id=driver_id)
            newTripAvailable.trip_status = 0
            newTripAvailable.save()
        except NewTripAvailable.DoesNotExist:
            return APIResponses.failure_result(False, "New trip not available")

        serializer = NewTripAvailableSerializer(newTripAvailable)

        return APIResponses.success_result_with_array(True, "Trip available", "tripData", serializer.data)
    else:
        return APIResponses.success_missing_data(False, "driver id")

