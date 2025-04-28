from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, CruiseDetailFinal, Booking
from datetime import date, timedelta

class CruiseModelTests(TestCase):
    def setUp(self):
        self.cruise = CruiseDetailFinal.objects.create(
            type='Luxury',
            origin='Miami',
            departure='Port Miami',
            visiting='Caribbean Islands',
            nights=7,
            decks=10,
            cost=1000,
            seats=100,
            startDate=date.today(),
            endDate=date.today() + timedelta(days=7),
            cruiseName='Caribbean Dream',
            oceanviewRooms=50,
            InteriorRooms=50,
            oceanviewForward=20,
            oceanviewMiddle=20,
            oceanviewAft=10,
            InteriorForward=20,
            InteriorMiddle=20,
            InteriorAft=10,
            oceanviewRoomsCost=1500,
            InteriorRoomsCost=1000
        )

    def test_cruise_creation(self):
        self.assertEqual(self.cruise.cruiseName, 'Caribbean Dream')
        self.assertEqual(self.cruise.oceanviewRooms, 50)

    def test_room_count_validation(self):
        self.cruise.oceanviewForward = 30
        with self.assertRaises(ValidationError):
            self.cruise.clean()

class BookingAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.cruise = CruiseDetailFinal.objects.create(
            cruiseName='Test Cruise',
            startDate=date.today(),
            endDate=date.today() + timedelta(days=7)
        )
        self.client.force_authenticate(user=self.user)

    def test_create_booking(self):
        url = reverse('create_booking')
        data = {
            'cruise': self.cruise.id,
            'room_type': 'Oceanview',
            'room_number': 'B101',
            'location': 'forward',
            'user': self.user.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_rooms(self):
        url = reverse('get_rooms', kwargs={
            'cruise_id': self.cruise.id,
            'room_type': 'Oceanview',
            'location': 'forward'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
