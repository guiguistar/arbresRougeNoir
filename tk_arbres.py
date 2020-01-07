from tkinter import *
import ArbresRN
import random

rouge = "#E53A40"
noir  = "#090707"
bleu  = "#30A9DE"
jaune = "#EFDA05"

class ArbreGraphique:
    def __init__(self,root):
        self.root = root
        self.root.title( "Arbres rouges noirs" )

        #  Récupérer la résolution de l'écran
        self.largeurEcran = root.winfo_screenwidth()
        self.hauteurEcran = root.winfo_screenheight()

        print('Résolution: {} x {}'.format(self.largeurEcran,
                                           self.hauteurEcran))
        
        self.largeurCanvas = 4 / 5 * self.largeurEcran
        self.hauteurCanvas = 4 / 5 * self.hauteurEcran
        
        # L'arbre sous-jacent
        self.arbre = ArbresRN.NoeudRN()
        self.arbre.setLargeurTotalePixels(self.largeurCanvas)
        self.arbre.setHauteurTotalePixels(self.hauteurCanvas)

        # Le conteneur pour le canvas
        self.conteneurHaut = Frame(self.root)
        self.conteneurHaut.pack(side = TOP)
        self.conteneurHaut.configure(background=bleu)

        # Le conteur pour le texte, la saisie, le bouton
        self.conteneurBas = Frame(self.root)
        self.conteneurBas.pack(side = TOP)

        # Le canvas sur lequel dessiner l'abre
        self.canvas = Canvas(self.conteneurHaut, 
                             width=self.largeurCanvas,
                             height=self.hauteurCanvas,
                             background=bleu,
                             highlightbackground=bleu)
        self.canvas.pack(padx=5,pady=5)


        # Le champ de saisie de la valeur à insérer dans l'arbre
        self.valeurNoeud = StringVar()
        self.valeurNoeud.set(random.randrange(0,100))
        
        self.champ = Entry(self.conteneurBas, textvariable=self.valeurNoeud, width = 5, justify='right')
        chaine = 'Appuyer sur Entrée pour insérer un nombre aléatoire ou saisir un nombre.'
        chaine += 'Flèche haut/bas en mode arbre RN.'
        self.label = Label(self.conteneurBas, text=chaine )

        self.label.pack(side = LEFT, padx=20, pady=5)
        self.champ.pack(side = LEFT, pady=5)

        self.champ.bind('<KP_Enter>', self.gererSaisie)
        self.champ.bind('<Return>', self.gererSaisie)

        self.champ.focus_set()

        # La boîte à cocher pour afficher/masquer NIL
        self.booleenNIL = IntVar()

        self.boite = Checkbutton(self.conteneurBas, text='NIL', variable=self.booleenNIL, command=self.gererBoite)
        self.boite.pack(side = LEFT, pady=5)

        # Les boutons radio pour choisir le type d'arbre
        self.modeSelectionne = StringVar()
        self.modeSelectionne.set('ABR')
        
        self.rBoutonABR  = Radiobutton(self.conteneurBas,variable=self.modeSelectionne,
                                       text='ABR',value='ABR',command=self.gererBouton)
        self.rBoutonABR.pack(side = LEFT)
        self.rBoutonARN  = Radiobutton(self.conteneurBas,variable=self.modeSelectionne,
                                       text='Arbre RN',value='ARN',command=self.gererBouton)
        self.rBoutonARN.pack(side = LEFT)
        
        # Crée une première liste de générations
        self.mettreAJour()
        
        # Morphisme RN <-> 234
        self.root.bind('<Up>',   self.gererHaut)
        self.root.bind('<Down>', self.gererBas)
        self.transition = 0
        
    def parcoursListe(self, fonction):
        dessinerNIL = self.booleenNIL.get()
        for g, gen in enumerate(self.liste):
            for p, noeud in enumerate(gen):            
                fonction(noeud,dessinerNIL)

    def dessinerArete(self,noeud,dessinerNIL=False):
        if not noeud.estRacine() and ( not noeud.estVide() or dessinerNIL ):
            #self.canvas.create_line(noeud.x, noeud.y, noeud.p.x, noeud.p.y, fill=noir, width=1.5)
            self.canvas.create_line(noeud.xMorphisme(self.transition),
                                    noeud.yMorphisme(self.transition),
                                    noeud.p.xMorphisme(self.transition),
                                    noeud.p.yMorphisme(self.transition),
                                    fill=noir, width=1.5)
        
    def dessinerNoeud(self,noeud,dessinerNIL=False):
        if self.modeSelectionne.get() == 'ABR':
            couleurNoeud = noir

        if self.modeSelectionne.get() == 'ARN':
            couleurNoeud = noir if noeud.couleur == 'N' else rouge
            
        valeur = 'NIL'

        """
        r = noeud.r

        x1, y1 = noeud.x - r, noeud.y - r
        x2, y2 = noeud.x + r, noeud.y + r
        """
        r = noeud.rMorphisme(self.transition)

        x1, y1 = noeud.xMorphisme(self.transition) - r, noeud.yMorphisme(self.transition) - r
        x2, y2 = noeud.xMorphisme(self.transition) + r, noeud.yMorphisme(self.transition) + r

        if not noeud.estVide():
            valeur = noeud.valeur
            self.canvas.create_oval( x1, y1, x2, y2, fill=couleurNoeud, outline="")
            self.canvas.create_text( x1+r, y1+r, text=str(valeur), fill=jaune)
        elif dessinerNIL:
            c = 1.5
            self.canvas.create_rectangle( x1+r/c, y1+r/c, x2-r/c, y2-r/c, fill=couleurNoeud, outline="")
            self.canvas.create_text( x1+r, y1+r, text=str(valeur), fill=jaune)

    # Met à jour la géométrie de l'abre après l'ajourt d'un noeud
    def mettreAJour(self):
        """
        Mise à jour de la liste et de la géométrie après l'ajout d'un noeud.
        """
        self.liste = self.arbre.listeGenerations() # On récupère le dernier état de l'arbre
        self.arbre.calculerGeometrie(t=False) # ainsi que sa géométrie

    def dessiner(self):
        # On efface tout le canvas
        self.canvas.delete("all")

        # On redessine tous
        self.parcoursListe(self.dessinerArete)
        self.parcoursListe(self.dessinerNoeud)

    def mettreAJourEtDessiner(self):
        self.mettreAJour()
        self.dessiner()

    # Méthode appelée lorsqu'un valeur est saisie
    def gererSaisie(self, event):
        valeur = 0

        try:
            valeur = int(self.valeurNoeud.get())
        except ValueError:
            print('Valeurs entières uniquement.')

        if self.modeSelectionne.get() == 'ABR':
            self.arbre.inserer(valeur)
        if self.modeSelectionne.get() == 'ARN':
            self.arbre.insererRN(valeur)
            
        self.valeurNoeud.set(random.randrange(0,100))

        self.mettreAJourEtDessiner()

    # Méthode appelée lorsque le bouton NIL est cliqué
    def gererBoite(self):
        self.mettreAJourEtDessiner()
        
    # Methode appelée lorsque la flèche du haut est pressée
    def gererHaut(self,event):
        if self.modeSelectionne.get() == 'ARN':
            self.transition += 0.02
            if self.transition > 1: self.transition = 1
            self.mettreAJourEtDessiner()

    # Méthode appelée lorsque la flèche du bas est pressée
    def gererBas(self,event):
        if self.modeSelectionne.get() == 'ARN':
            self.transition -= 0.02
            if self.transition < 0: self.transition = 0
            self.mettreAJourEtDessiner()

    # Méhode appelée lorsque le bouton radio est préssé
    def gererBouton(self):
        print('Mode {}'.format(self.modeSelectionne.get()))
        if self.modeSelectionne.get() == 'ABR':
            self.transition = 0
        self.canvas.delete("all")
        self.arbre = ArbresRN.NoeudRN()
        
fenetre = Tk()
ag = ArbreGraphique(fenetre)
fenetre.mainloop()
