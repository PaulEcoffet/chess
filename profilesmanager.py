import pickle
import os.path
import os


class ProfilesManager:
    def __init__(self, filename):
        self.filename = os.path.join(
            os.path.realpath(os.path.dirname(__file__)), filename)
        self.profiles = {}
        self.lastUpdate = 0

    def saveProfiles(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self.profiles, file, pickle.HIGHEST_PROTOCOL)

    def updateProfiles(self):
        try:
            if self.lastUpdate < os.path.getmtime(self.filename):
                self.loadProfiles()
        except os.error:  # Si le fichier de profiles n'existe pas
            self.profiles = {}
    
    def getProfiles(self):
        self.updateProfiles()
        return self.profiles
    
    def getProfileByName(self, name):
        self.updateProfiles()
        try:
            profil = self.profiles[name]
        except:
            raise Exception("Profil inexistant")
        return profil

    def saveProfile(self, joueur):
        self.profiles[joueur.nom] = joueur
        self.saveProfiles()

    def loadProfiles(self):
        with open(self.filename, "rb") as file:
            self.profiles = pickle.load(file)
