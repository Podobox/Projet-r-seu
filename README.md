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
