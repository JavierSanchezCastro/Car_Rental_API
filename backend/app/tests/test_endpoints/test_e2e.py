from datetime import date, timedelta
from fastapi import status

def test_booking_e2e_flow(client):
    """Test complete E2E flow: check availability -> create booking -> verify changes"""
    #1. Get available cars for a future date
    test_date = date.today() + timedelta(days=5)
    response = client.get(f"/car/available?date={test_date}")
    assert response.status_code == status.HTTP_200_OK
    available_cars = response.json()
    assert len(available_cars) > 0
    
    #Select the first available car
    car_to_book = available_cars[0]
    car_uuid = car_to_book['uuid']
    max_days_available = car_to_book['max_days']
    
    #2. Create a booking for this car
    booking_data = {
        "car_uuid": car_uuid,
        "customer_name": "E2E Test User",
        "customer_email": "e2e_test@example.com",
        "booking_date": test_date.isoformat(),
        "days": min(3, max_days_available)  #Book for 3 days or max available if less
    }
    
    response = client.post("/booking/", json=booking_data)
    assert response.status_code == status.HTTP_200_OK
    booking_response = response.json()
    
    #Verify booking details
    assert booking_response["customer_name"] == booking_data["customer_name"]
    assert booking_response["customer_email"] == booking_data["customer_email"]
    assert booking_response["booking_date"] == booking_data["booking_date"]
    assert booking_response["days"] == booking_data["days"]
    assert "uuid" in booking_response
    assert "total_price" in booking_response
    
    #3. Verify car is not available for the booked dates
    #Check during the booking period
    booking_mid_date = test_date + timedelta(days=1)
    response = client.get(f"/car/available?date={booking_mid_date}")
    assert response.status_code == status.HTTP_200_OK
    available_cars_after_booking = response.json()
    assert car_uuid not in [car['uuid'] for car in available_cars_after_booking]
    
    #4. Verify booking appears in the car's bookings
    response = client.get(f"/car/{car_uuid}/bookings")
    assert response.status_code == status.HTTP_200_OK
    car_bookings = response.json()
    
    #Find our booking in the list
    booking_found = next(
        (b for b in car_bookings if b["uuid"] == booking_response["uuid"]),
        None
    )
    assert booking_found is not None
    assert booking_found["customer_name"] == booking_data["customer_name"]
    
    #5. Verify we can retrieve the booking directly
    response = client.get(f"/booking/{booking_response['uuid']}")
    assert response.status_code == status.HTTP_200_OK
    booking_details = response.json()
    assert booking_details["uuid"] == booking_response["uuid"]
    assert booking_details["car"]["uuid"] == car_uuid