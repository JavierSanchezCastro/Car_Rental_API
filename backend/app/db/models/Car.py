from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from sqlalchemy import String, Integer, Enum, Numeric, and_
from db.models.Base import Base
from enum import Enum as PyEnum
from db.models.Booking import Booking

class CarType(str, PyEnum):
    ECONOMY = "economy"
    STANDARD = "standard"
    LUXURY = "luxury"
    SUV = "suv"
    LIMOUSINE = "limousine"

class Car(Base):
    brand: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    type: Mapped[CarType] = mapped_column(Enum(CarType), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    price_per_day: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    #is_available: Mapped[bool] = mapped_column(Boolean, default=True) is_available depende de los bookings

    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="car")
    bookings_future: Mapped[list["Booking"]] = relationship("Booking", back_populates="car", primaryjoin=lambda: and_(Booking.car_id == Car.id, Booking.booking_date >= date.today()), overlaps="bookings")
