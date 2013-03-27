import pickle 
import joueur
import os.path, os.error

class ProfilesLoader:
    def __init__(self, filename):
        self.filename = filename
        self.profiles = None
        self.lastUpdate = 0
    
    def saveProfiles(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self.profiles, file, pickle.HIGHEST_PROTOCOL)

    def getProfiles(self):
        try:
            if self.lastUpdate < os.path.getmtime(self.filename):
                self.loadProfiles()
        except os.error: # Si le fichier de profiles n'existe pas
            self.profiles = None
        return self.profiles
    
    def saveProfile(self, joueur):
        self.profiles[joueur.nom] = joueur
        self.saveProfiles()
    
    def loadProfiles(self):
        with open(self.filename, "rb") as file:
            self.profiles = pickle.load(file)