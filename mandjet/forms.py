from django import forms
from .models import TimeSlot

class ReservationForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['start', 'end']