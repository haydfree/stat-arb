from UI import UI
from ObjectFactory import ObjectFactory


class Main:
    def __init__(self):
        self.run()

    @staticmethod
    def run() -> None:
        objectFactory: ObjectFactory = ObjectFactory(name="of1")
        ui: UI = UI(objectFactory=objectFactory)


if __name__ == '__main__':
    Main.run()
