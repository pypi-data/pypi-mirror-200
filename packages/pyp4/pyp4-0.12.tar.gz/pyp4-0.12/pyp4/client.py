import re

from P4 import P4, P4Exception


class Client(P4):
    # The mode of add api4p4 mapping
    #                       w: overwrite
    #                       a: append write
    # DEFAULT_VIEW_MODE:    w: overwrite
    DEFAULT_VIEW_MODE = OVERWRITE_VIEW = "w"
    APPEND_VIEW = "a"
    VIEW_MODE = [OVERWRITE_VIEW, APPEND_VIEW]

    OPTIONS_LIST = ["allwrite", "clobber", "compress", "locked", "modtime", "rmdir"]
    P4_OPTIONS = "noallwrite noclobber nocompress unlocked nomodtime normdir"

    def __init__(self, logger=None, multiple=False, exception_level=1, **kwargs):
        """
        :param: multiple: invoke this prior to connecting if you need to use multiple P4 connections in parallel in a multi-threaded Python application.
        :param: port: api4p4 server, example api4p4.com:2002
        :param: user: user name
        :param: password: user password
        :param: charset: api4p4 character set, must be one of:
                none, auto, utf8, utf8-bom, iso8859-1, shiftjis, eucjp, iso8859-15,
                iso8859-5, macosroman, winansi, koi8-r, cp949, cp1251,
                utf16, utf16-nobom, utf16le, utf16le-bom, utf16be,
                utf16be-bom, utf32, utf32-nobom, utf32le, utf32le-bom, utf32be,
                cp936, cp950, cp850, cp858, cp1253, iso8859-7, utf32be-bom,
                cp852, cp1250, iso8859-2
        :param: encoding: When decoding strings from a non-Unicode server, strings are assumed to be encoded in UTF8.
                To use another encoding, set p4.encoding to a legal Python encoding, or raw to receive Python bytes instead of a Unicode string.
                Available only when compiled with Python 3.
        ...
        """
        self.client = ""
        self.password = kwargs.get("password")
        super().__init__(**kwargs)
        if multiple:
            self.disable_tmp_cleanup()
        if logger:
            self.logger = logger

        self.exception_level = exception_level

    def modify_workspace(self, workspace_name, owner=None, host=None, root=None, options=None, submit_options="submitunchanged", view=None, mode=DEFAULT_VIEW_MODE):
        if mode not in Client.VIEW_MODE:
            raise P4Exception(f"invalid mode of add api4p4 mapping: `{mode}`")

        options = options or []
        for options in options:
            if options not in Client.OPTIONS_LIST:
                raise P4Exception(f"invalid option for p4_options: `{options}`")

            Client.P4_OPTIONS = re.sub(re.compile(rf"(un|no){options}", re.S), options, Client.P4_OPTIONS)

        self.client = workspace_name
        workspace = self.fetch_client(workspace_name)
        if owner is not None:
            workspace["Owner"] = owner
        if host is not None:
            workspace["Host"] = host
        if root is not None:
            workspace["Root"] = root
        if options is not None:
            workspace["Options"] = Client.P4_OPTIONS
        if submit_options is not None:
            workspace["SubmitOptions"] = submit_options
        if view is not None:
            if mode == Client.OVERWRITE_VIEW:
                workspace["View"] = view
            elif mode == Client.APPEND_VIEW:
                workspace["View"] += view

        self.save_client(workspace)
        return self

    @property
    def name(self):
        if not self.client:
            raise P4Exception("workspace has not been set up")

        return self.client

    @property
    def view(self):
        return self.fetch_client(self.client).get("View", [])

    def set_view(self, view_list: list):
        self.modify_workspace(workspace_name=self.name, view=view_list, mode=Client.OVERWRITE_VIEW)

    def add_view(self, view_list: list):
        self.modify_workspace(workspace_name=self.name, view=view_list, mode=Client.APPEND_VIEW)
