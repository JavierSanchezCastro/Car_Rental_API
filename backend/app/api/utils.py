from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from db.session import get_session

SessionDB = Annotated[Session, Depends(get_session)]
