import pickle
import os
import os.path
import time
import glob


class Save:
    def __init__(self, p=None, blanc=None, noir=None, blanc_a_main=True,
                 max_histo=5):
        self.crea = time.time()
        self.date = self.crea
        self.p = p
        self.blanc = blanc
        self.noir = noir
        self.blanc_a_main = blanc_a_main
        self.histo = []
        self.max_histo = max_histo


class SavesManager:
    def __init__(self, folder):
        self.saveFolder = os.path.join(os.path.realpath(os.path.dirname(__file__)), folder)

    def getSaves(self):
        saves = []
        for file in glob.iglob(os.path.join(self.saveFolder, "*.chessSave")):
            file = os.path.basename(file)
            if file.endswith(".chessSave"):
                file = os.path.splitext(file)[0]
                saves.append((file, self.getSave(file)))
        saves.sort(key=lambda x: x[1].date, reverse=True)
        return saves

    def getSave(self, filename):
        try:
            with open(os.path.join(self.saveFolder, filename + ".chessSave"), "rb") as file:
                save = pickle.load(file)
        except os.error:
            raise Exception("Invalid file")
        else:
            return save

    def save(self, save, filename):
        if isinstance(save, Save):
            save.date = time.time()
            path = os.path.join(self.saveFolder, filename + ".chessSave")
            with open(path, "wb") as file:
                pickle.dump(save, file)
        else:
            raise TypeError("save is not a chess save instance")
