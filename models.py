from typing import Any, Optional

from pydantic import BaseModel
from sqlalchemy import JSON, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm.session import Session

Base = declarative_base()


class NetworkConfigModel(Base):
    """
    This class is used for database mapping.
    """

    __tablename__ = "network_config"

    id = Column(Integer, primary_key=True)
    connection = Column(Integer)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(255))
    config = Column(JSON)
    type = Column(String(50))
    infra_type = Column(String(50))
    port_channel_id = Column(Integer)
    max_frame_size = Column(Integer)

    @classmethod
    def get_id_by_name(cls, session: Session, name: str) -> int | None:
        """
        This method returns the ID of the entry by its name.
        :param session: db session
        :param name: name of the entry
        :return: None or int
        """
        instance = session.query(cls).filter(cls.name==name).first()
        return instance.id if instance else None


class NetworkConfigPydanticModel(BaseModel):
    """
    This class is used for data validation.
    """

    name: str
    config: Any

    connection: Optional[int] = None
    description: Optional[str] = None
    type: Optional[str] = None
    infra_type: Optional[str] = None
    port_channel_id: Optional[int] = None
    max_frame_size: Optional[int] = None

    class Config:
        orm_mode = True
