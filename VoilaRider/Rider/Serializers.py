from rest_framework import serializers
from VoilaRider.Rider.RiderModels import RiderTripLocation


class RiderTripLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiderTripLocation
        fields = '__all__'
