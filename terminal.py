from plateau import Plateau
from profilesmanager import ProfilesManager
from savesmanager import SavesManager
from joueur import Joueur
import useraction
import re
from utils import reverse_range, safe_input


class Terminal():
    def __init__(self):
        self.coupValide = re.compile(r"(?P<c_d>[a-h])(?P<l_d>[1-8]) (?P<c_a>[a-h])(?P<l_a>[1-8])")
        self.profilesManager = ProfilesManager("profiles.chess")
        self.savesManager = SavesManager("saves/")

    def afficher_plateau(self, p, main, blanc):
        """Affiche le plateau, le joueur qui a la main est en bas

        Le joueur blanc sert de référence à l'affichage"""
        if main is not blanc:
            reverse = False
        else:
            reverse = True
        entete = [chr(i) for i in
            reverse_range(not reverse, ord('A'), ord('H')+1)]
        print("    ", end="")  # padding
        print(*entete, sep=" "*3)
        print("  \u2554", "\u2550\u2550\u2550\u2564"*7,
                      "\u2550\u2550\u2550\u2557", sep="")
        for i in reverse_range(reverse, 8):
            left = True
            for j in reverse_range(not reverse, 8):
                if left:
                    print(i + 1, "\u2551", end=" ")
                    left = False
                else:
                    print("\u2502", end=" ")
                if p.getPiece(i, j) is not None:
                    joueur = p.getPiece(i,j).getJoueur()
                    piece = p.getPiece(i,j).getRepres()
                    if joueur is blanc:
                        print(piece.upper(), end=" ")
                    else:
                        print(piece, end=" ")
                else:
                    print(" ", end=" ")
            print("\u2551", i+1)
            if i == 7 and not reverse or i == 0 and reverse:
                print("  \u255A", "\u2550\u2550\u2550\u2567"*7,
                      "\u2550\u2550\u2550\u255D", sep="")
            else:
                print("  \u255F", "\u2500\u2500\u2500\u253C"*7,
                  "\u2500\u2500\u2500\u2562", sep="")
        print("    ", end="") # padding
        print(*entete, sep=" "*3)

    def selectProfile(self, nom, taken=[]):
        profiles = self.profilesManager.getProfiles()
        takennoms = [profile.nom for profile in taken]
        profiles = [profile for profile in profiles.values()
                if profile.nom not in takennoms]
        print("Joueur ", nom, ", sélectionnez votre profil.", sep="")
        i = 1
        for profile in profiles:
            print(i,": ", profile.nom, " (elo: ", profile.elo, ")", sep="")
            i += 1
        print("n: Nouveau profil")
        run = True
        while run:
            entree = safe_input(">>> ", str)
            try:
                entree = int(entree)
            except ValueError:
                if entree.startswith("n"):
                    choisi = self.nouveauProfil()
                    run = False
            else:
                if entree >= 1 and entree <= i-1:
                    choisi = profiles[entree-1]
                    run = False
            if run:
                print("Entrée non valide")
        return choisi

    def nouveauProfil(self):
        """Dessine l'interface de création de nouveau profil"""
        run = True
        profiles = self.profilesManager.getProfiles()
        while run:
            nom = safe_input("Entrez le nom du profil : ", str)
            if not nom in profiles.keys():
                joueur = Joueur(nom, 1200)  # Classement ELO niveau débutant
                run = False
            else:
                print("Un profil porte déjà ce nom. \
                        Veuillez en utilisez un autre.")
            print("Si vous possèdez un score ELO, veuillez l'indiquer, \
                    sinon, laissez le champ vide")
            run = True
            while run:
                entree = input("Votre score ELO (1200) :")
                try:
                    joueur.elo = int(entree)
                except:
                    if(entree == ""):
                        run = False
                    else:
                        print("Veuillez entrer un score entier.")
                else:
                    run = False
            self.profilesManager.saveProfile(joueur)
            return joueur


    def start(self):
        """Démarrer l'interface"""
        run = True
        print("Bienvenue dans le jeu d'échec de Loïc Labache et Paul Ecoffet")
        while run:
            print("Que souhaitez-vous faire ? [N]ouvelle partie,"+
                  "[c]harger une partie, [q]uitter")
            entree = safe_input(">>> ", str).lower()
            if entree.startswith('c'):
                save = self.loadGame()
                self.afficher_historique(save)
                self.startGame(save.p, save.blanc, save.noir, 
                               save.blanc_a_main)
            elif entree.startswith('q'):
                run = False
            else:
                self.startGame()
        print("Merci d'avoir joué")

    def ask(self, joueur):
        """Demande au joueur d'entrer son coup et le convertit
en coordonnées"""
        action = useraction.UserAction(useraction.INVALID)
        entree = safe_input(joueur.nom +", entrez votre coup: ", str).lower()
        m = self.coupValide.match(entree)
        if m is not None:
            action.action = useraction.MOVE
            action.data["dep"] = (int(m.group("l_d"))-1,
                                  ord(m.group("c_d")) - ord('a'))
            action.data["arr"] = (int(m.group("l_a"))-1,
                                  ord(m.group("c_a")) - ord('a'))
        elif entree == "roque" or entree == "0-0":
            action.action = useraction.ROQUE
            action.data["sens"] = -1
        elif entree == "groque" or entree == "0-0-0":
            action.action = useraction.ROQUE
            action.data["sens"] = 1
        elif entree == "exit":
            action.action = useraction.EXIT
        elif entree == "save":
            action.action = useraction.SAVE
        return action

    def startGame(self, p=Plateau(), blanc=None, noir=None, blanc_a_main=True):
        """Démarre une nouvelle partie"""
        if blanc is None and noir is None:
            blanc = self.selectProfile("blanc")
            noir = self.selectProfile("noir", [blanc])
        p.setup(blanc, noir)
        gagnant = None
        stop = False
        if blanc_a_main:
            main = blanc
        else:
            main = noir
        while gagnant is None and not stop:
            self.afficher_plateau(p, main, blanc)
            passer_main = False
            while not passer_main:
                action = self.ask(main)
                if action.action == useraction.MOVE:
                    try:
                        p.bougerPiece(main, action.data["dep"][0], 
                            action.data["dep"][1], action.data["arr"][0],
                            action.data["arr"][1])
                    except Exception as e:
                        print(e)
                    else:
                        passer_main = True
                elif action.action == useraction.ROQUE:
                    try:
                        p.roquer(main, action.data["sens"])
                    except Exception as e:
                        print(e)
                    else:
                        passer_main = True
                elif action.action == useraction.EXIT:
                    passer_main = True
                    stop = True
            if main == blanc:
                main = noir
            else:
                main = blanc
        return gagnant