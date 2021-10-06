from rest_framework import serializers
from VoilaDriver.OnlineOfflineModule.OnlineOfflineModel import BiddingRates


class BiddingRatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiddingRates
        fields = '__all__'
