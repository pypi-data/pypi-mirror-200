import os.path
from croydon.baseapp import BaseApp


class App(BaseApp):

    def __init__(self):
        app_dir = os.path.abspath(os.path.dirname(__file__))
        project_dir = os.path.abspath(os.path.join(app_dir, ".."))
        super().__init__(project_dir=project_dir)


app = App()
