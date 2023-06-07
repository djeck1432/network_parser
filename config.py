import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    """
    This class contains the database URI and other configuration parameters.
    """

    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    config_name = "configClear_v2.json"


@dataclass(frozen=True)
class ConfigMap:
    """
    This class contains all the keys that are used to access the data in the JSON file.
    """

    main_key = "frinx-uniconfig-topology:configuration"
    native_key = "Cisco-IOS-XE-native:native"
    interface_key = "interface"
    activated_interface_names = (
        "Port-channel",  # should be at first place
        "TenGigabitEthernet",
        "GigabitEthernet",
    )
    deactivated_interface_names = ("BDI", "Loopback")  # Not implemented yet
    port_config_key = "Cisco-IOS-XE-ethernet:channel-group"
