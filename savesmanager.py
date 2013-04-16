import pickle
import os
import os.path
import time

class Save:
    def __init__(self, p=None, blanc=None, noir=None, blanc_a_main=True,
                 max_histo=5):
        self.date = time.time()
        self.p = p
        self.blanc = blanc
        self.noir = noir
        self.blanc_a_main = blanc_a_main
        self.histo = []
        self.max_histo = max_histo

class SavesManager:
    def __init__(self, folder):
        self.saveFolder = os.path.realpath(os.path.dirname(__file__))
    
    def getSaves(self):
        pass
    
    def getSave(self, filename):
        try:
            save = pickle.load(os.path.join(self.saveFolder, filename+".chessSave"))
        except os.error:
            raise Exception("Invalid file")
        else:
            return save
    
    def save(self, save, filename):
        if isinstance(save, Save):
            save.date = time.time()
            pickle.dump(os.path.join(self.saveFolder, filename+".chessSave"),
                        save)
        else:
            raise TypeError("save is not a chess save instance")