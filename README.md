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
4. [`Moteur électrique`](Ateliers/_Moteur électrique): utiliser un moteur électrique
5. [`Servomoteur`](Ateliers/_Servomoteur): utiliser un servomoteur
6. [`Moteur pas-à-pas`](Ateliers/7_Moteur pas-à-pas): utiliser un moteur pas-à-pas

## Contribuer

Le contenu de ce dépôt ne fait qu'effleurer la programmation en Micropython
sur le Raspberry Pi Pico et le _Physical Computing_ en général.
Il reste une infinité d'autres sujets à documenter.

Tout le monde est donc invité à contribuer.
Si vous trouvez une erreur, si vous avez des idées pour de nouvelles fonctionnalités,
si vous avez écrit un nouveau module, si vous voulez discuter d'un sujet en relation, ...
Ouvrez une [_issue_](https://github.com/jlp6k/art-programming_physical-computing/issues)
ou contactez-moi directement.

## Licence

art-programming_physical-computing © 2024 by Jean-Louis Paquelin is licensed under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1).
