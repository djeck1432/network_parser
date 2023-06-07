import json
import os
import unittest
from unittest.mock import MagicMock, mock_open, patch

from pydantic import ValidationError

from app.config import Config, ConfigMap
from app.main import get_config_json, get_interface_data, main

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class TestGetConfigJson(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data='{"key":"value"}')
    @patch("json.load")
    def test_get_config_json(self, json_mock, open_mock):
        json_mock.return_value = {"key": "value"}

        result = get_config_json()

        open_mock.assert_called_once_with(
            os.path.join(BASE_DIR, Config.config_name), "r"
        )
        json_mock.assert_called_once()
        self.assertEqual(result, {"key": "value"})

    @patch("builtins.open", new_callable=mock_open, read_data='{"key":"value"}')
    @patch("json.load")
    def test_get_config_json_invalid_json(self, json_mock, open_mock):
        json_mock.side_effect = json.decoder.JSONDecodeError(
            "Invalid JSON", doc="", pos=0
        )

        with self.assertRaises(Exception) as context:
            get_config_json()

        self.assertEqual(str(context.exception), "JSON file is not valid")


class TestGetInterfaceData(unittest.TestCase):
    def test_get_interface_data_with_correct_keys(self):
        json_data = {
            ConfigMap.main_key: {
                ConfigMap.native_key: {ConfigMap.interface_key: "test_interface_data"}
            }
        }

        expected_result = "test_interface_data"

        result = get_interface_data(json_data)

        self.assertEqual(result, expected_result)

    def test_get_interface_data_with_incorrect_keys(self):
        json_data = {
            "wrong_main_key": {
                "wrong_native_key": {"wrong_interface_key": "test_interface_data"}
            }
        }

        with self.assertRaises(Exception) as context:
            get_interface_data(json_data)

        self.assertTrue("JSON file has wrong structure" in str(context.exception))


class MockDBManager:
    """
    This class is used to mock the DBManager class.
    """

    def __init__(self):
        pass

    def add_entry(self, *args, **kwargs):
        return None

    def get_portal_channel_id(self, *args, **kwargs):
        return None


class TestMain(unittest.TestCase):
    @patch("app.main.get_config_json")
    @patch("app.main.DBManager", return_value=MockDBManager())
    @patch("app.main.get_interface_data")
    @patch("app.models.NetworkConfigPydanticModel")
    @patch("app.main.logger")
    def test_main(
        self,
        mock_logger,
        mock_network_config_model,
        mock_get_interface_data,
        mock_db_manager,
        mock_get_config_json,
    ):
        mock_get_config_json.return_value = {
            ConfigMap.main_key: {
                ConfigMap.native_key: {ConfigMap.interface_key: "test_interface_data"}
            }
        }

        mock_get_interface_data.return_value = {
            "Port-channel": [
                {
                    "name": "test1",
                    "description": "description1",
                    "mtu": "mtu1",
                    ConfigMap.port_config_key: {"number": "number1"},
                }
            ],
            "TenGigabitEthernet": None,
        }

        mock_network_config_model.side_effect = [
            MagicMock(),
            ValidationError(
                model="NetworkConfigPydanticModel", errors=[{"msg": "error"}]
            ),
        ]

        main()

        mock_logger.info.assert_called_with("No data for GigabitEthernet")

        assert mock_logger.info.call_count == 2
        assert mock_logger.error.call_count == 1
