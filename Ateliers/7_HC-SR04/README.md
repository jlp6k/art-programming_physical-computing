## Capteur de distance à ultrason

Un capteur de distance à ultrason est un capteur actif dont le principe de fonctionnement est comparable
à celui d'un sonar : le capteur émet un signal sonore bref dans les [ultrasons](https://fr.wikipedia.org/wiki/Ultrason)
et écoute l'écho de cette impulsion.

La vitesse du son dans l'air étant d'environ 344 m/s, le temps écoulé entre l'émission et la réception de l'écho
permet de calculer la distance entre le capteur et l'obstacle situé devant lui.
Par exemple, s'il s'écoule 0.1 seconde entre l'émission et la réception, cela signifie que le signal sonore a mis
0.1 seconde pour faire l'aller-retour entre le capteur et l'obstacle, la distance parcourue est de 344 ✕ 0.1 = 344 m 
aller-retour, soit 32.2 m entre le capteur et l'obstacle.

![Illustration du principe du sonar](../../Images/Sonar_Principle_FR.svg)

Dans le schéma ci-dessus, des impulsions sonores sont émises en direction de l'objet à détecter (figurées en rouge).
Elles sont réfléchies par l'objet et reviennent vers le récepteur (en vert).
La distance entre le capteur et l'objet `r = t * V / 2` où `t` est le temps mis par une impulsion sonore pour faire
l'aller-retour et `V` est la vitesse du son dans le milieu ambiant.

À noter que la mesure peut être perturbée de multiples façons, notamment par l'hétérogénéité du milieu et par
l'[effet Doppler](https://fr.wikipedia.org/wiki/Effet_Doppler) si le capteur ou l'objet détecté sont en mouvement.
