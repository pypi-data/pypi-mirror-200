import logging

from pyp4.pyp4 import PyP4


class LoggerHandler(logging.Logger):

    def __init__(self, name='root', level=logging.INFO, fm=None):
        super().__init__(name)

        self.setLevel(level)
        fmt = logging.Formatter(fm)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(fmt)
        self.addHandler(stream_handler)


log = LoggerHandler(
    name="test",
    level=logging.INFO,
    fm='%(asctime)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s'
)

if __name__ == '__main__':
    workspace_config = {
        "workspace_name": "172_test_niushuaibing",
        # "owner": "admin",
        # "host": "",
        # "description": "Created by admin.\n",
        # "root": r"D:\workspace\niushuaibin",
        "options": [
            "clobber",
            "rmdir"
        ],
        # "submit_options": "submitunchanged",
        # "view": [
        #     "//depot/test/... //test_workspace/test/..."
        # ]
    }
    pyp4 = PyP4(port="x5_mobile.p4.com:1666", auth=("niushuaibing", "NSB1hblsqt."), logger=log)
    res = pyp4.workspace_exists("172_test_niushuaibing")
    print(res)
    # workspace = pyp4.set_workspace(**workspace_config)

    # wp = session.switch_workspace("x5_mobile_niu")
    # sync_result = wp.run_sync("-f", "//x5mplan/resmg/ui/cdn-texture-base.xlsx")
    # wp.set_view(["//x5mplan/resmg/ui/... //x5_mobile_niu/x5mplan/resmg/ui/..."])
    # print(workspace.view)
    # checkout_files = p4_client.run_opened("-a", "//...")
    pyp4.client.disconnect()
