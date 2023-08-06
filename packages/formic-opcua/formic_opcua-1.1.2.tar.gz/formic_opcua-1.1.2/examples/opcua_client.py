# Copyright Formic Technologies 2023
import logging.config
import time

from formic_opcua import OpcuaClient

LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s | %(levelname)s | %(name)s | %(module)s | %(funcName)s:%(lineno)d | %(message)s',
        },
    },
    'handlers': {
        'root_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './opcua.log',
            'formatter': 'verbose',
            'backupCount': 5,
            'maxBytes': 10000000,
            'encoding': 'utf-8',
        },
        'opcua_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './opcua.log',
            'formatter': 'verbose',
            'backupCount': 5,
            'maxBytes': 10000000,
            'encoding': 'utf-8',
        },
        'background_lib_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './asyncua.log',
            'formatter': 'verbose',
            'backupCount': 5,
            'maxBytes': 10000000,
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'root': {
            'handlers': ('root_file_handler',),
            'level': logging.INFO,
            'propagate': False,
        },
        'formic_opcua': {
            'handlers': ('opcua_file_handler',),
            'level': logging.WARNING,
            'propagate': False,
        },
        'asyncua': {
            'handlers': ('background_lib_file_handler',),
            'level': logging.INFO,
            'propagate': False,
        },
    },
}

logging.config.dictConfig(LOG_CONFIG)


def main() -> None:
    config_file_name = './example_configs/opcua_config_1.yaml'
    with OpcuaClient(server_config_file=config_file_name, connect_timeout=0.25) as client:
        for i in range(10):
            client.write(
                path='formic/device_type/PLC/device/SYS1_PLC1/connection/connection_status',
                value=i,
            )
            # client.write(
            #     path='formic/device_type/PLC/device/SYS1_PLC1/states/critical_system_statuses/level_1_errors',
            #     value=i,
            # )
            # client.read(
            #     path='formic/device_type/PLC/device/SYS1_PLC1/states/critical_system_statuses/level_1_errors',
            # )
            # all_variables = client.read_all()
            # print(all_variables)
            # print(i)
            time.sleep(2)


if __name__ == '__main__':
    main()
