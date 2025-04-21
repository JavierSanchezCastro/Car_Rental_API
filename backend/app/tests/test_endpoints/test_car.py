from datetime import date, timedelta
import pytest
from sqlalchemy import select
from db.models.Car import Car
from db.models.Booking import Booking

def test_get_available_cars_no_bookings(client, sample_car):
    """Test that all cars are available when there are no bookings"""
    test_date = date.today() + timedelta(days=5)
    
    response = client.get(f"/car/available?date={test_date}")
    assert response.status_code == 200
    
    available_cars = response.json()
    assert len(available_cars) > 0
    assert all(car['max_days'] >= 1 for car in available_cars)
    
    #Verify the sample car is in the response
    sample_car_data = next((car for car in available_cars if car['uuid'] == str(sample_car.uuid)), None)
    assert sample_car_data is not None
    assert sample_car_data['max_days'] == 5  #Max allowed by the system

def test_get_available_cars_with_booking(client, db_session, sample_car):
    """Test that cars with bookings on the selected date are not available"""
    #Create a booking for the sample car
    booking_date = date.today() + timedelta(days=3)
    booking = Booking(
        car_id=sample_car.id,
        customer_name="Test User",
        customer_email="test@example.com",
        booking_date=booking_date,
        end_booking_date=booking_date + timedelta(days=2),
        days=2,
        total_price=sample_car.price_per_day * 2
    )
    db_session.add(booking)
    db_session.commit()

    #Refresh the sample_car to ensure it's in the current session
    db_session.refresh(sample_car)
    
    #Test date during the booking period
    test_date = booking_date + timedelta(days=1)
    response = client.get(f"/car/available?date={test_date}")
    assert response.status_code == 200
    
    available_cars = response.json()
    assert str(sample_car.uuid) not in [car['uuid'] for car in available_cars]

def test_get_available_cars_max_days_calculation(client, db_session, sample_car):
    """Test that max_days is correctly calculated based on future bookings"""
    #Create a future booking for the sample car
    future_booking_date = date.today() + timedelta(days=10)
    booking = Booking(
        car_id=sample_car.id,
        customer_name="Test User",
        customer_email="test@example.com",
        booking_date=future_booking_date,
        end_booking_date=future_booking_date + timedelta(days=3),
        days=3,
        total_price=sample_car.price_per_day * 3
    )
    db_session.add(booking)
    db_session.commit()
    
    #Test date before the booking
    test_date = date.today() + timedelta(days=5)
    response = client.get(f"/car/available?date={test_date}")
    assert response.status_code == 200
    
    available_cars = response.json()
    sample_car_data = next((car for car in available_cars if car['uuid'] == str(sample_car.uuid)), None)
    
    #Should be available with max_days = (booking start date - test date) - 1
    expected_max_days = (future_booking_date - test_date).days - 1
    assert sample_car_data is not None
    assert sample_car_data['max_days'] == min(expected_max_days, 5)  #Capped at 5

def test_get_available_cars_invalid_date(client):
    """Test that invalid dates return appropriate errors"""
    #Date in the past
    past_date = date.today() - timedelta(days=1)
    response = client.get(f"/car/available?date={past_date}")
    assert response.status_code == 422
    
    #Date too far in the future (more than 1 year)
    future_date = date.today() + timedelta(days=366)
    response = client.get(f"/car/available?date={future_date}")
    assert response.status_code == 422