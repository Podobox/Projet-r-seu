Fonctions à ajouter dans un fichier dans Controller:

si je veux modifier 

- si je suis proprio
    - check
    - je modifie
- sinon
    - demande propriete
    - si je suis proprio
        - check
        - je modifie
    - sinon
        bug
        - je fais rien


si je recois une demande de donner la proprieté
    - je donne


Propriété de propriété:
    - case (batiments et les walkers)
    - population (s'acquiere avec la construction/destruction/promotion/démotion de maisons)
    - argent


à faire :

- ajouter l'attribut propriétaire aux objet (bâtiment, walkers, ...)
- Classe proprio (fonction qui compte ses possessions)


Répartition:
    - 1 sur le daemon en C (2?)
    - 1 sur la communication C/python (socket)
    - 2 sur le python

ca sert a rien d'avoir un champ `owner` pour chaque tile vu qu'on a juste besoin de savoir
si c'est nous ou pas, c'est un booleen pas un id ou quoi. De toute facon on broadcast la
demande de propriété

Pareil, le message CHANGE_OWNERSHIP ne sert a rien
