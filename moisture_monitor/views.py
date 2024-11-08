import requests
from django.http import JsonResponse
from django.shortcuts import render
from .models import MoistureReading
from django.utils import timezone
import pytz
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Define calibration points (use your measured values for ADC_DRY and ADC_WET)
ADC_DRY = 0      # Replace with actual dry value
ADC_WET = 4095   # Replace with actual wet value (assuming 12-bit ADC)

def view_moisture(request):
    readings = MoistureReading.objects.order_by('-timestamp')[:10]
    return render(request, "moisture_monitor/moisture_view.html", {"readings": readings})

def latest_reading(request):
    try:
        # Send a request to the ESP device
        response = requests.get("http://192.168.4.1", timeout=5)
        adc_value = int(response.text.strip())

        # Map ADC value to percentage based on calibration
        if adc_value <= ADC_DRY:
            moisture_percentage = 0
        elif adc_value >= ADC_WET:
            moisture_percentage = 100
        else:
            moisture_percentage = ((adc_value - ADC_DRY) / (ADC_WET - ADC_DRY)) * 100

    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to ESP: {e}")
        return JsonResponse({"timestamp": None, "moisture_level": 0})

    # Save the reading with timezone-aware timestamp
    local_time = timezone.now().astimezone(pytz.timezone("America/Mexico_City"))
    reading = MoistureReading.objects.create(
        timestamp=local_time,
        adc_value=moisture_percentage
    )

    # Return JSON with the timestamp and moisture percentage
    return JsonResponse({
        "timestamp": local_time.strftime('%Y-%m-%d %H:%M:%S'),
        "moisture_level": moisture_percentage
    })

