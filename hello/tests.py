from django.db.models import Max
from django.test import Client, TestCase

from .models import Airport, Flight, Passenger
# Create your tests here.

class ModelsTestCase(TestCase):

	def setUp(self):

		a1 = Airport.objects.create(symbol="AAA", city="City A")
		a2 = Airport.objects.create(symbol="BBB", city="City B")

		Flight.objects.create(origin=a1, destination=a2, duration=100)
		Flight.objects.create(origin=a2, destination=a2, duration=200)
		Flight.objects.create(origin=a2, destination=a1, duration=-200)
	
	def test_departure_count(self):
		a = Airport.objects.get(symbol="BBB")
		self.assertEqual(a.departures.count(), 2)

	def test_arrivals_count(self):
		a = Airport.objects.get(symbol="AAA")
		self.assertEqual(a.arrivals.count(), 1)

	def test_validity_of_flights(self):
		a1 = Airport.objects.get(symbol="AAA")
		a2 = Airport.objects.get(symbol="BBB")
		f = Flight.objects.get(origin=a1, destination=a2, duration=100)
		self.assertTrue(f.is_valid_flight())

	def test_invalid_destination(self):
		a2 = Airport.objects.get(symbol="BBB")
		f = Flight.objects.get(origin=a2, destination=a2)
		self.assertFalse(f.is_valid_flight())

	def test_invalid_duration(self):
		a1 = Airport.objects.get(symbol="AAA")
		a2 = Airport.objects.get(symbol="BBB")
		f = Flight.objects.get(origin=a2, destination=a1, duration=-200)
		self.assertFalse(f.is_valid_flight())

	def test_index(self):
		c = Client()
		response = c.get("/")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context["flights"].count(), 3)
	
	def test_valid_flight_page(self):
		a1 = Airport.objects.get(symbol="BBB")
		f = Flight.objects.get(origin=a1, destination=a1)

		c = Client()
		response = c.get(f"/{f.id}")
		self.assertEqual(response.status_code, 200)

	def test_invalid_flight_page(self):
		max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]

		c = Client()
		response = c.get(f"/{max_id + 1}")
		self.assertEqual(response.status_code, 404)

	def test_flight_page_passengers(self):
		f = Flight.objects.get(pk=1)
		p = Passenger.objects.create(first="Alice", last="Adams")
		f.passengers.add(p)

		c = Client()
		response = c.get(f"/{f.id}")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context["passengers"].count(), 1)

	def test_flig_page_nopassengers(self):
		f = Flight.objects.get(pk=1)
		p = Passenger.objects.create(first="Alice", last="Adams")

		c = Client()
		response = c.get(f"/{f.id}")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context["no_passengers"].count(), 1)



