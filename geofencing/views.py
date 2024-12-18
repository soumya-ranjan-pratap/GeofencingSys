from django.shortcuts import render
from django.http import JsonResponse
from .models import CheckInOut
from datetime import datetime
from geopy.distance import geodesic
from django.shortcuts import render
from django.http import JsonResponse
from .models import CheckInOut
from datetime import datetime

GEOFENCE_COORDS = (20.301176124999998, 85.856136)  # Example coordinates (latitude, longitude)
GEOFENCE_RADIUS = 0.1  # 200 meters

def index(request):
    return render(request, 'geofencing/index.html')


def check_geofence(request):
    if request.method == 'POST':
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))
        user_coords = (latitude, longitude)
        print(f"Received coordinates: Latitude={latitude}, Longitude={longitude}")  # Debugging line

        distance = geodesic(GEOFENCE_COORDS, user_coords).km
        print(f"Calculated distance: {distance} km")  # Debugging line

        if distance <= GEOFENCE_RADIUS:
            print("User is inside the geofence")
            return JsonResponse({"status": "inside"})
        print("User is outside the geofence")
        return JsonResponse({"status": "outside"})



def record_action(request):
    try:
        if request.method == 'POST':
            # Get the data from the POST request
            username = request.POST.get('username')
            action = request.POST.get('action')

            # Check if action and username are being received
            print(f"Received action: {action}, Username: {username}")

            # Create a record for the CheckInOut model
            if action == 'check-in':
                record = CheckInOut(username=username, check_in=datetime.now())
            elif action == 'check-out':
                record = CheckInOut(username=username, check_out=datetime.now())
            else:
                return JsonResponse({"status": "error", "message": "Invalid action"})

            # Save the record to the database
            record.save()
            print(f"Record saved: {record.username} - Check-in: {record.check_in}, Check-out: {record.check_out}")

            return JsonResponse({"status": "success", "message": f"{action} recorded successfully"})

    except Exception as e:
        print(f"Error in record_action view: {e}")
        return JsonResponse({"status": "error", "message": f"An error occurred: {e}"})

