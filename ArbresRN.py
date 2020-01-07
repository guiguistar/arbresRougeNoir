# coding: utf-8

import random
import time

class NoeudRN:
    """
    Un arbre rouge-noir vérifie les propriétés suivantes:
       1. Un noeud est soit rouge soit noir.
       2. La racine et les noeuds vides (~ NIL) sont noirs.
       3. Si un noeud est rouge, ses enfants sont noirs.
       4. Tous les chemins d'un noeud jusque ses descendants vides ont le même
          nombre de noeuds noirs.

    La classe dispose de 4 champs fondamentaux:
     - valeur
     - fg: une référence vers le fils gauche
     - fd: une référence vers le fils droit
     - p : une référence vers le parent
     - couleur: 'R' ou 'N'

    Il est très important pour les critères d'arrêt des fonctions
    récursives que:
     - les noeuds vides, et seulement les noeud vides, aient:
        - valeur = None
        - fg = None
        - fd = None
     - les feuilles aient:
        - valeur différent de None
        - fg = noeud vide
        - fd = noeud vide
     - la racine ait:
        - valeur différente de None
        - parent = noeud vide

    Remarques:
       - tous les noeuds non vides ont deux fils, quitte à rajouter un
         ou deux fils vides
       - on pourrait n'utiliser qu'un seul noeud vide pour toutes les
         feuilles
       - la suppression n'est pas implémentée
    """
    def __init__(self, valeur=None, parent=None):
        self.valeur = valeur

        # Si le noeud n'est pas vide, on lui ajoute deux fils vides
        self.fg = None if valeur is None else NoeudRN()
        self.fd = None if valeur is None else NoeudRN()

        # On relie le noeud à son parent
        self.p = parent

        # On colore le noeud
        self.couleur = 'N' if valeur is None  else 'R'

        # Mettre pour self.verbosite = 1 pour afficher différentes informations
        # à l'exécution.
        self.verbosite = 0

    def estVide(self):
        return self.valeur is None

    def estFeuille(self):
        return self.fg.estVide() and self.fd.estVide()

    def estRacine(self):
        return self.p is None

    def estFilsGauche(self):
        if self.estRacine():
            return False
        return self == self.p.fg

    def estFilsDroit(self):
        # Syntaxe équivalente à celle de estFilsGauche()
        return not self.estRacine() and self == self.p.fd

    def estNoir(self):
        return self.couleur == 'N'

    def estRouge(self):
        return self.couleur == 'R'
    
    def calculerHauteur(self):
        if self.estVide() or self.estFeuille():
            return 0
        else:
            hg = self.fg.calculerHauteur()
            hd = self.fd.calculerHauteur()

            return 1+max(hg,hd)
        
    def calculerHauteurNoire(self):
        """
        La hauteur noire ne tient compte que des noeuds noirs.
        """
        if self.estVide():
            return 0
        else:
            hg = self.fg.calculerHauteurNoire()
            hd = self.fd.calculerHauteurNoire()

            h = 1 if self.couleur == 'N' else 0

            return h + max(hg,hd)
            
    def calculerGeneration(self):
        if self.estRacine():
            return 0
        return self.p.calculerGeneration() + 1

    def oncle(self):
        if self.p.estFilsGauche():
            return self.p.p.fd
        return self.p.p.fg
    
    def frere(self):
        if self.estFilsGauche():
            return self.p.fd
        return self.p.fg
        
    def afficher(self, texte=None):
        if texte: print(texte)
        if self.estVide():
            print('NIL')
        else:
            print('  noeud.valeur = {}.'.format(self.valeur))
            print('  noeud.couleur = {}.'.format(self.couleur))
            print('  noeud.fg.valeur = {}.'.format(self.fg.valeur))
            print('  noeud.fd.valeur = {}.'.format(self.fd.valeur))
            if not self.estRacine():
                print('  noeud.p.valeur = {}.'.format(self.p.valeur))
        
    def listeGenerations(self):
        """
        Crée une liste de listes de noeuds, regroupés par génération.
        [ [racine],
          [racine.fg, racine.fd];
          [racine.fg.fg, racine.fg.fd, racine.fd.fg, ...],
            ....,
          ]
        """
        if self.estVide(): return []
        F = [] # File pour le parcours en largeur
        liste = []
        F.append(self)
        while F:
            noeud = F.pop(0)
            if not liste:
                liste.append([noeud])
            else:
                if noeud.calculerGeneration() == liste[-1][-1].calculerGeneration():
                    liste[-1].append(noeud)
                else:
                    liste.append([noeud])
            if not noeud.estVide():
                F.append(noeud.fg)
                F.append(noeud.fd)
        return liste

    def calculerLargeur(self):
        """
        Retourne le nombre de noeuds de la génération la plus nombreuse.
        """
        liste = self.listeGenerations()
        if liste: return max(len(gen) for gen in liste)
        else:     return 0

    def insererRandom(self,eventail=1000):
        v = random.randrange(eventail)
        self.inserer(v)
    
    def inserer(self,valeur, parent=None):
        """
        Insère une valeur en respectant la structure d'ABR.
        Ne réquilibre pas.
        """
        if self.estVide():
            self.valeur = valeur
            self.fg = NoeudRN(parent=self)  # Essentiel pour les terminaisons
            self.fd = NoeudRN(parent=self)  # Idem
            self.p = parent
            if parent: self.couleur = 'R'
        else:
            if   valeur > self.valeur: self.fd.inserer(valeur, self)
            elif valeur < self.valeur: self.fg.inserer(valeur, self)
            else:
                if self.verbosite == 1:
                    print('La valeur se trouve déjà dans l\'arbre.')

    def insererRN(self,valeur, parent=None):
        """
        Insère une valeur en respectant la structure d'ABR.
        Rééquilibre en tenant compte de la structure d'arbre RN.
        """
        if self.verbosite == 1:
            print(80*'=')
            print('Insertion de la valeur {} dans {}.'.format(valeur,self.valeur)) 
            print(80*'=')
            
        if self.estVide():
            self.valeur = valeur
            self.fg = NoeudRN(parent=self)  # Essentiel pour les terminaisons
            self.fd = NoeudRN(parent=self)  # Idem
            self.p = parent
            if parent: self.couleur = 'R'   # Un noeud est rouge juste avant l'insertion
        else:
            if   valeur > self.valeur: self.fd.insererRN(valeur, self)
            elif valeur < self.valeur: self.fg.insererRN(valeur, self)
            else:
                if self.verbosite == 1:
                    print('La valeur se trouve déjà dans l\'arbre.')

        """
        Si la parent est noir, pas de problème, sinon la règle 3 est violée.
        """
                
        # Corrections pour satisfaire à toutes les règles
        """
        Cas 0: le noeud est la racine, violation de la règle 2.
        """
        if self.estRacine():
            if self.verbosite:
                print('{} est la racine.'.format(self.valeur))
            # La racine doit être noire (règle 2)
            self.couleur = 'N'
            
        elif self.p.estRacine():
            if self.verbosite:
                print('Le parent de {} est la racine.'.format(self.valeur))

        else:
            # Si on enfreint la règle 3 (parent rouge):
            if self.couleur == 'R' and self.p.couleur == 'R':

                if self.verbosite:
                    print('Oncle de {}: {}, de couleur {}'.format(self.valeur,
                                                                  self.oncle().valeur,
                                                                  self.oncle().couleur))
                """
                Cas 1: l'oncle est rouge:
                - changment de couleur pour le grand-père, l'oncle et le père

                   Ngp        c1        Rgp   
                   / \      ----->     / \    
                  Rp  Ro              Np  No  
                 / \                 / \      
                R   Nf              R   Nf    
        
                """
                if self.oncle().couleur == 'R':
                    if self.verbosite:
                        print('L\'oncle est rouge.')
                        
                    self.p.p.couleur = 'R'
                    self.oncle().couleur = 'N'
                    self.p.couleur = 'N'

                # Cas 2: l'oncle est noir
                elif self.oncle().couleur == 'N': 
                    if self.verbosite:
                        print('L\'oncle est noir.')
                    """
                    Cas 2-2: l'oncle est noir, configuration en triangle:

                          /                    \
                                    ou  
                          \                    /

                    - rotation droite autour du père si le noeud est fils gauche et
                      le père fils droit
                    - rotation gauche autour du père si le noeud est fils droit et
                      le père fils gauche
                    - puis cas 2-1

                    Les transformations ci-dessus permettent de se ramener à une
                    configuration en ligne.

                             Ngp               Ngp               
                             / \      rg       / \   
                            Rp  No  ----->    R   No 
                           / \               /       
                         Nf   R~self        Rp       
                                           /         
                                          Nf         
                    """
                    if self.estFilsGauche() and self.p.estFilsDroit():
                        if self.verbosite:
                            print('Configuration triangle noeud fils gauche père fils droit.')

                        self.p.rotationDroite() # cette rotation laise self intact

                        if self.verbosite:
                            self.afficher('Après triangle noeud fils gauche père fils droit.')
                            self.p.fd.afficher('Fils droit') 

                        self.p.fd.corrigerConfigurationLigne()
                        
                    elif self.estFilsDroit() and self.p.estFilsGauche():
                        if self.verbosite:
                            print('Configuration triangle noeud fils droit père fils gauche.')

                        self.p.rotationGauche()

                        if self.verbosite:
                            self.afficher('Après triangle noeud fils droit père fils gauche.')
                            self.p.fg.afficher('Fils gauche') # self.p.fg désigne Rp, après rotation, sur la figure ci-dessus

                        self.p.fg.corrigerConfigurationLigne()

                    """
                    Cas 2-1: configuration en ligne:

                         /                  \
                                  ou
                       /                      \

                    """
                    self.corrigerConfigurationLigne()

    def insererRNRandom(self,eventail=100):
        valeur = random.randrange(0,eventail)
        self.insererRN(valeur)
        
    def corrigerConfigurationLigne(self):
        """
        Cas 2-1: l'oncle est noir, configuration en ligne
        - rotation droite autour du grand-père si le noeud est fils
          gauche et le père fils gauche
        - rotation gauche autour du grand-père si le noeud est fils
          droit et le père fils droit
        - changement de couleur du grand-père et du père
  
                    Ngp               Rp               Np              
                   / \      rd       / \       c2     / \    
                  Rp  No  ----->    R   Ngp  ----->  R   Rgp 
                 / \                   / \              / \  
                R   Nf                Nf  No           Nf  No
                    
        """
                
        if self.estFilsGauche() and self.p.estFilsGauche():
            if self.verbosite:
                print('Configuration ligne gauche gauche.')
                
            self.p.p.couleur == 'R'
            self.p.couleur == 'N'
            self.p.p.rotationDroite()
                        
        if self.estFilsDroit() and self.p.estFilsDroit():
            if self.verbosite:
                print('Configuration ligne droit droit.')
            
            self.p.p.couleur == 'R'
            self.p.couleur == 'N'
            self.p.p.rotationGauche()


    """
    Notations:
      d~self     rd       b~self
       / \     ----->      / \
      b   E               A   d
     / \         rg          / \
    A   C      <-----       C   E

    Suppose que le noeud a un déséquilibre de +2
    A, b, C, d, E sont des noeuds
   
    - une rotation droite laisse b intact
    - après une rotation droite de d, il n'y a plus aucune référence vers b.
    """
    def rotationDroite(self):
        if self.verbosite:
            print('Rotation droite de {}.'.format(self.valeur))
            self.afficher('Avant rotation droite:')

        # Création du noeud d de droite
        d = NoeudRN(self.valeur,parent=self)
        d.fg = self.fg.fd
        d.fd = self.fd

        self.fg.fd.p = d
        self.fd.p = d
        
        # Mise à jour de self
        self.valeur = self.fg.valeur

        self.fg.fg.p = self
        self.fg = self.fg.fg

        self.fd = d

        if self.verbosite:
            self.afficher('Après rotation droite:')

    """
    Notations:
         d~self     rd       b~self
          / \     ----->      / \
         b   E               A   d
        / \         rg          / \
       A   C      <-----       C   E

    - une rotation gauche laisse d intact
    - après une rotation gauche de b, il n'y a plus aucune référence vers d.
    """
    def rotationGauche(self):
        if self.verbosite:
            print('Rotation gauche de {}.'.format(self.valeur))
            self.afficher('Avant rotation gauche:')

        # Création du noeud b de gauche
        b = NoeudRN(self.valeur, parent=self)
        b.fd = self.fd.fg
        b.fg = self.fg

        self.fd.fg.p = b
        self.fg.p = b

        # Mise à jour de self
        self.valeur = self.fd.valeur

        self.fd.fd.p = self
        self.fd = self.fd.fd

        self.fg = b

        if self.verbosite: self.afficher('Après rotation gauche:')

    """
    Méthodes pour l'affichage graphique
    """
    @classmethod
    def setLargeurTotalePixels(cls, l):
        cls.largeurTotalePixels = l

    @classmethod
    def setHauteurTotalePixels(cls, h):
        cls.hauteurTotalePixels = h

    def calculerGeometrie(self, t=False):
        """
        Attention cette méthode initialise l'attribut de classe 'transformation',
        qui est un boolean:
         - False pour utiliser la géométrie d'un ABR classique
         - True pour utiliser la géométrie d'un arbre 234

        Avantage:
          - ne stocker qu'une seule fois le booleen pour tous les noeuds d'un arbre donné
        Inconvénient:
          - peut provoquer des erreurs si on essaie de représenter graphiquement plusieurs
            arbres en même temps
        """
        NoeudRN.transformation = t
        self.geometrie()
        self.geometrie234()
        
    def geometrie(self):
        """
        Méthode récursive
        """
        if self.estRacine(): self.setGeometrieRacine()
        elif self.estVide(): self.setGeometrie(4,2)
        else:                self.setGeometrie(2,1)

        if self.fg: self.fg.geometrie()
        if self.fd: self.fd.geometrie()

    def geometrie234(self):
        """
        Méthode récursive.
        """
        if self.estRacine(): self.setGeometrieRacine()
        elif self.estVide(): self.setGeometrie234(4,2)
        else:                self.setGeometrie234(2,1)

        if self.fg: self.fg.geometrie234()
        if self.fd: self.fd.geometrie234()
            
    def setGeometrieRacine(self,coeffDistance=1,coeffRayon=8):
        assert self.estRacine()

        hauteur = self.calculerHauteur()
        largeur = self.calculerLargeur()

        # Distance de base pour séparer verticalement deux générations
        NoeudRN.distance =        coeffDistance * NoeudRN.hauteurTotalePixels / ( hauteur + 1 )
        NoeudRN.distance234 = 2 * coeffDistance * NoeudRN.hauteurTotalePixels / ( hauteur + 2 )

        # Rayons pour les disques qui représenteront les noeuds
        NoeudRN.rayon =     NoeudRN.largeurTotalePixels / (     coeffRayon * ( hauteur + 1 ) )
        NoeudRN.rayon234 =  NoeudRN.largeurTotalePixels / ( 2 * coeffRayon * ( hauteur + 2 ) )

        if self.verbosite == 1:
            self.affichageGeometrie(hauteur,largeur)
        
        self._x = NoeudRN.largeurTotalePixels // 2
        self._y = NoeudRN.rayon

        self._x234 = NoeudRN.largeurTotalePixels // 2
        self._y234 = NoeudRN.rayon234

    def affichageGeometrie(self, hauteur, largeur):
        print('Hauteur: {}'.format(hauteur))
        print('Hauteur noire: {}'.format(self.calculerHauteurNoire()))
        print('Largeur: {}\n'.format(largeur))
            
    def setGeometrie(self,cx=2,cy=1):
        """
        Cette méthode calcule les coordonnées (x,y) d'un noeud pour une disposition
        en ABR classique. La position d'un noeud est calculée en fonction de:
          - de la position de son  noeud parent
          - de son rang (fils gauche ou fils droit)
        """
        self._x = self.p._x
        self._y = self.p._y + NoeudRN.distance / cy

        # Distance de base pour séparer horizontalement deux noeuds:
        #    largeur du canvas / 2 ^ ( génération du noeud )        
        self.distanceHorizontale = NoeudRN.largeurTotalePixels // (2**self.calculerGeneration())

        # Si le neoud est fils gauche
        if self.estFilsGauche():
            self._x -= self.distanceHorizontale // cx
        # Si le noeud est fils droit
        else:
            self._x += self.distanceHorizontale // cx

    def setGeometrie234(self,cx=2,cy=1):
        """
        Cette méthode calcule les coordonnées (x,y) d'un noeud pour une
        disposition en arbre 234.
        La position d'un noeud est calculée en fonction de:
          - son rang (fils gauche ou fils droit)
          - sa couleur
          - le rang du noeud parent
          - la couleur du parent
        """
        self._x234 = self.p._x234
        self._y234 = self.p._y234

        # Distance de base pour séparer horizontalement deux noeuds:
        #    largeur du canvas / 2 ^ ( génération du noeud )
        self.distanceHorizontale234 = NoeudRN.largeurTotalePixels // (2**self.calculerGeneration())

        # Si le noeud est noir
        if self.estNoir():
            dX = self.distanceHorizontale234 // cx
            dY = NoeudRN.distance234 / cy

            self._y234 += dY
            
            if self.estFilsGauche():
                if self.p.estNoir():
                    # Noeud noir fils gauche d'un père noir gauche
                    if self.p.estFilsGauche():
                        self._x234 -= dX
                    # Noeud noir fils gauche d'un père noir droit
                    else:
                        self._x234 -= dX
                else:
                    # Noeud noir fils gauche d'un père rouge gauche
                    if self.p.estFilsGauche():
                        self._x234 -= dX + dX
                    # Noeud noir fils gauche d'un père rouge droit
                    else:
                        self._x234 += dX // 2
            else:
                if self.p.estNoir():
                    # Noeud noir fils droit d'un père noir gauche
                    if self.p.estFilsGauche():
                        self._x234 += dX
                    # Noeud noir fils droit d'un père noir droit
                    else:
                        self._x234 += dX
                else:
                    # Noeud noir fils droit d'un père rouge gauche
                    if self.p.estFilsGauche():
                        self._x234 -= dX // 2
                    # Noeud noir fils droit d'un père rouge droit
                    else:
                        self._x234 += dX + dX

        # Si le noeud est rouge, on peut le "coller" à son père noir
        else:
            dX = 2 * NoeudRN.rayon234 - 5 # un peu moins que le diamètre
            if self.estFilsGauche(): self._x234 -= dX 
            else:                    self._x234 += dX
    """
    Attention: les trois getters ci-après ne peuvent être appelé qu'après
    un appel à la méthode calculerGeometrie().
    """
    @property
    def x(self):
        if NoeudRN.transformation: return self._x234
        else:                      return self._x

    @property
    def y(self):
        if NoeudRN.transformation: return self._y234
        else:                      return self._y
    @property
    def r(self):
        if NoeudRN.transformation: return NoeudRN.rayon234
        else:                      return NoeudRN.rayon
        
    def xMorphisme(self,t):
        return int(self._x + t * (self._x234 - self._x))

    def yMorphisme(self,t):
        return int(self._y + t * (self._y234 - self._y)) 

    def rMorphisme(self,t):
        return int(NoeudRN.rayon + t * (NoeudRN.rayon234 - NoeudRN.rayon))

    
if __name__ == '__main__':
    arbre = NoeudRN()

    N = 1000000
    valeurs = [random.randrange(10*N) for _ in range(N)]

    print('Début de l\'insertion.')
    t1 = time.clock()
    for i, valeur in enumerate(valeurs):
        if i % ( N // 1000 ) == 0:
            print('{} valeurs insérées.'.format(i))
        arbre.insererRN(valeur)
    t2 = time.clock()
    print('Fin de l\'insertion: {} secondes.'.format(t2-t1))

    h = arbre.calculerHauteur()
    print('Hauteur de l\'arbre: {}, 2^{} = {}'.format(h,h, 2**h))
