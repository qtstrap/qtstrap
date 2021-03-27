from qtstrap import *
from main_window import MainWindow


"""
application.py



"""


class Application(BaseApplication):
    # replace these with your own information
    # setting these values at the application level makes it easier to use QSettings later on
    organization_name = 'ExampleCo'
    organization_domain = 'ExampleCo'
    application_name = 'Your Application'
    application_version = '0.1'
    
    def __init__(self) -> None:
        super().__init__()

        # create window
        self.window = MainWindow()
        self.window.show()