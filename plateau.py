"""Fichier contenant la logique du plateau"""
import pieces
import copy
from echecexception import EchecException


class Plateau():
    """Décrit le plateau de jeu"""

    def __init__(self):
        """Construction du plateau"""
        self.t = [[None for j in range(8)] for i in range(8)]
        self.roi = {}
        self.joueurBlanc = None
        self.joueurNoir = None

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
        self.t[0][4] = pieces.Roi(self, blanc, 0, 4)
        self.t[0][3] = pieces.Dame(self, blanc, 0, 3)
        self.t[7][0] = pieces.Tour(self, noir, 7, 0)
        self.t[7][7] = pieces.Tour(self, noir, 7, 7)
        self.t[7][1] = pieces.Cavalier(self, noir, 7, 1)
        self.t[7][6] = pieces.Cavalier(self, noir, 7, 6)
        self.t[7][2] = pieces.Fou(self, noir, 7, 2)
        self.t[7][5] = pieces.Fou(self, noir, 7, 5)
        self.t[7][4] = pieces.Roi(self, noir, 7, 4)
        self.t[7][3] = pieces.Dame(self, noir, 7, 3)
        for i in range(8):
            self.t[1][i] = pieces.Pion(self, blanc, 1, i)
            self.t[6][i] = pieces.Pion(self, noir, 6, i)
        self.roi[noir] = self.t[7][4]
        self.roi[blanc] = self.t[0][4]

    def getJoueurNoir(self):
        return self.joueurNoir

    def getJoueurBlanc(self):
        return self.joueurBlanc

    def getRoi(self, joueur):
        try:
            return self.roi[joueur]
        except:
            raise Exception("Joueur invalide")

    def getPiece(self, line, col):
        return self.t[line][col]

    def setPiece(self, piece, line, col):
        piece.updateCoord(line, col)
        self.t[line][col] = piece

    def delPiece(self, line, col):
        self.t[line][col] = None

    def bougerPiece(self, joueur, line_d, col_d, line_a, col_a, faked=False):
        piece = self.getPiece(line_d, col_d)
        if piece is not None:
            if piece.getJoueur() is joueur:
                if piece.peutBouger(line_a, col_a):
                    rollback = [[None for i in range(8)] for j in range(8)]
                    for i in range(8):
                        for j in range(8):
                            rollback[i][j] = copy.copy(self.t[i][j])
                    self.setPiece(piece, line_a, col_a)
                    self.delPiece(line_d, col_d)
                    if self.echec(joueur):
                        self.t = rollback
                        raise EchecException("Ce mouvement vous place en échec")
                    if faked:
                        self.t = rollback
                elif piece is self.getRoi(joueur) and (col_a == 1 or col_a == 5):
                    sens = (col_a - col_d) // abs(col_a - col_d)
                    try:
                        self.roquer(joueur, sens)
                    except Exception:
                        raise EchecException("Mouvement non autorisé")
                else:
                    raise EchecException("Mouvement non autorisé")
            else:
                raise EchecException("Cette pièce ne vous appartient pas")
        else:
            raise EchecException("Cette pièce n'existe pas")

    def roquer(self, joueur, sens):
        piece = self.getRoi(joueur)
        line_d = piece.line
        col_d = piece.col
        if sens == 1:
            col_t = 7
            col_a = 6
        else:
            sens == -1
            col_t = 0
            col_a = 2
        if piece.peutRoquer(sens):
            tour = self.getPiece(line_d, col_t)
            self.setPiece(piece, piece.line, col_a)
            self.setPiece(tour, piece.line, col_a - sens)
            self.delPiece(line_d, col_d)
            self.delPiece(line_d, col_t)
        else:
            raise EchecException("Roque impossible")

    def echec(self, joueur, line=None, col=None):
            if line is None:
                line = self.getRoi(joueur).line
            if col is None:
                col = self.getRoi(joueur).col
            for row in self.t:
                for piece in row:
                    if piece is not None:
                        if piece.getJoueur() is not joueur:
                            if piece.peutBouger(line, col):
                                return True
            return False

    def echec_et_mat(self, joueur, line=None, col=None):
        if line is None:
            line = self.getRoi(joueur).line
        if col is None:
            col = self.getRoi(joueur).col
        for row in self.t:
            for piece in row:
                if piece is not None and piece.getJoueur() is joueur:
                    for i in range(8):
                        for j in range(8):
                            try:
                                self.bougerPiece(joueur, piece.line, piece.col, i, j, True)
                            except EchecException:
                                pass
                            else:
                                return False
        return True
