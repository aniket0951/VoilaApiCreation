from rest_framework import serializers
from VoilaDriver.OnlineOfflineModule.OnlineOfflineModel import OnlineOfflineModel


class OnlineOfflineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineOfflineModel
        fields = '__all__'
