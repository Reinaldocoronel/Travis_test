from django.contrib import admin
from .models import Airport, Flight, Passenger

class PassengerInLine(admin.StackedInline):
	model = Passenger.flights.through
	extra = 1

class FlightAdmin(admin.ModelAdmin):
	inlines = [PassengerInLine]
		
class PassengerAdmin(admin.ModelAdmin):
	filter_horizontal = ("flights",)

# Register your models here.
admin.site.register(Airport)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passenger, PassengerAdmin)