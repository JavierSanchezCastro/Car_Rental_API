import sys
import os
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

#Add the backend directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

from db.session import SessionLocal, engine
from db.models.Car import Car, CarType
from db.models.Booking import Booking
from db.models.Base import Base

Base.metadata.create_all(bind=engine)

def generate_cars():
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

    cars_to_generate = 40
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
                is_available=True
            )
            
            db.add(car)
            cars_created += 1
        
        if cars_created >= cars_to_generate:
            break

    db.commit()
    print(f"✅ {cars_created} cars inserted into the database.")

def generate_bookings():
    db: Session = SessionLocal()
    today = datetime.now().date()
    
    all_cars = db.query(Car).all()
    
    bookings_to_create = max(1, round(len(all_cars) * 0.3))
    booked_cars = random.sample(all_cars, bookings_to_create)
    
    bookings_created = 0
    
    for car in booked_cars:
        booking_date = today - timedelta(days=random.randint(0, 15))
        
        days = random.randint(1, 7)
        is_still_active = (booking_date + timedelta(days=days)) >= today
        
        client_num = random.randint(1, 100)
        booking = Booking(
            car_id=car.id,
            customer_name=f"Client {client_num}",
            customer_email=f"client{client_num}@example.com",
            booking_date=booking_date,
            days=days,
            total_price=car.price_per_day * days
        )
        db.add(booking)
        
        car.is_available = not is_still_active
        bookings_created += 1
    
    db.commit()
    print(f"✅ {bookings_created} bookings created (30% of cars).")
    print(f"📊 {sum(1 for car in all_cars if not car.is_available)} cars are now unavailable.")
    return bookings_created

if __name__ == "__main__":
    print("Generating Data...")
    generate_cars()
    generate_bookings()