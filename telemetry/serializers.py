from rest_framework import serializers
from .models import VehicleTelemetry

class VehicleTelemetrySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleTelemetry
        fields = '__all__'