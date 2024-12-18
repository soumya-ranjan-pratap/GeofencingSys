from django.shortcuts import render
from django.http import JsonResponse
from .models import CheckInOut
from datetime import datetime
from geopy.distance import geodesic
from django.utils.timezone import now

GEOFENCE_COORDS = (20.301176124999998, 85.856136)  # Example coordinates (latitude, longitude)
GEOFENCE_RADIUS = 0.1  # 100 meters

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
    if request.method == 'POST':
        username = request.POST.get('username')
        action = request.POST.get('action')
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))

        # Debugging logs
        print(f"Action: {action}, User: {username}, Latitude: {latitude}, Longitude: {longitude}")

        if action == 'check-in':
            # Record check-in
            check_in = CheckInOut.objects.create(
                username=username,
                latitude=latitude,
                longitude=longitude,
                check_in=now()
            )
            return JsonResponse({'status': 'success', 'message': 'Check-In recorded!', 'id': check_in.id})
        
        elif action == 'check-out':
            # Find the latest Check-In record for the user (without a check-out time)
            check_out = CheckInOut.objects.filter(username=username, check_out__isnull=True).last()
            if check_out:
                check_out.longitude = longitude
                check_out.latitude = latitude
                check_out.check_out = now()
                check_out.save()
                return JsonResponse({'status': 'success', 'message': 'Check-Out recorded!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'No Check-In record found for this user.'})
        
        return JsonResponse({'status': 'error', 'message': 'Invalid action.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

