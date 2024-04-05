from django.shortcuts import render,redirect
from .models import Vehicle
from .models import TimeSlot
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
import json

from django.utils import timezone

# Create your views here.
def home(request):
   vehicles = Vehicle.objects.all()
   context = {'vehicles': vehicles}
   return render(request, 'home.html', context)

def planning(request):
    time_slots = TimeSlot.objects.all()
    time_slots_data = [{'start': slot.start.isoformat(), 'end': slot.end.isoformat(), 'day': slot.get_start_day()} for slot in time_slots]
    serialized_data = json.dumps(time_slots_data)
    return render(request, 'planning.html', {'time_slots': serialized_data})

def production(request):
    return render(request, 'production.html', context={'key': 'value'})

def book_vehicle(request):
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle_id')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')

        try:
            # Assuming that vehicle_id is valid and exists in your Vehicle model
            vehicle = Vehicle.objects.get(id=vehicle_id)

            # Check if there is an overlapping reservation
            overlapping_reservation = TimeSlot.objects.filter(
                Q(vehicle=vehicle) &
                (
                    (Q(start__gte=start_date, start__lt=end_date) | Q(end__gt=start_date, end__lte=end_date)) |
                    (Q(start__lte=start_date, end__gte=end_date)) |
                    (Q(start__lt=start_date, end__gt=end_date))
                )
            ).first()

            if overlapping_reservation:
                messages.error(request, 'This vehicle is already reserved during the requested time period.')
                return JsonResponse({'success': False, 'message': 'Overlapping reservation'})

            # Create a TimeSlot instance
            time_slot = TimeSlot(
                start=start_date,
                end=end_date,
                user=request.user,
                vehicle=vehicle
            )

        
            time_slot.full_clean()  
            time_slot.save()

            messages.success(request, 'Reservation successful!')
            return JsonResponse({'success': True, 'message': 'Reservation successful'})
        except ValidationError as ve:
            messages.error(request, f'Validation error: {ve}')
            return JsonResponse({'success': False, 'message': 'Validation error'})
        except Exception as e:
            messages.error(request, f'Error creating reservation: {e}')
            return JsonResponse({'success': False, 'message': 'Error creating reservation'})

    return HttpResponse("Invalid request method")

   
