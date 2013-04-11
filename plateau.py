"""Fichier contenant la logique du plateau"""
import pieces

class Plateau():
    """Décrit le plateau de jeu"""
    
    def __init__(self):
        """Construction du plateau"""
        self.t = [[None for j in range(8)] for i in range(8)]

    def setup(self, blanc, noir):
        """Initialisation du plateau avec les pièces placées"""
        self.joueurBlanc = blanc
        self.joueurNoir = noir
        self.t[0][0] = pieces.Tour(self, blanc, 0, 0)
        self.t[0][7] = pieces.Tour(self, blanc, 0, 7)
        self.t[0][1] = pieces.Cavalier(self, blanc, 0, 1)
        self.t[0][6] = pieces.Cavalier(self, blanc, 0, 6)
        self.t[0][2] = pieces.Fou(self, blanc, 0, 2)
        self.t[0][5] = pieces.Fou(self, blanc, 0, 5)
        self.t[0][3] = pieces.Roi(self, blanc, 0, 3)
        self.t[0][4] = pieces.Dame(self, blanc, 0, 4)
        self.t[7][0] = pieces.Tour(self, noir, 7, 0)
        self.t[7][7] = pieces.Tour(self, noir, 7, 7)
        self.t[7][1] = pieces.Cavalier(self, noir, 7, 1)
        self.t[7][6] = pieces.Cavalier(self, noir, 7, 6)
        self.t[7][2] = pieces.Fou(self, noir, 7, 2)
        self.t[7][5] = pieces.Fou(self, noir, 7, 5)
        self.t[7][3] = pieces.Roi(self, noir, 7, 3)
        self.t[7][4] = pieces.Dame(self, noir, 7, 4)
        for i in range(8):
            self.t[1][i] = pieces.Pion(self, blanc, 1, i)
            self.t[6][i] = pieces.Pion(self, noir, 6, i)

    def getJoueurNoir(self):
        return self.joueurNoir
    
    def getJoueurBlanc(self):
        return self.joueurBlanc

    def getPiece(self, x, y):
        return self.t[x][y]

    def setPiece(self, piece, x, y):
        piece.updateCoord(x, y)
        self.t[x][y] = piece

    def delPiece(self, x, y):
        self.t[x][y] = None

    def bougerPiece(self, joueur, xd, yd, xa, ya):
        piece = self.getPiece(xd, yd)
        if piece is not None:
            if piece.get_joueur() is joueur:
                if piece.peutBouger(xa, ya):
                    self.setPiece(piece, xa, ya)
                    self.delPiece(xd, yd)
                else:
                    raise Exception("Mouvement non autorisé")
            else:
                raise Exception("Cette pièce ne vous appartient pas")
        else:
            raise Exception("Cette pièce n'existe pas")

