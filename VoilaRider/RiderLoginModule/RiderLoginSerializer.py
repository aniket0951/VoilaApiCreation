from rest_framework import serializers
from VoilaRider.RiderLoginModule.RiderLoginModel import RiderLogin


class RiderLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiderLogin
        fields = '__all__'
