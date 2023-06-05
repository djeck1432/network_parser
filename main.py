import os
import json
import logging

from db_manager import DBManager
from config import Config, ConfigMap
from models import NetworkConfigPydanticModel
from pydantic.error_wrappers import ValidationError
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_config_json() -> dict:
    """
    This function reads the JSON file and returns its content.
    :return: dict
    """
    file_path = os.path.join(BASE_DIR, Config.config_name)
    with open(file_path, 'r') as f:
        try:
            json_data = json.load(f)
        except json.decoder.JSONDecodeError:
            raise Exception("JSON file is not valid")

    return json_data


def get_interface_data(json_data: dict) -> dict:
    """
    This function returns the interface data from the JSON file.
    If the JSON file has wrong structure, an exception is raised.
    :param json_data: dict
    :return: dict
    """
    try:
        config_data = json_data[ConfigMap.main_key]
        native_data = config_data[ConfigMap.native_key]
        interface_data = native_data[ConfigMap.interface_key]
    except KeyError:
        raise Exception("JSON file has wrong structure")
    return interface_data


if __name__ == "__main__":
    json_data = get_config_json()
    db_manager = DBManager()
    interface_data = get_interface_data(json_data)

    for interface_name in ConfigMap.activated_interface_names:
        interface_config_data = interface_data.get(interface_name)
        if not interface_config_data:
            logger.info(f"No data for {interface_name}")
            continue

        result = []
        for item in interface_config_data:
            port_config = item.get(ConfigMap.port_config_key)
            try:
                result_item = NetworkConfigPydanticModel(
                    name=f"{interface_name}{item.get('name')}",
                    description=item.get("description"),
                    max_frame_size=item.get("mtu"),
                    config=item,
                    port_channel_id=port_config and port_config.get("number"),
                )
                db_manager.add_entry(result_item)
            except ValidationError as exc:
                logger.error(f"Error while validating data: {exc}", exc_info=True)
                continue
