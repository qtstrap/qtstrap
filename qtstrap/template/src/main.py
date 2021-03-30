from application import Application


def run():
    app = Application() # Create the Qt Application
    app.exec_() # Run the main Qt loop


if __name__ == "__main__":
    run()