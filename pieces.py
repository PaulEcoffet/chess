from utils import smart_range


class Piece:
    def __init__(self, plateau, joueur, line, col):
        self.joueur = joueur
        self.p = plateau
        self.line = line
        self.col = col
        self.moves = 0

    def updateCoord(self, line, col):
        self.line = line
        self.col = col
        self.moves += 1

    def getRepres(self):
        try:
            return self.repres
        except:
            raise NotImplementedError("Abstract method")

    def getPos(self):
        return self.line, self.col

    def getJoueur(self):
        return self.joueur

    def peutBouger(self, line_a, col_a):
        raise NotImplementedError("Abstract method")

    def peutRoquer(self, line_a, col_a):
        return False


class Pion(Piece):
    def __init__(self, plateau, joueur, line, col):
        super().__init__(plateau, joueur, line, col)
        self.repres = "p"

    def peutBouger(self, line_a, col_a):
        if self.joueur is self.p.getJoueurNoir():
            sens = -1
        else:
            sens = 1
        return self._avance(line_a, col_a, sens) or self._mange(line_a, col_a, sens)

    def _avance(self, line_a, col_a, sens):
        if (self.col == col_a and self.line + sens == line_a and
                self.p.getPiece(line_a, col_a) is None):
            return True
        elif (self.moves == 0 and self.col == col_a and self.line + sens * 2 == line_a and
                self.p.getPiece(line_a, col_a) is None and
                self.p.getPiece(line_a - sens, col_a) is None):
            return True
        else:
            return False

    def _mange(self, line_a, col_a, sens):
        if (abs(self.col - col_a) == 1 and self.line + sens == line_a):
            piece = self.p.getPiece(line_a, col_a)
            if (piece is not None and
                    piece.getJoueur() is not self.getJoueur()):
                return True
        return False


class Tour(Piece):
    def __init__(self, plateau, joueur, line, col):
        super().__init__(plateau, joueur, line, col)
        self.repres = "t"

    def peutBouger(self, line_a, col_a):
        if self.p.getPiece(line_a, col_a) is not None:
            if self.p.getPiece(line_a, col_a).getJoueur() is self.joueur:
                return False
        if self.line == line_a and self.col != col_a:
            sens = (col_a - self.col) // abs(col_a - self.col)
            for i in range(self.col + sens, col_a, sens):
                if self.p.getPiece(self.line, i) is not None:
                    return False
            return True
        elif self.line != line_a and self.col == col_a:
            sens = (line_a - self.line) // abs(line_a - self.line)
            for i in range(self.line + sens, line_a, sens):
                if self.p.getPiece(i, self.col) is not None:
                    return False
            return True
        else:
            return False


class Cavalier(Piece):
    def __init__(self, plateau, joueur, line, col):
        super().__init__(plateau, joueur, line, col)
        self.repres = "c"

    def peutBouger(self, line_a, col_a):
        movement = [(2, 1), (2, -1), (1, -2), (1, 2), (-2, -1), (-2, 1),
                    (-1, -2), (-1, +2)]
        if self.p.getPiece(line_a, col_a) is not None:
            if self.p.getPiece(line_a, col_a).getJoueur() is self.joueur:
                return False
        for x_m, y_m in movement:
            if self.line + x_m == line_a and self.col + y_m == col_a:
                return True
        return False


class Fou(Piece):
    def __init__(self, plateau, joueur, line, col):
        super().__init__(plateau, joueur, line, col)
        self.repres = "f"

    def peutBouger(self, line_a, col_a):
        if self.p.getPiece(line_a, col_a) is not None:
            if self.p.getPiece(line_a, col_a).getJoueur() is self.joueur:
                return False
        if abs(col_a - self.col) / abs(line_a - self.line) == 1:
            sens_c = (col_a - self.col) // abs(col_a - self.col)
            sens_l = (line_a - self.line) // abs(line_a - self.line)
            for i in range(1, abs(line_a - self.line), 1):
                if self.p.getPiece(self.line + i * sens_l,
                                   self.col + i * sens_c) is not None:
                    return False
            return True
        else:
            return False


class Dame(Piece):
    def __init__(self, plateau, joueur, line, col):
        super().__init__(plateau, joueur, line, col)
        self.repres = "d"

    def peutBouger(self, line_a, col_a):
        return Tour.peutBouger(self, line_a, col_a) or Fou.peutBouger(self, line_a, col_a)


class Roi(Piece):
    def __init__(self, plateau, joueur, line, col):
        super().__init__(plateau, joueur, line, col)
        self.repres = "r"

    def peutBouger(self, line_a, col_a):
        mouvement = [(line, col) for line in range(-1, 2) for col in range(-1, 2)
                     if not (col == 0 and line == 0)]
        if self.p.getPiece(line_a, col_a) is not None:
            if self.p.getPiece(line_a, col_a).getJoueur() is self.joueur:
                return False
        for (xm, ym) in mouvement:
            if self.line + xm == line_a and self.col + ym == col_a:
                return True
        return False

    def peutRoquer(self, sens):
        if sens == 1:
            col_t = 7
            col_a = 6
        else:
            sens = -1
            col_t = 0
            col_a = 2
        tour = self.p.getPiece(self.line, col_t)
        if isinstance(tour, Tour):
            if self.moves == 0 and tour.moves == 0:
                for col in smart_range(self.col, col_a + sens):
                    if self.p.getPiece(self.line, col) is not None or self.p.echec(self.joueur, self.line, col):
                        return False
                    return True
        return False
