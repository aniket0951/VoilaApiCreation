import self
from django.http import HttpResponse, JsonResponse
import json
from rest_framework.parsers import JSONParser
from VoilaDriver.Common import APIResponses
from VoilaDriver.LoginModule.DriverLoginModel import DriverInfo
from VoilaDriver.OnlineOfflineModule.OnlineOfflineSerializer import OnlineOfflineSerializer
from VoilaDriver.OnlineOfflineModule.OnlineOfflineModel import OnlineOfflineModel
from VoilaDriver.Common.APIKey import MAPApiKey
import requests
from django.views.decorators.csrf import csrf_exempt
from json.decoder import JSONDecoder


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


# --------- get all available vehicle in radius --------
def CalculateDistanceOfVehicle(pickup_lat, pickup_lng, destination_lat, destination_lng):
    apikey = MAPApiKey()
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={pickup_lat}, {pickup_lng}&destination={destination_lat},  {destination_lng}&key={apikey}"
    response = requests.get(url)
    dec = json.loads(response.content.decode())
    km = (dec['routes'][0]['legs'][0]['distance']['text'])
    removeKm = km.removesuffix('km')
    print(removeKm)
    if int(float(removeKm)) <= 5:
        return APIResponses.success_result(True, removeKm)
    else:
        return APIResponses.failure_result(False, "Greater than 20")


@csrf_exempt
def getAllAvailableVehicles(request):
    pickup_lat = request.data.get('pickup_lat')
    pickup_lng = request.data.get('pickup_lng')
    destination_lat = request.data.get('destination_lat')
    destination_lng = request.data.get('destination_lng')

    return CalculateDistanceOfVehicle(pickup_lat, pickup_lng, destination_lat, destination_lng)


@csrf_exempt
def distanceBetweenDriverAndRider(pickup_lat, pickup_lng, destination_lat, destination_lng):
    apikey = MAPApiKey()
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={pickup_lat}, {pickup_lng}&destinations={destination_lat},  {destination_lng}&mode=driving&language=it-IT&key={apikey}"
    response = requests.get(url)
    dec = json.loads(response.content.decode())
    km = (dec['rows'][0]['elements'][0]['distance']['text'])
    removeKm = km.removesuffix('km')
    print(removeKm)
    if int(removeKm) <= 20:
        return APIResponses.success_result(True, removeKm)
    else:
        return APIResponses.failure_result(False, "Greater than 20")


# -------- get all drivers in the radius --------------------
def getAllDriverWithRadius(request):
    return APIResponses.failure_result(False, "Get all drivers in the radius")
