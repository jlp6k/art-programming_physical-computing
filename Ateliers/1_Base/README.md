## Raspberry Pi Pico et alimentation électrique

La tension de fonctionnement du microcontrôleur RP2040 qui équipe la carte Raspberry Pi Pico est de 3.3 V.
Cette carte peut être alimentée de deux manières avec une large plage de tensions : 

1. Par le port USB, la carte reçoit alors une tension de 5 V qui est abaissée à 3.3 V.
2. Par la patte 39 nommée `VSYS`, dans ce cas, il faut appliquer une tension comprise entre 1.8 V
et 5.5 V qui est augmentée ou abaissée automatiquement aux 3.3 V requis. 

La patte 40 du Raspberry Pico est appelée `VBUS`. Elle donne accès au circuit d'alimentation fourni 
par la connexion USB, c'est-à-dire une tension de 5 V. Elle est à la masse si le Pico n'est pas
alimenté par le port USB.

La patte 36 est appelée `3V3(OUT)`. Lorsque le Pico est alimenté, elle fournit une tension constante
de 3.3 V.
Le courant maximum que cette patte peut délivrer est de 300 mA.

Les pattes 3, 8, 13, 18, 23, 28, 33, 38 sont nommées `GND` et connectées à la masse (0 V) du Raspberry
Pi Pico.

À noter que l'alimentation du microcontrôleur de la carte Raspberry Pi Pico peut être
suspendue en connectant la patte 37 `3V3_EN` à la masse. La tension de la patte `3V3(OUT)`
tombera alors à 0 V et le fonctionnement du microcontrôleur sera interrompu.

### Brochage du Pico

![identification des broches du Raspberry Pi Pico](../../Images/picow-pinout_wbg.svg)

La carte Raspberry Pi Pico W comporte de nombreuses connexions ou broches (_pin_ en anglais).
Le schéma ci-dessus montre l'ensemble des connexions disponibles et modes de fonctionnement des
broches, c'est ce qu'on appelle un _pinout diagram_ en anglais.

Comme c'est le cas pour la plupart de la documentation disponible sur des sujets 
technique, ce schéma est truffé d'acronymes.

Les broches en rouge étiquetées _Power_ concernent l'alimentation de la carte (cf. _supra_).

Les broches étiquetées en noir, sont toutes reliées à la masse (0 volt), _Ground_ en anglais.
Elles sont équivalentes.
À noter cependant que l'usage de la broche 33 `AGND` devrait être réservé aux usages analogiques,
autrement dit, comme masse pour les capteurs analogiques.
 
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
Le microcontrôleur RP2040 fournit 4 ADC dont 3 sont respectivement reliés aux
broches `ADC0`, `ADC1`, `ADC2` (voir aussi [3_Potentiomètre/Analog to Digital Converter](https://github.com/jlp6k/art-programming_physical-computing/blob/main/Ateliers/3_Potentiomètre/README.md#analog-to-digital-converter)).


Le quatrième convertisseur `ADC3` permet de mesurer la tension d'alimentation
appliquée à la broche `VSYS` de la carte Raspberry Pi Pico.
Il existe également un convertisseur nommé `ADC4` qui donne accès à la
température de fonctionnement de la puce RP2040.

L'ensemble des broches notées `GPIO` (_General Purpose Input Output_) peuvent être utilisées
pour émettre ou recevoir des signaux numériques (des 0 et des 1).
Une broche utilisée dans ce mode général ne pourra pas être simultanément utilisées pour fonctionner
selon un protocole de communication _UART_, _I2C_ ou _SPI_, ni comme convertisseur analogique-numérique.

Les deux broches en rose servent à interrompre le fonctionnement / redémarrer
le microcontrôleur. Elles ont un effet lorsqu'elles sont connectées à la masse.

Les deux broches en orange peuvent être connectées à une sonde extérieure qui
permet d'inspecter l'état du microcontrôleur et de sa mémoire pendant son
fonctionnement. Elles permettent également de programmer le microcontrôleur.
En MicroPython, l'usage de ces broches n'est généralement pas très utile.

### Câblage

Le câblage des platines de prototypage commence avec les rails d'alimentation 
latéraux. Les rails de masse sont repérées par un marquage latéral bleu.

Les rails de 3.3 et 5 volts sont marqués en rouge.
Rien ne les distingue hormis que l'un est à gauche et l'autre à droite
de la platine de prototypage.

![câblage de l'alimentation d'une platine de prototypage à partir d'un Rasperry Pi Pico](assets/Base_proto_wbg.svg)

> Les composants qui fonctionnent avec une tension d'alimentation de 3.3 volts
> peuvent être endommagés s'ils sont alimentés en 5 volts. Une grande attention doit être
> portée à ce sujet.

Les trous de la platine de prototypage sont reliés horizontalement
sous les rails d'alimentation.

Les trous sont reliés verticalement en deux séries de cinq trous
dans la partie centrale.

### Préparation du Raspberry Pi Pico

Il ne faut pas oublier d'installer MicroPython sur le Raspberry Pi Pico W.
Pour cela il faut suivre les instructions disponibles sur
https://www.raspberrypi.com/documentation/microcontrollers/micropython.html#drag-and-drop-micropython.

> Important : vous devez installer la version de MicroPython spécifique à la carte 
> dont vous disposez.

Toutes les versions de MicroPython sont disponibles sur https://micropython.org/download/.

Pour programmer votre Raspberry Pi Pico, procédez comme suit :

1. Téléchargez le _firmware_ approprié pour votre Microcontrôleur sur votre ordinateur.
2. Appuyez sur le micro-bouton `BOOTSEL` (sur le Pico, à côté de la LED) et maintenez-le enfoncé.
Tout en gardant le bouton appuyé, connectez votre Pico à un ordinateur avec un câble USB.
Relâchez le bouton `BOOTSEL` lorsque votre Pico apparaît comme un dispositif de stockage de masse
appelé `RPI-RP2`.
3. Glissez et déposez le fichier MicroPython `.uf2` sur le volume `RPI-RP2`.
Votre Pico redémarre, il fait maintenant fonctionner MicroPython !
