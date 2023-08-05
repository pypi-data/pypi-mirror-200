from __future__ import annotations

import abc
import json
from dataclasses import dataclass
from typing import TypeVar

from bigeye_sdk.functions.aws import get_secret

from bigeye_sdk.log import get_logger

log = get_logger(__file__)


class Credential(abc.ABC):
    pass


CREDENTIAL = TypeVar('CREDENTIAL', bound='Credential')


class LocalFileCredential(Credential):

    @classmethod
    def load_from_file(cls, file: str) -> CREDENTIAL:
        log.info(f'Loading API Conf: {file}')
        with open(file) as fin:
            return cls(**json.load(fin))


class AwsSecretCredential(Credential):

    @classmethod
    def load_from_aws_secret(cls, secret_name: str, region_name: str = 'us-west-2') -> CREDENTIAL:
        log.info(f'Loading Secret: {secret_name}')
        return cls(**get_secret(region_name=region_name, secret_name=secret_name))


class LoadableCredential(LocalFileCredential, AwsSecretCredential):
    pass


class DatabaseCredential(LoadableCredential):
    @abc.abstractmethod
    def get_sqlalchemy_conn_str(self, database: str = None) -> str:
        pass


@dataclass
class AwsCredential(LoadableCredential):
    aws_key: str
    aws_secret_key: str


@dataclass
class PostgresCredential(DatabaseCredential):
    username: str
    password: str
    host: str
    port: int = 5432

    def get_sqlalchemy_conn_str(self, database: str = None) -> str:
        url = f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}"
        if database:
            url = f'{url}/{database}'
        return url


@dataclass
class SnowflakeCredential(DatabaseCredential):
    username: str
    password: str
    account_identifier: str

    def get_sqlalchemy_conn_str(self, warehouse: str = None, role: str = None, database: str = None) -> str:
        if database:
            return f'snowflake://{self.username}:{self.password}@{self.account_identifier}/{database}'
        else:
            return f'snowflake://{self.username}:{self.password}@{self.account_identifier}'
