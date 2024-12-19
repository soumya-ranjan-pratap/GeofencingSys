from django.shortcuts import render
from django.http import JsonResponse
from .models import CheckInOut
from datetime import datetime
from geopy.distance import geodesic
from django.utils.timezone import now
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm


GEOFENCE_COORDS = (20.3011975, 85.85613799999999)
GEOFENCE_RADIUS = 0.05  # 50 meters


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the index page
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'geofencing/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Error creating user. Please try again.')
    else:
        form = UserCreationForm()

    return render(request, 'geofencing/register.html', {'form': form})


def index(request):
    user = request.user
    return render(request, 'geofencing/index.html', {'user' : user})


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
            # Check if the user already has an open check-in (not checked out)
            existing_check_in = CheckInOut.objects.filter(username=username, check_out__isnull=True).first()
            if existing_check_in:
                return JsonResponse({'status': 'error', 'message': 'You are already checked in. Please check-out before checking in again.'})

            # Record check-in
            check_in = CheckInOut.objects.create(
                username=username,
                latitude=latitude,
                longitude=longitude,
                check_in=now()
            )
            return JsonResponse({'status': 'success', 'message': 'Check-In recorded!', 'id': check_in.id})
        
        elif action == 'check-out':
            # Find the most recent Check-In record for the user that hasn't been checked out
            check_in = CheckInOut.objects.filter(username=username, check_out__isnull=True).last()

            if not check_in:
                # No Check-In record found for this user, return an error
                return JsonResponse({'status': 'error', 'message': 'No recent Check-In record found for this user.'})
            
            # If a Check-In exists, record the Check-Out
            check_in.longitude = longitude
            check_in.latitude = latitude
            check_in.check_out = now()
            check_in.save()
            return JsonResponse({'status': 'success', 'message': 'Check-Out recorded!'})
        
        return JsonResponse({'status': 'error', 'message': 'Invalid action.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

