from datetime import date, timedelta
import uuid
from fastapi import status

def test_create_booking_success(client, sample_car):
    """Test successful booking creation"""
    booking_date = date.today() + timedelta(days=5)
    booking_data = {
        "car_uuid": str(sample_car.uuid),
        "customer_name": "Test User",
        "customer_email": "test@example.com",
        "booking_date": booking_date.isoformat(),
        "days": 3
    }
    
    response = client.post("/booking/", json=booking_data)
    assert response.status_code == status.HTTP_200_OK
    
    booking_response = response.json()
    assert booking_response["customer_name"] == booking_data["customer_name"]
    assert booking_response["customer_email"] == booking_data["customer_email"]
    assert booking_response["booking_date"] == booking_data["booking_date"]
    assert booking_response["days"] == booking_data["days"]
    assert booking_response["total_price"] == sample_car.price_per_day * booking_data["days"]
    assert booking_response["end_booking_date"] == (booking_date + timedelta(days=booking_data["days"])).isoformat()
    assert "uuid" in booking_response

def test_create_booking_car_not_found(client):
    """Test booking creation with non-existent car"""
    booking_date = date.today() + timedelta(days=5)
    booking_data = {
        "car_uuid": str(uuid.uuid4()),  #Random UUID that doesn't exist
        "customer_name": "Test User",
        "customer_email": "test@example.com",
        "booking_date": booking_date.isoformat(),
        "days": 3
    }
    
    response = client.post("/booking/", json=booking_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()

def test_create_booking_date_in_past(client, sample_car):
    """Test booking creation with date in the past"""
    past_date = date.today() - timedelta(days=1)
    booking_data = {
        "car_uuid": str(sample_car.uuid),
        "customer_name": "Test User",
        "customer_email": "test@example.com",
        "booking_date": past_date.isoformat(),
        "days": 3
    }
    
    response = client.post("/booking/", json=booking_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_booking_date_too_far_in_future(client, sample_car):
    """Test booking creation with date more than 1 year in the future"""
    future_date = date.today() + timedelta(days=366)
    booking_data = {
        "car_uuid": str(sample_car.uuid),
        "customer_name": "Test User",
        "customer_email": "test@example.com",
        "booking_date": future_date.isoformat(),
        "days": 3
    }
    
    response = client.post("/booking/", json=booking_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_booking_too_many_days(client, sample_car):
    """Test booking creation with more than 5 days"""
    booking_date = date.today() + timedelta(days=5)
    booking_data = {
        "car_uuid": str(sample_car.uuid),
        "customer_name": "Test User",
        "customer_email": "test@example.com",
        "booking_date": booking_date.isoformat(),
        "days": 6  #More than allowed
    }
    
    response = client.post("/booking/", json=booking_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_booking_conflicting_dates(client, db_session, sample_car):
    """Test booking creation when car is already booked"""
    #Create an existing booking
    existing_booking_date = date.today() + timedelta(days=5)
    existing_booking = {
        "car_uuid": str(sample_car.uuid),
        "customer_name": "Existing User",
        "customer_email": "existing@example.com",
        "booking_date": existing_booking_date.isoformat(),
        "days": 3
    }
    client.post("/booking/", json=existing_booking)
    
    #Try to create a conflicting booking
    conflicting_booking_date = existing_booking_date + timedelta(days=1)
    conflicting_booking = {
        "car_uuid": str(sample_car.uuid),
        "customer_name": "New User",
        "customer_email": "new@example.com",
        "booking_date": conflicting_booking_date.isoformat(),
        "days": 2
    }
    
    response = client.post("/booking/", json=conflicting_booking)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "not available" in response.json()["detail"].lower()