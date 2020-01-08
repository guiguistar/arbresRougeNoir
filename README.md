# arbresRougeNoir

Outil de visualisation des arbres rouge-noir et de l'arbre 2-3-4 qui lui est isomorphe.

# Propriétés d'un arbre rouge-noir

    Un arbre rouge-noir vérifie les propriétés suivantes:
       1. Un noeud est soit rouge soit noir.
       2. La racine et les noeuds vides (~ NIL) sont noirs.
       3. Si un noeud est rouge, ses enfants sont noirs.
       4. Tous les chemins d'un noeud jusque ses descendants vides ont le même
          nombre de noeuds noirs.

# ArbresRN.py implémente:
  - une classe NoeudRN représentant un noeud dans un arbre rouge-noir.
  - l'insertion en tant qu' arbre binaire de recherche
  
# tk_arbres.py implémente:
 - représentation graphique des arbres
 
# Exemple:

## Arbre initial:
<img src="img/arbresRougeNoir_capture_1.png" alt="Arbre rouge-noir"/>

## Transition 1:
<img src="img/arbresRougeNoir_capture_2.png" alt="Arbre rouge-noir"/>

## Transition 2:
<img src="img/arbresRougeNoir_capture_3b.png" alt="Arbre rouge-noir"/>

## Arbre 2-3-4
<img src="img/arbresRougeNoir_capture_3.png" alt="Arbre rouge-noir"/>

