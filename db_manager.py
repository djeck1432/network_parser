import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import (DisconnectionError, IntegrityError,
                            InvalidRequestError)
from sqlalchemy.orm import sessionmaker

from app.config import Config
from app.models import NetworkConfigModel, NetworkConfigPydanticModel

logger = logging.getLogger(__name__)


class DBManager:
    DATABASE_URL_TEMPLATE = "postgresql://{user}:{password}@{host}:{port}/{db_name}"

    def __init__(self):
        """
        This class is responsible for the database connection and data insertion.
        """
        self.engine = create_engine(self._get_database_url())
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def _get_database_url(self) -> str:
        return self.DATABASE_URL_TEMPLATE.format(
            user=Config.db_user,
            password=Config.db_password,
            host=Config.db_host,
            port=Config.db_port,
            db_name=Config.db_name,
        )

    def add_entry(self, data: NetworkConfigPydanticModel) -> None:
        """
        This function adds a new entry to the database.
        :param data: data to be added
        :return: None
        """
        new_entry = NetworkConfigModel(**data.dict())
        try:
            self.session.add(new_entry)
            self.session.commit()
        except (IntegrityError, InvalidRequestError, DisconnectionError) as exc:
            logger.error(
                f"Error while adding data to the database: {exc}", exc_info=True
            )

    def get_portal_channel_id(self, port_config: dict | None) -> int | None:
        """
        This function returns the ID of the portal_channel_id with the given name.
        :param port_config: port config
        :return: None or int
        """
        if not port_config:
            return None

        if port_number := port_config.get("number"):
            return NetworkConfigModel.get_id_by_name(
                self.session, f"Port-channel{port_number}"
            )
