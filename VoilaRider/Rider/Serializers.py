from rest_framework import serializers
from VoilaRider.Rider.RiderModels import RiderTripLocation, NewTripAvailable


class RiderTripLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiderTripLocation
        fields = '__all__'


# ---------- create a new trip fro driver serializer -----------------------
class NewTripAvailableSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewTripAvailable
        fields = '__all__'

