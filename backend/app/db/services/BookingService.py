from sqlalchemy.orm import Session
from db.models.Booking import Booking
from db.daos.BookingDAO import BookingDAO
from pydantic import UUID4
from fastapi import status, HTTPException
from db.schemas.booking import BookingCreate
from db.services.CarService import CarService
from datetime import timedelta
from logger import logger


class BookingService:

    @staticmethod
    def get_by_uuid(uuid: UUID4, db: Session):
        logger.debug(f"Looking up booking with UUID: {uuid}")
        booking = BookingDAO(db).get_by_uuid(uuid=uuid)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Booking with uuid={uuid} not found")
        return booking
    
    @staticmethod
    def create(booking_info: BookingCreate, db: Session):
        logger.info(f"Attempting to create booking for car: {booking_info.car_uuid}")
        car = CarService.get_by_uuid(booking_info.car_uuid, db=db) #Already check with HTTPException

        logger.debug(f"Car found: {car.uuid} ({car.brand} {car.model})")
        start_booking = booking_info.booking_date
        end_booking = booking_info.booking_date + timedelta(days=booking_info.days)
        booking_data = booking_info.model_dump(exclude="car_uuid")
        booking_data["end_booking_date"] = end_booking
        booking_data["total_price"] = car.price_per_day * booking_info.days

        if CarService.is_car_available(car_id=car.id, start_date=start_booking, end_date=end_booking, db=db):
            booking = BookingDAO(db).create(car_id=car.id, booking_data=booking_data)
            logger.info(
                    f"Booking created successfully | "
                    f"ID: {booking.uuid} | "
                    f"Car: {car.brand} {car.model} | "
                    f"Dates: {booking_info.booking_date} to {booking.end_booking_date}"
                )
            return booking
        else:
            logger.warning(
                    f"Car not available | "
                    f"Car UUID: {booking_info.car_uuid} | "
                    f"Requested dates: {booking_info.booking_date} (+{booking_info.days} days)"
                )
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Car with uuid={car.uuid} is not available")
