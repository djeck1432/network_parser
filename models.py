from typing import Any, Optional

from pydantic import BaseModel
from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class NetworkConfigModel(Base):
    """
    This class is used for database mapping.
    """

    __tablename__ = "network_config"

    id = Column(Integer, primary_key=True)
    connection = Column(Integer)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    config = Column(JSON)
    type = Column(String(50))
    infra_type = Column(String(50))
    port_channel_id = Column(Integer)
    max_frame_size = Column(Integer)


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
