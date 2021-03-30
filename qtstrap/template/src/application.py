from qtstrap import *
from main_window import MainWindow


class Application(BaseApplication):
    organization_name = '$publisher'
    organization_domain = '$publisher'
    application_name = '$appname'
    application_version = '$version'
    
    def __init__(self) -> None:
        super().__init__()

        self.window = MainWindow() # create window
        self.window.show()