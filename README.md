# BioPathBot

SHS : Digital Humanities A, EPFL, 2017

## Collaborateurs

* [Christophe Badoux](https://github.com/christophebx)
* [Kim Lan Phan Hoang](https://github.com/pyphilia)
* [Robin Lan](https://github.com/roblan11)
* [Julien Burkhard](https://github.com/sherushe)

## Librairies

* **Basemap** pour dessiner des cartes: http://matplotlib.org/basemap/index.html
* **Geopy** pour trouver les coordonnées géographique d'un lieu: https://pypi.python.org/pypi/geopy

## Objectif

Ce bot effectue deux types d'actions en parallèle :

1. Il gère automatiquement les informations ayant lieu dans des zones spatiotemporelles en recopiant toutes les informations correspondant à une zone spatiotemporelle donnée.

Exemple le bot détecte

1864.08.22 / Genève. Création par Henri Dunant de la Croix rouge. [6]
et ajoute l'évènement dans la page de référence spatiotemporelle de taille minimale correspondante.

2. Il construit et maintient pour chaque personne une page spéciale qui trace la trajectoire biographique de cette personne.

La biographie d'Henri Dunant est transformée en séquence de zones spatiotemporelles.

Eventuellement cette page peut aussi contenir une carte temporelle.
