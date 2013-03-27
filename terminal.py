from plateau import Plateau
from profilesloader import ProfilesLoader

def reverse_range(reverse, start, stop=None, step=1):
    if stop is None:
        stop = start
        start = 0
    if reverse:
        step = -step
        start, stop = stop-1, start-1
    return range(start, stop, step)

class Terminal():
    def __init__(self):
        self.p = None
        self.profileloader = ProfilesLoader("profiles.chess")

    def afficher_plateau(self, main):
        """Affiche le plateau, le joueur qui a la main est en bas"""
        if main == 1:
            reverse = False
        else:
            reverse = True
        entete = [chr(i) for i in 
            reverse_range(not reverse, ord('A'), ord('H')+1)]
        print("  ", end="") # padding
        print(*entete, sep=" "*3)
        print("\u2554", "\u2550\u2550\u2550\u2564"*7,
                      "\u2550\u2550\u2550\u2557", sep="")
        for i in reverse_range(reverse, 8):
            left = True
            for j in reverse_range(not reverse, 8):
                if left:
                    print("\u2551", end=" ")
                    left = False
                else:
                    print("\u2502", end=" ")
                if self.p.getPiece(i,j) is not None:
                    joueur = self.p.getPiece(i,j).get_joueur()
                    piece = self.p.getPiece(i,j).get_repres()
                    if joueur == 1:
                        print(piece.upper(), end=" ")
                    else:
                        print(piece, end=" ")
                else:
                    print(" ", end=" ")
            print("\u2551", i+1)
            if i == 7 and not reverse or i == 0 and reverse:
                print("\u255A", "\u2550\u2550\u2550\u2567"*7,
                      "\u2550\u2550\u2550\u255D", sep="")
            else:
                print("\u255F", "\u2500\u2500\u2500\u253C"*7,
                  "\u2500\u2500\u2500\u2562", sep="")
        print("  ", end="") # padding
        print(*entete, sep=" "*3)

    def selectProfile(self, nom, taken):
        profiles = self.profilesLoader.getProfiles()
        profiles = [profile for profile in profiles if profile not in taken]
        print("Joueur ", nom, ", sélectionnez votre profil.", sep="")
        i = 1
        for profile in profiles:
            print(i,": ", profile.nom, " (elo: ", profile.elo, ")", sep="")
            i += 1
        print("n: Nouveau profil")
        run = True
        while run:
            entree = input(">>> ")
            try:
                entree = int(entree)
            except ValueError:
                if entree[0] == "n":
                    choisi = self.nouveauProfil()
                    run = False
            else:
                if entree >= 1 and entree <= i-1:
                    choisi = profiles[entree-1]
                    run = False
            if run:
                print("Entrée non valide")

    def start(self):
        """Démarrer l'interface"""
        print("Bienvenue dans le jeu d'échec de Loïc Labache et Paul Ecoffet")
        blanc = self.selectProfile("blanc")
        noir = self.selectProfile("noir", [blanc])
        self.startGame(blanc, noir)

    def ask(self, joueur):
        """Demande au joueur d'entrer son coup et le convertit
en coordonnées"""
        # TODO: Vérifier entrée utilisateur
        entree = str(input("Entrez votre coup: "))
        dep, arr = entree.split(" ")
        piece = (int(dep[1])-1, ord(dep[0].lower()) - ord('a'))
        to = (int(arr[1])-1, ord(arr[0].lower()) - ord('a'))
        return (piece, to)

    def startGame(self, joueur1, joueur2):
        """Démarre une nouvelle partie"""
        self.p = Plateau()
        self.p.setup(joueur1, joueur2)
        gagnant = None
        main = joueur1
        while gagnant == None:
            self.afficher_plateau(main)
            run = True
            while run:
                piece, to = self.ask(main)
                try:
                    self.p.bougerPiece(main, piece[0], piece[1],
                                       to[0], to[1])
                except Exception as e:
                    print(e)
                else:
                    run = False
            if main == joueur1:
                main = joueur2
            else:
                main = joueur1
