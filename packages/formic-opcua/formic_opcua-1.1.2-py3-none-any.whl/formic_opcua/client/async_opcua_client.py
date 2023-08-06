# Copyright Formic Technologies 2023
import logging
import posixpath
from typing import Any, Dict, List

from asyncua import Client
from asyncua.ua.uatypes import VariantType

from formic_opcua.core import convert_type, parse_settings

logger = logging.getLogger(__name__)


class AsyncOpcuaClient:
    def __init__(self, server_config_file: str) -> None:
        logger.debug('Configuring client.')
        self._server_config_file = server_config_file
        self.config = parse_settings(self._server_config_file)
        self._client_map: Dict[str, tuple] = dict()
        self._url = self.config['server_settings']['url']
        self._uri = self.config['server_settings']['uri']
        self._idx = -1
        self._client = Client(url=self._url)
        logger.info(f'Client created with url: {self._url}, and uri: {self._uri}')

    async def connect(self) -> None:
        try:
            await self._client.connect()
        except ConnectionRefusedError as e:
            logger.error(
                f'Unable to connect to server. Client expects server to have url: {self._url} and uri: {self._uri}. '
                f'Server is not running or the configs are not matched with client.'
            )
            raise e

        logger.info('Client connected to server.')
        self._idx = await self._client.get_namespace_index(self._uri)
        logger.info(f'Namespace index = {self._idx}')
        logger.info(f'Mapping namespace using {self._server_config_file}')
        try:
            for child_name, root in self.config['opcua_nodes'].items():
                await self._map_client(child_name, root)
        except Exception as e:
            logger.error(f'Unable to map opcua nodes from {self._server_config_file}: {e}')
            raise e

    async def _map_client(self, parent_path: str, root: dict) -> None:
        if self._is_leaf(root):
            identifier = self.identifier_from_string(parent_path)
            var = await self._client.nodes.root.get_child(identifier)
            self._client_map[parent_path] = (var, getattr(VariantType, root['type']))
            return None

        original_parent_path_length = len(parent_path)

        for child_root_name, child_root in root.items():
            parent_path = posixpath.join(parent_path, child_root_name)
            if original_parent_path_length == 0:
                parent_path = parent_path[1:]

            await self._map_client(parent_path, child_root)
            parent_path = parent_path[:original_parent_path_length]

    def identifier_from_string(self, path: str) -> List[str]:
        identifier = [f'{self._idx}:{path_part}' for path_part in path.split('/')]
        return ['0:Objects'] + identifier

    async def write(self, path: str, value: Any) -> None:
        logger.info(f'Writing {value} to {path}')
        try:
            var, var_type = self._client_map[path]
            value = convert_type(value=value, var_type=var_type)
            await var.write_value(value, var_type)
        except KeyError as ke:
            logger.error(f'{ke} does not exist in client map: {self._client_map}')
        except ConnectionError as e:
            logger.error(f'Unable to write {value} to {path}: {e}')

    async def read(self):
        return {path: await node.read_value() for path, (node, var_type) in self._client_map.items()}

    @staticmethod
    def _is_leaf(root: dict) -> bool:
        if 'initial_value' in root:
            return True
        return False

    async def disconnect(self) -> None:
        logger.info('Cleaning up client.')
        await self._client.disconnect()
