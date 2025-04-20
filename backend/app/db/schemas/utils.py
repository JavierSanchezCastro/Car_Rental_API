from typing import Annotated
from pydantic import FutureDate, Field
from datetime import date, timedelta

FutureDateOneYear = Annotated[FutureDate, Field(..., le=date.today() + timedelta(days=365))]
