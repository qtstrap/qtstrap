from qtstrap import *
from main_window import MainWindow


"""
application.py

TODO: explain this

"""


class Application(BaseApplication):
    organization_name = '$publisher'
    organization_domain = '$publisher'
    application_name = '$appname'
    application_version = '$version'
    
    def __init__(self) -> None:
        super().__init__()

        # create window
        self.window = MainWindow()
        self.window.show()