TemplateClassesEtInstances
==========================
Ce template génére la liste des classes, des instances et des paquetages d'un paquetage donné.

Contenu du template
-------------------
Pour un paquetage (ou une liste de paquetages) donné(s) les éléments suivants sont générés:
* la liste des classes, avec leur résumé et les instances correspondantes,
* la liste des instances, avec les scénarii dans lesquels ces instances sont utilisées
* pour chaque classe les opérations définies par cette classe ainsi que les messages reçus pas des instances de ces classes
* les diagrammes contenus dans le paquetage
* de manière récursive les sous paquetages contenu dans le paquetage

Exemple
-------
Un [exemple](Exemple.png) de modèle en entrée est fourni sous forme ainsi qu'un exemple de [résultat](Resultat.pdf) généré.

Historique
----------
* 1.2: Affichage dans une table des opérations définies sur les classes
* 1.1: Affichage des références vers les scenarii
* 1.0: Version initiale