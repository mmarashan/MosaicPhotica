from abc import ABC


class View(ABC):

    def inject(self, presenter):
        pass

    def start(self):
        pass

