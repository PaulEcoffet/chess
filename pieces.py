class Piece:
    def __init__(self, plateau, joueur, x, y):
        self.joueur = joueur
        self.plateau = plateau
        self.x = x
        self.y = y

    def updateCoord(self, x, y):
        self.x = x
        self.y = y

    def get_repres(self):
        try:
            return self.repres
        except:
            raise TypeError("Unimplemented method")

    def get_joueur(self):
        return self.joueur

    def peutBouger(self, x_a, y_a):
        pass


class Pion(Piece):
    def __init__(self, plateau, joueur, x, y):
        super().__init__(plateau, joueur, x, y)
        self.repres = "p"
        self.double = True
        self.a_double = False

    def peutBouger(self, x_a, y_a):
        if self.joueur is self.plateau.getJoueurNoir():
            sens = -1
        else:
            sens = 1
        if (self.y == y_a and self.x + sens == x_a and
                self.plateau.getPiece(x_a, y_a) is None):
            return True
        return False


class Tour(Piece):
    def __init__(self, plateau, joueur, x, y):
        super().__init__(plateau, joueur, x, y)
        self.repres = "t"

    def peutBouger(self, x_a, y_a):
        if self.plateau.getPiece(x_a, y_a) is not None:
            if self.plateau.getPiece(x_a, y_a).get_joueur() is self.joueur:
                return False
        if self.x == x_a and self.y != y_a:
            sens = (y_a - self.y) // abs(y_a - self.y)
            for i in range(self.y + sens, y_a, sens):
                if self.plateau.getPiece(self.x, i) is not None:
                    return False
            return True
        elif self.x != x_a and self.y == y_a:
            sens = (x_a - self.x) // abs(x_a - self.x)
            for i in range(self.x + sens, x_a, sens):
                if self.plateau.getPiece(i, self.y) is not None:
                    return False
            return True
        else:
            return False


class Cavalier(Piece):
    def __init__(self, plateau, joueur, x, y):
        super().__init__(plateau, joueur, x, y)
        self.repres = "c"

    def peutBouger(self, x_a, y_a):
        movement = [(2, 1), (2,-1), (1, -2), (1, 2), (-2, -1), (-2, 1),
                   (-1, -2), (-1, +2)]
        if self.plateau.getPiece(x_a, y_a) is not None:
            if self.plateau.getPiece(x_a, y_a).get_joueur() is self.joueur:
                return False
        for x_m,y_m in movement:
            if self.x + x_m == x_a and self.y + y_m == y_a :
                return True
        return False


class Fou(Piece):
    def __init__(self, plateau, joueur, x, y):
        super().__init__(plateau, joueur, x, y)
        self.repres = "f"

    def peutBouger(self, x_a, y_a):
        if self.plateau.getPiece(x_a, y_a) is not None:
            if self.plateau.getPiece(x_a, y_a).get_joueur() is self.joueur:
                return False
        if abs (y_a - self.y)/abs(x_a - self.x) == 1 :
            sens_c = (y_a - self.y) // abs(y_a - self.y)
            sens_l = (x_a - self.x) // abs(x_a - self.x)
            print(sens_l, sens_c)
            for i in range(1, abs(x_a - self.x), 1) :
                if self.plateau.getPiece(self.x + i*sens_l,
                                        self.y + i*sens_c) is not None:
                    return False
            return True
        else:
            return False

class Dame(Piece):
    def __init__(self, plateau, joueur, x, y):
        super().__init__(plateau, joueur, x, y)
        self.repres = "d"

    def peutBouger(self, x_a, y_a):
        return Tour.peutBouger(self, x_a, y_a) or Fou.peutBouger(self, x_a, y_a)


class Roi(Piece):
    def __init__(self, plateau, joueur, x, y):
        super().__init__(plateau, joueur, x, y)
        self.repres = "r"

    def peutBouger(self, x_a, y_a):
        mouvement = [(x, y) for x in range(-1, 2) for y in range(-1, 2)
                     if not (x == y and x == 0)]
        if self.plateau.getPiece(x_a, y_a) is not None:
            if self.plateau.getPiece(x_a, y_a).get_joueur() is self.joueur:
                return False
        for (xm, ym) in mouvement:
            if self.x + xm == x_a and self.y + ym == y_a:
                return True