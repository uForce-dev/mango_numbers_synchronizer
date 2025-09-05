import logging
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from config import settings
from models import MangoLine

logger = logging.getLogger(__name__)


Base = declarative_base()


class PhoneNumberTable(Base):
    __tablename__ = "mango_office__phone_numbers"

    line_id = Column(Integer, primary_key=True)
    number = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=True)
    comment = Column(Text, nullable=True)
    region = Column(String(10), nullable=False)
    schema_id = Column(Integer, nullable=False)
    schema_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DatabaseService:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._connect()

    def _connect(self):
        try:
            connection_string = (
                f"postgresql://{settings.postgres_user}:{settings.postgres_password}"
                f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
            )

            self.engine = create_engine(connection_string, echo=False)
            self.SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine
            )

            Base.metadata.create_all(bind=self.engine)

            logger.info("Connected to PostgreSQL")

        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise

    def get_session(self) -> Session:
        return self.SessionLocal()

    def get_phone_number_by_number(
        self, session: Session, number: str
    ) -> Optional[PhoneNumberTable]:
        try:
            return (
                session.query(PhoneNumberTable)
                .filter(PhoneNumberTable.number == number)
                .first()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error fetching number {number}: {e}")
            return None

    def create_phone_number(self, session: Session, mango_line: MangoLine) -> bool:
        try:
            phone_number = PhoneNumberTable(
                line_id=mango_line.line_id,
                number=mango_line.number,
                name=mango_line.name,
                comment=mango_line.comment,
                region=mango_line.region,
                schema_id=mango_line.schema_id,
                schema_name=mango_line.schema_name,
            )
            session.add(phone_number)
            session.commit()
            logger.info(f"Created number: {mango_line.number}")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error creating number {mango_line.number}: {e}")
            session.rollback()
            return False

    def update_phone_number(
        self, session: Session, existing: PhoneNumberTable, mango_line: MangoLine
    ) -> bool:
        try:
            existing.line_id = mango_line.line_id
            existing.name = mango_line.name
            existing.comment = mango_line.comment
            existing.region = mango_line.region
            existing.schema_id = mango_line.schema_id
            existing.schema_name = mango_line.schema_name
            existing.updated_at = datetime.utcnow()

            session.commit()
            logger.info(f"Updated number: {mango_line.number}")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error updating number {mango_line.number}: {e}")
            session.rollback()
            return False

    def get_all_phone_numbers(self, session: Session) -> List[PhoneNumberTable]:
        try:
            return session.query(PhoneNumberTable).all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching all numbers: {e}")
            return []

    def close(self):
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")
