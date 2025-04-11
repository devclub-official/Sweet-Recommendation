from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

class DataSource(ABC):
    @abstractmethod
    def get_data(self, *args, **kwargs):
        pass

class SQLAlchemyDataSource(DataSource):
    def __init__(self, session: Session):
        self.session = session
        
    def get_data(self, query_func, *args, **kwargs):
        with self.session as session:
            return query_func(session, *args, **kwargs)
