import sys
import os
import random
from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from sqlalchemy import not_

#Add the backend directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

from db.session import SessionLocal, engine
from db.models.Car import Car, CarType
from db.models.Booking import Booking
from db.models.Base import Base

Base.metadata.create_all(bind=engine)

def generate_cars(cars_to_generate: int = 5):
    db: Session = SessionLocal()

    #Car distribution
    car_distribution = {
        CarType.ECONOMY: 0.25,    #25%
        CarType.STANDARD: 0.40,   #40%
        CarType.LUXURY: 0.10,     #10%
        CarType.SUV: 0.20,        #20%
        CarType.LIMOUSINE: 0.05   #5%
    }

    #Brands
    car_brands_models = {
        CarType.ECONOMY: [
            ("Toyota", "Yaris", 2020, 30),
            ("Hyundai", "i20", 2021, 35),
            ("Kia", "Rio", 2019, 32),
            ("Volkswagen", "Polo", 2022, 38)
        ],
        CarType.STANDARD: [
            ("Toyota", "Corolla", 2021, 50),
            ("Honda", "Civic", 2022, 55),
            ("Volkswagen", "Golf", 2020, 52),
            ("Ford", "Focus", 2021, 48)
        ],
        CarType.LUXURY: [
            ("BMW", "5 Series", 2022, 120),
            ("Mercedes", "E-Class", 2021, 130),
            ("Audi", "A6", 2022, 125),
            ("Lexus", "ES", 2021, 110)
        ],
        CarType.SUV: [
            ("Toyota", "RAV4", 2021, 70),
            ("Nissan", "Qashqai", 2022, 65),
            ("Hyundai", "Tucson", 2020, 68),
            ("Kia", "Sportage", 2022, 72)
        ],
        CarType.LIMOUSINE: [
            ("Mercedes", "S-Class", 2022, 200),
            ("BMW", "7 Series", 2021, 190),
            ("Audi", "A8", 2022, 195),
            ("Rolls-Royce", "Phantom", 2021, 500)
        ]
    }

    cars_created = 0

    for car_type, percentage in car_distribution.items():
        quantity = round(cars_to_generate * percentage)
        
        if cars_created + quantity > cars_to_generate:
            quantity = cars_to_generate - cars_created
        
        for _ in range(quantity):
            brand, model, year, price = random.choice(car_brands_models[car_type])
            
            varied_price = price * random.uniform(0.9, 1.1)
            
            car = Car(
                brand=brand,
                model=model,
                type=car_type,
                year=year,
                price_per_day=round(varied_price, 2),
            )
            
            db.add(car)
            cars_created += 1
        
        if cars_created >= cars_to_generate:
            break

    db.commit()
    print(f"✅ {cars_created} cars inserted into the database.")

def is_car_available_for_dates(car: Car, start_date: date, end_date: date) -> bool:
    for booking_car in car.bookings:
        if booking_car.booking_date <= end_date and start_date <= booking_car.end_booking_date:
            return False
    return True

def generate_random_date_in_current_month() -> date:
    """Generate a random date within the current month"""
    today = datetime.now().date()
    
    if today.month == 12:
        last_day = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        last_day = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
    
    random_day = random.randint(1, last_day.day)
    return today.replace(day=random_day)

def generate_bookings(num_bookings: int = 20):
    db: Session = SessionLocal()
    all_cars: list[Car] = db.query(Car).all()
    
    if not all_cars:
        print("❌ No cars available to create bookings")
        return
    
    bookings_created = 0
    attempts = 0
    max_attempts = num_bookings * 3  # Prevent infinite loops
    
    while bookings_created < num_bookings and attempts < max_attempts:
        attempts += 1
        
        #Select random car
        car = random.choice(all_cars)
        
        #Generate random booking dates
        booking_date = generate_random_date_in_current_month()
        days = random.randint(1, 5)
        end_date = booking_date + timedelta(days=days)
        
        if not is_car_available_for_dates(car, booking_date, end_date):
            continue  #Skip if car is not available
        
        #Create booking
        client_num = random.randint(1, 1000)
        booking = Booking(
            car_id=car.id,
            customer_name=f"Client {client_num}",
            customer_email=f"client{client_num}@example.com",
            booking_date=booking_date,
            end_booking_date=end_date,
            days=days,
            total_price=round(car.price_per_day * days, 2)
        )
        
        db.add(booking)
        db.commit()
        bookings_created += 1
    
    db.commit()
    
    print(f"✅ {bookings_created} bookings created successfully")
    
    return bookings_created

if __name__ == "__main__":
    print("Generating Data...")
    generate_cars(10)
    generate_bookings(30)