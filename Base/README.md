La tension de fonctionnement du microcontrôleur RP2040 qui équipe la carte Raspberry Pi Pico est de 3,3 V. La carte peut être alimentée de
deux manières : 

1. Par le port USB, la carte reçoit alors une tension de 5 V qui est abaissée à 3,3 V.
2. Par la patte 39 nommée `VSYS`, dans ce cas, il faut appliquer une tension comprise entre 1,8 V
et 5,5 V qui est augmentée ou abaissée automatiquement aux 3,3 V requis. 

La patte 40 du Raspberry Pico est appelée `VBUS`. Elle donne accès au circuit d'alimentation fourni 
par la connexion USB, c'est-à-dire une tension de 5 V. Elle est à la masse si le Pico n'est pas
alimenté par le port USB.

La patte 36 est appelée `3V3(OUT)`. Lorsque le Pico est alimenté, elle fournit une tension constante
de 3,3 V.
Le courant maximum que cette patte peut délivrer est de 300 mA.

Les pattes 3, 8, 13, 18, 23, 28, 33, 38 sont nommées `GND` et connectées à la masse (0 V) du Raspberry
Pi Pico.

À noter que l'alimentation du microcontrôleur de la carte Raspberry Pi Pico peut être
suspendue en connectant la patte 37 `3V3_EN` à la masse. La tension de la patte `3V3(OUT)`
tombera alors à 0 V et le fonctionnement du microcontrôleur sera interrompu.

### Brochage du Pico

![identification des broches du Raspberry Pi Pico](..%2FImages%2Fpicow-pinout_wbg.svg)

La carte Raspberry Pi Pico W comporte de nombreuses connexions ou broches (_pin_ en anglais).
Le schéma ci-dessus montre l'ensemble des connexions disponibles et modes de fonctionnement des
broches, c'est ce qu'on appelle un _pinout diagram_ en anglais.

Comme c'est le cas pour la plupart de la documentation disponible sur des sujets 
technique, ce schéma est truffé d'acronymes.

Les broches en rouge étiquetées _Power_ concernent l'alimentation de la carte (cf. _supra_).

Les broches étiquetées en noir, sont toutes reliées à la masse (0 volt), _Ground_ en anglais.
Elles sont interchangeables.
 
[_UART_](https://fr.wikipedia.org/wiki/UART) est un acronyme qui signifie _Universal Asynchronous Receiver Transmitter_.
Cela désigne ici (en violet) des paires de broches, l'une pour l'émission,
l'autre pour la réception, qui permettent de communiquer avec d'autres équipements
électroniques.
Le microcontrôleur RP2040 qui équipe la carte Raspberry Pi Pico peut utiliser
différentes paires de broches pour communiquer selon les
[protocoles](https://fr.wikipedia.org/wiki/Protocole_de_communication) _UART_,
[_I2C_](https://fr.wikipedia.org/wiki/I2C) (en magenta) 
ou [_SPI_](https://fr.wikipedia.org/wiki/Serial_Peripheral_Interface) (en bleu). 
Évidemment, une paire de broches ne peut être utilisée qu'avec un seul protocole 
de communication à la fois.
La variante foncée des couleurs des broches pouvant être utilisée pour communiquer
avec l'une des protocoles _UART_, _I2C_ ou _SPI_ indique la configuration par défaut
des broches.

Les broches étiquetées en vert foncé sont celles reliées aux convertisseurs
analogique-numérique, _analog to digital converter_ ou _ADC_ en anglais.
Le microcontrôleur RP2040 fournit 4 ADC dont 3 sont respectivement reliées aux
broches `ADC0`, `ADC1`, `ADC2`.

Le quatrième convertisseur `ADC3` permet de mesurer la tension d'alimentation
appliquée à la broche `VSYS` de la carte Raspberry Pi Pico.
Il existe également un convertisseur nommé `ADC4` qui donne accès à la
température de fonctionnement de la puce RP2040.

Les deux broches en rose servent à interrompre le fonctionnement / redémarrer
le microcontrôleur. Elles ont un effet lorsqu'elles sont connectées à la masse.

Les deux broches en orange peuvent être connectées à une sonde extérieure qui
permet d'inspecter l'état du microcontrôleur et de sa mémoire pendant son
fonctionnement. Elles permettent également de programmer le microcontrôleur.
En MicroPython, l'usage de ces broches n'est généralement pas très utile.

### Câblage

Le câblage des plaques de prototypage commence avec les rails d'alimentation 
latéraux. Les rails de masse sont repérées par un marquage bleu.
Les rails de 3,3 et 5 volts sont marqués en rouge. Rien ne les distingue hormis que l'un
est à gauche et l'autre à droite de la plaque de prototypage.

![câblage de l'alimentation d'une plaque de prototypage à partir d'un Rasperry Pi Pico](Base_wbg.svg)

> Les composants qui fonctionnent avec une tension d'alimentation de 3,3 volts
> peuvent être endommagés s'ils sont alimentés en 5 volts. Une grande attention doit être
> portée à ce sujet.

### Préparation du Raspberry Pi Pico

Il ne faut pas oublier d'installer MicroPython sur le Raspberry Pi Pico W.
Pour cela il faut suivre les instructions disponibles sur
https://www.raspberrypi.com/documentation/microcontrollers/micropython.html.

> Important : vous devez installer la version de MicroPython spécifique à la carte 
> dont vous disposez.

Toutes les versions de MicroPython sont disponibles sur https://micropython.org/download/.
