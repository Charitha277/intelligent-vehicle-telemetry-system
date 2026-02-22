from django.db import models

class VehicleTelemetry(models.Model):
    speed = models.FloatField()
    fuel_level = models.FloatField()
    temperature = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    rule_anomaly = models.BooleanField(default=False)
    ml_anomaly = models.BooleanField(default=False)

    anomaly_reason = models.CharField(max_length=255, blank=True)
    health_score = models.FloatField(default=100)
    severity = models.CharField(max_length=20, default="Healthy")

    def __str__(self):
        return f"Speed: {self.speed} | Temp: {self.temperature}"