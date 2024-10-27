## Moteur électrique à courant continu à balais

Un moteur électrique (ou [machine électrique](https://fr.wikipedia.org/wiki/Machine_%C3%A9lectrique)) est un 
dispositif qui convertit l'énergie électrique en énergie mécanique.
Cette définition formelle et générale recouvre une grande variété d'appareils électriques.
Nous nous intéressons dans cet atelier à un type particulier de moteur électrique, 
le moteur à courant continu à balais (_brushed direct current electric motor_ ou _brushed DC electric motor_
en anglais).
Un autre type de moteur électrique est traité dans l'atelier sur les [`moteurs pas-à-pas`](../Ateliers/7_Moteur_pas-à-pas).

Ce type de moteur est probablement le plus répandu.
C'est celui qui équipe à plupart des petits équipements à piles ou batteries.
On le trouve par exemple dans les jouets ou dans les voitures (pour animer les essuies-glace ou le ventilateur 
du chauffage de l'habitacle ou celui du refroidissement du moteur, mais c'est un autre type de moteur qui sert à la
propulsion du véhicule).

La vidéo ci-dessous illustre le principe de fonctionnement du moteur à courant continu à balais.

[![Image de la vidéo Youtube : Moteur DC (courant continu), comment ça marche?](http://img.youtube.com/vi/A3b3Km5KVXs/0.jpg)](http://www.youtube.com/watch?v=A3b3Km5KVXs "Moteur DC (courant continu), comment ça marche?")

(N'hésitez pas à suggérer une meilleure vidéo !)

### Couple et vitesse de rotation

Le couple moteur est la force qui agit avec un bras de levier sur un point de pivot, ledit point
étant l'axe de rotation du moteur.
Ce couple moteur est exprimé en Newton par mètre, abrégé N m et correspond à une force exprimée en Newton
exercée sur un bras de levier à 1 mètre de l'axe de rotation.

Le couple et la vitesse de rotation du moteur dépendent de la tension d'alimentation et de l'intensité
du courant aux bornes du moteur.

La vitesse de rotation d'un moteur électrique peut rapidement atteindre des milliers de tours par minutes.
Un dispositif mécanique appelé réducteur, connecté à l'arbre du moteur, permet d'augmenter le couple
en diminuant la vitesse de rotation.

### Mise en œuvre

Nous disposons d'un moteur électrique avec réducteur.

![un moteur électrique à courant continu à balais équipé d'un réducteur](assets/moteur_3-6V_réducteur.jpg)

Des fils électriques (rouge et noir) sont connectés aux bornes de ce moteur.
Connectons le fil rouge au rail à 3.3V et le fil noir à un rail de masse (0 volts).
Notez à quelle vitesse et dans quel sens tourne le moteur.
Inversez la polarité : connectez le fil noir à la place du rouge et le fil rouge à la place du noir.
Le fil noir est maintenant connecté au rail à 3.3V et le rouge à la masse.
Observez que le moteur tourne en sens inverse.

Faites de même avec le rail à 5V et un rail de masse ; le moteur tourne plus vite.

### Faire varier la vitesse de rotation

Vous pourriez avoir l'idée d'alimenter le moteur au travers d'un potentiomètre pour faire varier sa tension 
d'alimentation comme nous l'avons fait avec une LED.
Malheureusement cette solution ne fonctionnera de façon acceptable qu'avec un très petit moteur.
En effet, un moteur électrique consomme un courant beaucoup plus important qu'une LED de 5mm de diamètre.

Si nous connectons un ampèremètre (tel que celui disponible dans votre multimètre) en série avec notre
moteur alimenté par le rail à 3.3V, le courant mesuré est de l'ordre de 150mA (soit 0.15A).

Comme nous l'avons vu dans l'atelier [`LED`](../Ateliers/2_LED), la puissance dissipée par un
élément d'un circuit peut être calculée à l'aide de la formule suivante `P = U ✕ I`
avec `P`, la puissance exprimée en watts, `U` la tension en volts aux bornes de l'élément et
`I` le courant qui traverse l'élément en ampères.

Ici le moteur consomme `P = U ✕ I = 3.3 ✕ 0.15 = 0.495 W`
à son plus haut régime.
Si on utilise un potentiomètre pour dissiper une partie de cette énergie afin de réduire la vitesse
du moteur, les caractéristiques du potentiomètre devront être choisies de façon adéquate
et nos petits potentiomètres ne peuvent pas dissiper un demi watt sans brûler.

### Modulation de largeur d'impulsion

Une solution pour faire varier la vitesse de rotation d'un moteur électrique à courant continu à balais
est similaire à celle que nous avons utilisée pour faire varier l'intensité de nos LED.
Cela consiste à alimenter le moteur avec des impulsions périodiques dont la longueur détermine la vitesse.

Le rapport de temps entre le début de deux impulsions consécutives et la durée d'une impulsion est appelé
rapport cyclique (_duty cycle_ en anglais).
Le rapport cyclique détermine le régime/ (la vitesse de rotation) du moteur alimenté par les impulsions.
Plus les impulsions sont longues, plus le moteur accélère (puisqu'il est alimenté pendant chaque impulsion).
Mais, plus le délai entre deux impulsions est long, plus le moteur ralenti (puisqu'il n'est plus alimenté
pendant ce temps).
Si la fréquence des impulsions est suffisamment élevée, les phases d'accélération/décélération se mêlent
pour obtenir une vitesse moyenne.

Ce mode de contrôle du régime moteur s'appelle
[modulation de largeur d'impulsion](https://fr.wikipedia.org/wiki/Modulation_de_largeur_d%27impulsion)
(_pulse width modulation_ ou _PWM_ en anglais).

Le graphique ci-dessous illustre la relation entre le rapport cyclique (la durée des impulsions par rapport
à la durée de la période) et le régime moteur.

![Graphique illustrant la relation entre le rapport cyclique et la vitesse de rotation](assets/PWM.svg)

D'après ce graphique la tension d'alimentation du moteur est de 0 volt ou de 3.3 volts.
Mais le moteur réagit comme s'il était alimenté par une tension variable entre 0 et 3.3V.

### L298N



