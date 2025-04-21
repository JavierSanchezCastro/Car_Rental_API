from sqlalchemy.orm import Session
from db.models.Car import Car
from db.daos.CarDAO import CarDAO
from db.daos.BookingDAO import BookingDAO
from pydantic import UUID4
from fastapi import status, HTTPException
from datetime import date
from sqlalchemy import select, func, and_, literal
from db.models.Booking import Booking
from db.schemas.car import CarShow_MaxDays
from datetime import datetime, timedelta
import calendar
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
from logger import logger


class CarService:

    @staticmethod
    def get_by_uuid(uuid: UUID4, db: Session):
        logger.info(f"Fetching car with UUID: {uuid}")
        car = CarDAO(db).get_by_uuid(uuid=uuid)
        if not car:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Car with uuid={uuid} not found")
        return car
    
    #@staticmethod
    #def get_availables(date: date, db: Session):
    #    cars = CarDAO(db).get_all()
    #    av_cars = []
    #    for car in cars:
    #        for booking in car.bookings:
    #            if booking.booking_date <= date and date <= booking.end_booking_date:
    #                break
    #        else:
    #            av_cars.append(car)
    #    return av_cars

    @staticmethod
    def get_availables(date_selected: date, db: Session):
        logger.info(f"Checking available cars for date: {date_selected}")
        future_booking_subq = (
            select(func.min(Booking.booking_date))
            .where(and_(
                Booking.car_id == Car.id,
                Booking.booking_date > date_selected
            ))
            .correlate(Car)
            .scalar_subquery()
        )

        booked_car_subq = (
            select(Booking.car_id)
            .where(and_(
                Booking.booking_date <= date_selected,
                Booking.end_booking_date >= date_selected
            ))
        )

        next_booking_or_far = func.coalesce(future_booking_subq, literal('2099-12-31'))

        max_days_available = func.datediff(next_booking_or_far, date_selected) - 1

        query = (
            select(Car, max_days_available.label("max_days_available"))
            .where(Car.id.not_in(booked_car_subq))
            .having(max_days_available > 0)
        )

        results = db.execute(query).all()

        response = [
            CarShow_MaxDays(
                id=car.id,
                brand=car.brand,
                model=car.model,
                type=car.type,
                year=car.year,
                price_per_day=car.price_per_day,
                uuid=car.uuid,
                max_days=min(max_days, 5)
            )
            for car, max_days in results
        ]
        logger.info(f"Found {len(response)} available cars")

        return response
    
    @staticmethod
    def get_availables_image(db: Session):
        bookings = BookingDAO(db).get_all()
        today = datetime.today()
        year = today.year
        month = today.month

        first_day = date(year, month, 1)
        last_day = date(year, month, calendar.monthrange(year, month)[1])

        fig, ax = plt.subplots(figsize=(12, 2 + len(bookings) * 0.4))

        ax.set_xlim(first_day, last_day)
        ax.set_ylim(0, len(bookings) + 1)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
        ax.set_yticks([])
        ax.set_title(f"Reservas del mes de {today.strftime('%B %Y')}", fontsize=14)

        for i, booking in enumerate(bookings, 1):
            bar_start = max(booking.booking_date, first_day)
            bar_end = min(booking.end_booking_date, last_day)
            if bar_start <= bar_end:
                duration = (bar_end - bar_start).days
                ax.barh(i, duration, left=bar_start, height=0.4, color='skyblue')
                label_pos = bar_start + timedelta(days=duration / 2)
                ax.text(label_pos, i, f"{booking.customer_name} - {booking.car.brand} {booking.car.model} ({booking.car.id})", ha='center', va='center', fontsize=9, color='black')

        plt.tight_layout()
        plt.grid(axis='x', linestyle='--', alpha=0.5)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        return buf

    @staticmethod
    def is_car_available(car_id: int, start_date: date, end_date: date, db: Session):
        logger.debug(
            f"Checking availability for car ID: {car_id} | "
            f"Dates: {start_date} to {end_date}"
        )
        overlap_check = (
            select(Booking.car_id)
            .where(and_(
                Booking.car_id == car_id,
                Booking.booking_date <= end_date,
                Booking.end_booking_date >= start_date
            ))
            .limit(1)
        )

        overlapping_booking = db.execute(overlap_check).scalar()

        return overlapping_booking is None