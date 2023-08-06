from enum import Enum
from P4 import P4Exception

from pyp4.client import Client


class ExceptionLevel(Enum):
    ignore_error = 0
    ignore_warning = 1
    not_ignore = 2


class PyP4:

    def __init__(self, port: str, auth: tuple = (), logger=None, exception_level=ExceptionLevel.ignore_warning, **kwargs):
        user, self.password = auth
        self.client = Client(
            logger=logger,
            port=port,
            user=user,
            password=self.password,
            exception_level=exception_level.value, **kwargs
        )
        self.connect()
        self.login()

    def connect(self):
        if not self.client.connected():
            self.client.connect()

    def login(self, password=None):
        if password:
            self.password = password

        self.client.run_login(password=self.password)

    def set_workspace(self, *args, **kwargs) -> Client:
        """
        {
            "workspace_name":"test_workspace",
            "owner":"admin",
            "host":"xxx",
            "description":"Created by admin.\n",
            "root":"D:\\workspace",
            "options":[
                "clobber"
            ],
            "submit_options":"submitunchanged",
            "view":[
                "//depot/test/... //test_workspace/test/..."
            ]
        }
        """
        return self.client.modify_workspace(*args, **kwargs)

    def switch_workspace(self, workspace_name: str) -> Client:
        if not self.client.exists(workspace_name):
            raise P4Exception(f"workspace `{workspace_name}` not exists")
        self.client.client = workspace_name
        return self.client

    def workspace_exists(self, workspace_name: str):
        return self.client.run_clients("-e", workspace_name)

    def disconnect(self):
        if self.client.connected():
            self.client.disconnect()
