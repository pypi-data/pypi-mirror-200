# Quittance

Génère des quittances de loyers, au format PDF.


## Installation

    pip install quittance


## Configuration

Il faut d’abord configurer quelques informations (addresses, noms…),
le plus simple est d’exécuter :

    quittance config

qui vous génèrera un fichier de configuration et vous proposera de
l’éditer.

Il est possible d’éditer la configuration en ligne de commande :

    quittance config --bailleur-city Lyon --bailleur-country France

C’est pratique pour de petites corrections, mais pour tout configurer
préférez éditer le fichier `toml`.


## Utilisation

Pour générer une nouvelle quittance, exécutez :

    quittance

Une nouvelle quittance sera générée au format PDF.
