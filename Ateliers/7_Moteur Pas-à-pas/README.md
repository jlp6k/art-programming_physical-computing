## Moteur pas-à-pas

Un [moteur pas à pas](https://fr.wikipedia.org/wiki/Moteur_pas_%C3%A0_pas)
(_stepper motor_ en anglais) est un type de moteur électrique rotatif
qu'il est possible de commander pour qu'il se place dans une position
angulaire précise.

Bien que d'usage souvent similaire au servomoteur, son fonctionnement
est tout à fait différent, de même que la façon de le contrôler.

Un moteur pas-à-pas est caractérisé par

- sa tension d'alimentation et son intensité, 
- sa résolution angulaire (combien de pas par tour ou combien de degrés entre
deux pas consécutifs),
- ses dimensions,
- s'il est bipolaire ou unipolaire et
- son couple : la force mécanique qu'il peut produire qui dépend largement de
ses caractéristiques physiques (plus il sera gros et plus il consommera d'énergie, plus
son couple sera élevé).

Pour faire fonctionner un moteur pas-à-pas, on emploie des circuits
intégrés spécifiquement étudiés pour cela et dont il existe de nombreuses
variétés qui facilitent plus ou moins la mise en œuvre des moteurs
pas-à-pas avec un microcontrôleur.
Ces circuits sont appelé des _stepper drivers_ (pilotes de moteur pas-à-pas
en français).

Dans le monde DIY, on rencontre fréquemment les moteurs 28BYJ-48 pilotés à l'aide du
circuit ULN2003. C'est une combinaison de moteur et de circuit de pilotage peu coûteuse
(de l'ordre de quelques euros).

Un autre circuit fréquemment utilisé est l'Allegro A4988 popularisé par le fabricant de
matériel de hobby [Pololu](https://www.pololu.com/product/1182).
Il permet de piloter des moteurs pas-à-pas en utilisant seulement 2 ports gpio (au minimum)
contre 4 ports pour le contrôleur ULN2003.
Par ailleurs, une grande partie des difficultés à surmonter pour coder le mouvement d'un
moteur pas-à-pas en utilisant un circuit ULN2003 est prise en charge par le circuit A4988.
Cela simplifie d'autant la charge du microcontrôleur que vous utilisez.

Pour notre part, nous utiliserons le couple 28BYJ-48 + ULN2003.










