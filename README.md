# Car Rental API

## Overview
A REST API for a car rental service with two core endpoints:
- List available cars for a specific date
- Create a booking for a car on a given date

## Design Choices

### Database Schema
**Minimalist Approach**:
- Only 2 tables: `Car` and `Booking`
- No user system (bookings contain customer info directly)
- No `is_available` flag (availability is dynamic based on booking dates)

**Why No Static Availability Flag?**
- A car's availability depends on date ranges, not a boolean
- Calculated in real-time by checking booking conflicts
- More accurate than maintaining a flag that could get out of sync

**Operational Constraints**:
- 1-day buffer between bookings (cars are being cleaned/prepared)
  - Example: If a booking ends Dec 5th, next available is Dec 7th
- Maximum 5-day rental period (business rule)

### Architecture
**Separation of Concerns**:
- `models/`: Database schema definitions
- `schemas/`: Pydantic models for request/response validation
- `services/`: Business logic (e.g., `CarService.py`, `BookingService.py`)
- `api/`: FastAPI route handlers

**Key Implementation Details**:
- Availability calculation uses SQL date range checks
- Price calculation happens at booking time (price_per_day × days)

## Technical Features

### Built With
- Python 3.13+
- FastAPI 0.115.12
- Pydantic 2.11.3
- SQLAlchemy (ORM) 2.0.40
- MySQL 9.3.0s

### Quality Assurance
- Pinned dependency versions (see requirements.txt)
- E2E and integration tests (pytest)
- Input validation via Pydantic

### Sample Data Generation
The `generate_cars.py` script:
- Creates cars with realistic distribution:
  - Economy (25%) | Standard (40%) | Luxury (10%) | SUV (20%) | Limousine (5%)
- Generates random bookings for testing availability logic

## Getting Started

### Prerequisites
- Docker and Docker Compose installed

### Quick Start with Docker
1. Clone the repository:
   ```bash
   git clone https://github.com/JavierSanchezCastro/Bookline_Coding_test.git
   cd bookline
   ```
2. Start all services:
   ```bash
   docker compose up -d
   ```
3. Access the services:
   - API: http://localhost:8000
   - Database Admin (Adminer): http://localhost:8080
   - Interactive API Docs:
     - Swagger UI: http://localhost:8000/docs
     - ReDoc: http://localhost:8000/redoc

4. Generate sample data (optional):
   ```bash
   docker compose run --rm backend generate_cars
   ```

### Testing
Run the test suite with:
```bash
docker compose exec backend pytest -v
```

## API Documentation
Interactive docs available at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)


## Potential Improvements

**Database Layer**:
- Async SQLAlchemy for better performance
- Redis cache for frequent availability queries

**Features**:
- Full CRUD operations for cars/bookings
- Authentication/authorization system
- Cancellation policies

**Operational**:
- Proper migration system (Alembic)




----------------------

