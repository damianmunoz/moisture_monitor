from django.db import models

class MoistureReading(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    adc_value = models.IntegerField()

    def __str__(self):
        return f"{self.timestamp}: {self.adc_value}"

