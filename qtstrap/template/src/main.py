#!/usr/bin/env python3


from application import Application


def run():    
    # Create the Qt Application
    app = Application()

    # Run the main Qt loop
    app.exec_()


if __name__ == "__main__":
    run()