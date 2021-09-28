from rest_framework import serializers
from VoilaDriver.LoginModule.DriverLoginModel import DriverInfo


class DriverInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverInfo
        fields = '__all__'
