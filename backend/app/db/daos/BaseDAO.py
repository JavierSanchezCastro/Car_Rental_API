from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from pydantic import UUID4


class BaseDAO(ABC):
    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def create(self, request):
        pass

    @abstractmethod
    def get_all(self, request):
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: UUID4):
        pass
