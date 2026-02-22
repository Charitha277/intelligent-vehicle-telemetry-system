from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import VehicleTelemetry
from .serializers import VehicleTelemetrySerializer
from sklearn.ensemble import IsolationForest
import numpy as np


@api_view(['GET', 'POST'])
def telemetry_list(request):

    if request.method == 'GET':
        telemetry = VehicleTelemetry.objects.all().order_by('timestamp')
        serializer = VehicleTelemetrySerializer(telemetry, many=True)
        return Response(serializer.data)

    if request.method == 'POST':

        speed = float(request.data.get("speed"))
        fuel = float(request.data.get("fuel_level"))
        temperature = float(request.data.get("temperature"))
        latitude = float(request.data.get("latitude"))
        longitude = float(request.data.get("longitude"))

        # ---------------------------
        # Rule-Based Detection
        # ---------------------------
        rule_anomaly = False
        reasons = []

        if speed > 110:
            rule_anomaly = True
            reasons.append("Overspeed")

        if temperature > 85:
            rule_anomaly = True
            reasons.append("Overheat")

        if fuel < 15:
            rule_anomaly = True
            reasons.append("Low Fuel")

        # ---------------------------
        # ML Detection
        # ---------------------------
        existing = VehicleTelemetry.objects.all().values_list(
            'speed', 'fuel_level', 'temperature'
        )

        ml_anomaly = False

        if len(existing) > 20:
            X = np.array(list(existing))
            model = IsolationForest(contamination=0.1)
            model.fit(X)

            new_point = np.array([[speed, fuel, temperature]])
            prediction = model.predict(new_point)

            if prediction[0] == -1:
                ml_anomaly = True
                reasons.append("ML Pattern Detected")

        # ---------------------------
        # Health Score Calculation
        # ---------------------------
        health_score = 100

        if speed > 100:
            health_score -= 20

        if temperature > 85:
            health_score -= 25

        if fuel < 20:
            health_score -= 20

        if ml_anomaly:
            health_score -= 30

        health_score = max(0, health_score)

        # ---------------------------
        # Severity Level
        # ---------------------------
        if health_score >= 80:
            severity = "Healthy"
        elif health_score >= 50:
            severity = "Warning"
        else:
            severity = "Critical"

        anomaly_reason = " | ".join(reasons)

        VehicleTelemetry.objects.create(
            speed=speed,
            fuel_level=fuel,
            temperature=temperature,
            latitude=latitude,
            longitude=longitude,
            rule_anomaly=rule_anomaly,
            ml_anomaly=ml_anomaly,
            anomaly_reason=anomaly_reason,
            health_score=health_score,
            severity=severity
        )

        return Response({"message": "Telemetry stored successfully"})