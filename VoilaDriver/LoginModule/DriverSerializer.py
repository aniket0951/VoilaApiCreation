from rest_framework import serializers
from VoilaDriver.LoginModule.DriverLoginModel import DriverInfo, DriverRateCard


class DriverInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverInfo
        fields = '__all__'


# ------------ driver rate card serializer ------------
class DriverRateCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverRateCard
        fields = '__all__'
