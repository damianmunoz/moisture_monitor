import requests
from django.http import JsonResponse
from django.shortcuts import render
from .models import MoistureReading
from django.utils import timezone
import pytz
import logging

# Set up logging
logger = logging.getLogger(__name__)

def view_moisture(request):
    # Retrieve the latest 10 readings for display
    readings = MoistureReading.objects.order_by('-timestamp')[:10]
    return render(request, "moisture_monitor/moisture_view.html", {"readings": readings})

def latest_reading(request):
    try:
        # Send a request to the ESP device
        response = requests.get("http://192.168.4.1", timeout=5)
        moisture_status = response.text.strip()

        # Interpret "OK" as 1; any other response as 0
        adc_value = 1 if moisture_status == "OK" else 0

    except requests.exceptions.RequestException as e:
        # Log error if connection fails and return a default response
        logger.error(f"Error connecting to ESP: {e}")
        return JsonResponse({"timestamp": None, "moisture_level": 0})

    # Ensure the timestamp is explicitly in the 'America/Mexico_City' timezone
    local_time = timezone.now().astimezone(pytz.timezone("America/Mexico_City"))
    reading = MoistureReading.objects.create(
        timestamp=local_time,
        adc_value=adc_value
    )

    # Return JSON with the timestamp and moisture level in readable format
    return JsonResponse({
        "timestamp": local_time.strftime('%Y-%m-%d %H:%M:%S'),
        "moisture_level": adc_value
    })
