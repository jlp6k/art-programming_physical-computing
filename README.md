# art-programming_physical-computing
Ce dépôt correspond au contenu téléchargeable d'un enseignement de _Physical Computing_ 
destiné aux étudiants de la [Villa Arson](https://villa-arson.fr/) et utilisant
[Micropython](https://docs.micropython.org/en/latest/) comme langage
et le [Raspberry Pi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#picow-technical-specification)
comme plate-forme matérielle.

## Comment utiliser ce dépôt ?

Ce dépôt est organisé en dossiers. La plupart de ces dossiers correspondent à des
ateliers-leçons permettant d'acquérir une ou plusieurs connaissances et compétences.
L'ordre de lecture des ateliers est important car ils sont classés par difficulté
croissante et les ateliers les plus avancés dépendent souvent de ceux qui les précèdent.

Le code proposé dans les ateliers s'appuie sur un ensemble de modules écrits dans le but
de simplifier l'usage de certains types de composants électroniques.
Ces modules sont disponibles dans le dossier [`lib`](lib).
Ils reflètent ma vision de l'idée de simplification, ils pourraient ne pas convenir
à votre usage.

1. [`Base`](Ateliers/1_Base) :
pour commencer le prototypage électronique avec le Raspberry Pi Pico.
C'est un atelier dont la mise en œuvre est préalable à tous les autres ateliers.
2. [`LED`](Ateliers/2_LED): allumer une LED, la faire clignoter.
3. [`Potentiomètre`](Ateliers/3_Potentiomètre): faire varier une tension à l'aide
d'un potentiomètre, utiliser une entrée analogique du Raspberry Pi Pico.
4. [`HC-SR501`](Ateliers/_HC-SR501): mise en œuvre du module capteur de mouvement HC-SR501.
5. [`Moteur électrique`](Ateliers/_Moteur_électrique): utiliser un moteur électrique.
6. [`Servomoteur`](Ateliers/_Servomoteur): utiliser un servomoteur.
7. [`Moteur pas-à-pas`](Ateliers/7_Moteur_pas-à-pas): utiliser un moteur pas-à-pas.

À noter que si le texte des ateliers est rédigé en français, il arrive que 
la documentation et les commentaires des modules contenus dans le dossier
`lib` soient écrits en anglais (ou dans un mélange de français et d'anglais).
Ceci s'explique parce que tous ces codes n'ont pas été écrits à la même période,
ni tout à fait avec la même motivation car ils proviennent parfois de projets plus anciens.
Je pense qu'un travail de traduction systématique vers l'anglais serait souhaitable
comme toute documentation partagée devrait l'être (IMHO) mais à ce jour je n'en ai 
pas eu le temps.

## Contribuer

Le contenu de ce dépôt ne fait qu'effleurer la programmation en Micropython
sur le Raspberry Pi Pico et le _Physical Computing_ en général.
Il reste une infinité d'autres sujets à documenter.

Tout le monde est donc invité à contribuer.
Si vous trouvez une erreur, si vous avez des idées pour de nouvelles fonctionnalités,
si vous avez écrit un nouveau module, si vous voulez discuter d'un sujet en relation, ...
Ouvrez une [_issue_](https://github.com/jlp6k/art-programming_physical-computing/issues)
ou contactez-moi directement.

Toute contribution sera récompensée par ma gratitude et votre nom dans la liste
des contributeurices.

Et surtout si vous êtes enseignant·e, ne restez pas dans l'ombre, nous pourrions collaborer.

## Licence et usage

art-programming_physical-computing
© 2024 by Jean-Louis Paquelin is licensed under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1).

Sauf mention contraire, tout le contenu du dépôt est ainsi licencié.

Si vous utilisez tout ou partie de ce projet en dehors d'un projet pédagogique de la 
Villa Arson, j'apprécierais que vous citiez cette source (et de toute manière c'est ce que
demande explicitement la licence ci-dessus).
Quelque chose comme :

> Ceci a été produit avec https://github.com/jlp6k/art-programming_physical-computing/
> 
> This was produced with https://github.com/jlp6k/art-programming_physical-computing/

Vous pouvez aussi m'envoyer un mail ou me contacter via https://github.com/jlp6k/art-programming_physical-computing/issues.
pour me dire ce que vous avez accompli avec l'aide du code ou des informations proposés ici.
