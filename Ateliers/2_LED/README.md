Une [LED](https://fr.wikipedia.org/wiki/Diode_%C3%A9lectroluminescente)
(_Light-Emitting Diode_), diode électroluminescente en français, est un composant
électronique semiconducteur qui produit de la lumière lorsqu'il est correctement alimenté.

À ce jour (2024/08/15), toutes les versions des cartes Raspberry Pi Pico sont équipées
d'une LED verte. La broche qui contrôle la LED varie cependant d'un modèle 
à l'autre.

![Emplacement de la LED sur la carte Raspberry Pi Pico W](../../Images/Pico1W_led_wbg.svg)

### Allumer la LED du Pico

Le programme suivant allume la LED de la carte Raspberry Pi Pico pendant 5 secondes,
puis l'éteint.

```python
import machine
import time

# On affecte à la variable led_pin un objet décrivant la broche à laquelle
# est connectée la 2_LED du Pico et la configuration de cette broche (ici en sortie).
led_pin = machine.Pin("LED", machine.Pin.OUT)

# On appelle la méthode on() de l'objet led_pin afin de passer la broche correspondante
# à 1. Cela a pour effet d'alimenter la 2_LED qui s'allume.
led_pin.on()

# On utilise la fonction sleep() du module time pour mettre le programme en pause
# pendant 5 secondes.
time.sleep(5)

# On appelle la méthode off() de l'objet led_pin afin de passer la broche correspondante
# à 0. Cela a pour effet d'éteindre la 2_LED.
led_pin.off()
```

Le programme suivant fait clignoter la LED du Pico à une fréquence de 1 Hz, c'est-à-dire
que le cycle d'allumage et d'extinction de la LED se répète 1 fois par seconde.

```python
import machine
import time

# On configure la broche qui contrôle la 2_LED du Pico.
led_pin = machine.Pin("LED", machine.Pin.OUT)

# On démarre une boucle infinie.
while True:
    # On appelle la méthode toggle() de l'objet led_pin afin de changer son état :
    # si la broche est à 1, elle bascule à 0,
    # si elle est à 0, elle bascule à 1.
    led_pin.toggle()
    
    # L'exécution du programme est suspendue pendant 0.5 seconde.
    time.sleep(0.5)
    
    # L'état de la 2_LED reste inchangé (pendant le temps de la pause) jusqu'au
    # tour de boucle suivant.
```

Pouvoir contrôler la LED du Pico est d'une utilité limitée.
Nous allons voir comment connecter d'autres LED au Pico.

### Belle LED

Une LED est un composant électronique qui comporte deux pattes (deux pôles).
On dit que c'est un composant bipolaire ou un dipôle.
Son fonctionnement est non linéaire et polarisé (ou asymétrique). 
Ainsi, le sens de branchement d'une diode détermine le fonctionnement du circuit
dont elle fait partie.

Une diode (LED ou autre) laisse passer le courant si la tension appliquée à l'anode,
le pôle positif, est plus importante qu'à la cathode, le pôle négatif.
Dans cette configuration, la diode est dite passante.
Si la tension est plus importante à la cathode qu'à l'anode, la diode bloque le courant
Dans ce cas, on dit que la diode est bloquée.

À noter que si la différence de potentiel (la différence entre la tension à l'anode et
la tension à la cathode) dépasse une valeur maximale dépendante du modèle de diode employée,
la diode sera détruite.

![symbole_diode.svg](../../Images/symbole_diode.svg)
![symbole des LEDs](../../Images/symbole_LED.svg) 

Les dessins ci-dessus sont les représentations symboliques d'une diode et d'une LED.
Le côté positif d'une diode (l'anode) est matérialisé par un triangle,
le côte négatif (la cathode) est matérialisé par une barre.
Les flêches sur le symbole de la LED figurent la lumière émise par ce type
de diode lorsqu'un courant les traverses (lorsque qu'elles sont passantes).

![Anatomie d'une LED](../../Images/LED_labelled_fr_wbg.svg)

Les LEDs ont des caractéristiques physiques variables. Les plus importantes sont leur
couleur, leur dimension et forme, leur tension d'alimentation et le courant maximum
qui peut les traverser sans les endommager.

La couleur d'une LED est déterminée par le matériau semiconducteur employé pour sa
fabrication (et rarement par la couleur du plastique qui l'encapsule).

Les LEDs que l'on peut utiliser sur une platine de prototypage sont disponibles
dans de nombreuses couleurs et généralement en 3 ou 5 mm de diamètre.

![Leds vert, rouge et bleue](assets/GRB%20leds_bbg.jpg)

Pour connaître la tension d'alimentation exacte d'une LED et le courant qui peut la
traverser, il faut se référer à sa fiche technique.

La tension de fonctionnement d'une LED se situe généralement entre 1 et 3 volts.
Le courant peut aller de quelques milliampères pour les LEDs les plus courantes qui servent
à la signalisation visuelle, à quelques ampères pour les LEDs servant à l'éclairage.

#### Circuit en série

Les tensions dont nous disposons sont :

- 5 volts fournis à partir de la connexion USB de la carte Raspberry Pi Pico
sur la broche `VBUS`.
- 3.3 volts fournis par le convertisseur de tension qui équipe la carte Raspberry Pi Pico
sur la broche `3V3(OUT)`.

Les tensions fournies par la carte sont donc trop élevées pour alimenter directement 
une LED : il faut réduire la tension. Pour cela, nous allons mettre une résistance en série
avec la LED.

Un circuit électrique en série est un circuit dans lequel des composants bipôlaires
sont connectés les uns à la suite des autres.
La tension aux bornes d'un tel circuit est égale à la somme des tensions aux bornes
de chaque composant.

```mermaid
flowchart LR
    left(" ") --- A[composant 1]
    A --- B[composant 2]
    B --- C[composant 3]
    C --- right(" ")
```

La tension entre les extrémités du circuit est égale à la tension aux bornes de
`composant 1` + la tension aux bornes de `composant 2` + la tension aux bornes de
`composant 3`.

En vertu de la [loi d'Ohm](https://fr.wikipedia.org/wiki/Loi_d%27Ohm), 
une résistance connectée en série avec la LED va permettre d'abaisser la tension 
aux bornes de la LED. 

```mermaid
flowchart LR
    left(" ") --- A[LED]
    A --- B[Résistance]
    B --- right(" ")
```

La loi d'Ohm est très simple : la tension `U` (en volts) aux bornes
d'une résistance est égale au produit du courant `I` (en ampères) qui la traverse par
sa valeur `R` (en ohms).

```mermaid
flowchart LR
    A([U = R ✕ I]) ~~~ B([R = U / I]) ~~~ C([I = U / R])
```

Prenons par exemple une LED dont la tension de fonctionnement est 2 volts et
le courant de fonctionnement 10 milliampères que nous alimentons à partir du rail
à 3.3 volts de notre platine de prototypage.

La tension aux bornes de la résistance doit être 3.3 - 2 = 1.3 volts.
Connaissant la tension (1.3 V) et le courant (10 mA = 0.01 A), la valeur de la résistance
peut-être calculée par la formule `R = U / I = 1.3 / 0.01 = 130 Ω (ohms)`.

Ainsi il faudra connecter la LED en série avec une résistance _d'au moins_ 130 Ω. 
Une valeur de résistance supérieure protégera efficacement la LED mais diminuera sa luminosité.
Une résistance de valeur inférieure n'abaissera pas suffisamment la tension aux bornes
de la LED, la surtension réduira la durée de vie de la LED, voire la détruira.

L'énergie consommée par la résistance pour protéger la LED est dissipée sous forme de chaleur.
Cela implique que la puissance de la résistance doit être appropriée à son usage car, 
si ce n'est pas le cas, la résistance brulera.
Les résistances de 1/8, 1/4 ou 1/2 watt sont communes.
La puissance effectivement dissipée par la résistance se calcule à
l'aide de la formule suivante `P = U ✕ I` avec `P`, la puissance exprimée en watts,
`U` en volts et `I` en ampères.

Dans le cas qui nous occupe, la résistance devra dissiper `P = U ✕ I = 1.3 ✕ 0.01 = 0.013 W`,
une résistance de 1/8 W = 0.125 W suffira donc amplement.

Si vous voulez vous épargner l'effort de ces calculs, nombre de pages web les feront
pour vous. Par exemple : 
[calculateur de résistance pour LED chez DigiKey](https://www.digikey.fr/fr/resources/conversion-calculators/conversion-calculator-led-series-resistor)

#### Résistance ✊

![symboles des résistances](../../Images/symbole_r%C3%A9sistance.svg)

Comme montré dans le dessin ci-dessus, les 
[résistances](https://fr.wikipedia.org/wiki/R%C3%A9sistance_(composant))
peuvent être schématiquement représentées de deux façons. La version en zigzag est 
une représentation normalisée américaine mais largement employée dans le reste du monde.

Ce sont des composants bipôlaires symétrique, ils fonctionnent de manière identique
dans les deux sens.

Les résistances les plus courantes dans les usages de hobby se présentent sous
la forme d'un petit cylindre d'environ 10 mm de long et de 2 ou 3 mm de diamètre
à chaque extrémité duquel sort une patte métallique (que l'on enfichera dans la platine
de prototypage).
Le corps cylindrique porte plusieurs bandes de couleur qui permettent de noter
certaines caractéristiques techniques du composant notamment sa valeur en ohms et 
sa tolérance (la précision de sa valeur).
Le tableau ci-dessous permet de déterminer la valeur d'une résistance d'après la couleur
des bandes qu'elle porte.

![Code couleur résistances.svg](../../Images/Code%20couleur%20r%C3%A9sistances.svg)

Sauriez-vous déterminer les valeurs des résistances ci-dessous (réponse au bas de cette page) ?

![6 résistances de différentes valeurs](https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Electronic-Axial-Lead-Resistors-Array.png/168px-Electronic-Axial-Lead-Resistors-Array.png)

Des aides en ligne sont disponibles pour déterminer ces valeurs, par exemple :
[calculateur de code couleur des résistances chez DigiKey](https://www.digikey.fr/fr/resources/conversion-calculators/conversion-calculator-resistor-color-code).

Toutes les valeurs de résistance ne sont pas communément disponibles, il existe des
[séries](https://fr.wikipedia.org/wiki/CEI_60063) de valeurs usuelles.
La série E3, par exemple, ne comporte que les valeurs :
1 Ω, 2.2 Ω, 4.7 Ω, 10 Ω, 22 Ω, 47 Ω, 100 Ω, 220 Ω, 470 Ω,
1 kΩ, 2.2 kΩ, 4.7 kΩ, 10 kΩ, 22 kΩ, 47 kΩ, 100 kΩ, 220 kΩ, 470 kΩ, 
1 MΩ, 2.2 MΩ, 4.7 MΩ, 10 MΩ, 22 MΩ, 47 MΩ, 100 MΩ, 220 MΩ, 470 MΩ.
La série E3 est obsolète mais c'est la plus courte à recopier.

Une série est constituée des multiples et sous-multiples d'un ensemble de valeurs comprises
entre 10 et 100.
La série E3, par exemple, est formée des multiples et sous-multiples de 3 valeurs : 10, 22 et 47. 

Si l'on reprend l'exemple commencé plus haut, pour protéger notre LED, nous avons besoin d'une
résistance de 130 Ω. Cette valeur n'est pas disponible dans la série E3... Ni dans la série E6,
ni même la E12, elle n'apparaît que dans la série E24.

Dans le contexte du prototypage de circuit employant des microcontrôleurs, les LEDs sont 
souvent protégées par des résistances de 220 Ω. C'est une valeur qui fait partie de toutes les
séries et qui est ainsi supposée plus largement disponible.
Cette pratique offre également une marge de sécurité.

#### Représentation schématique et câblage du circuit

Avant de câbler le circuit sur la platine de prototypage, il peut être utile de tracer
un schéma du circuit.

![Schéma de câblage d'une LED alimentée par un Raspberry Pi Pico](assets/LED_0_sch_wbg.svg)

Les circuits intégrés tels que celui utilisé sont généralement symbolisés
de façon générique par un carré ou un rectangle d'où partent les différentes connexions.

Dans le schéma, on peut voir que la résistance et la LED sont câblées en série,
que la cathode (le pôle négatif) de la LED est connectée à la masse 
du Raspberry Pi Pico qui ne sert qu'à produire la tension de 3.3 V.

![platine de prototypage avec une LED](assets/LED_0_proto_wbg.svg)

Le câblage correspond au schéma.

1. L'anode de la LED, la plus longue patte du composant, le côté triangulaire de la diode sur
le schéma, est connectée à une patte de la résistance de 220 Ω (dont le code de couleur est 
rouge rouge marron).
2. L'autre patte de la résistance est connectée au rail à 3.3 V de la platine de prototypage.
3. La cathode, la patte la plus courte de la LED, la barre de la diode sur le schéma, 
est connectée à un rail de masse de la platine de prototypage.

| 🔴⚠️ Vérifiez toujours deux fois votre câblage avant de brancher l'alimentation. ⚠️ 🔴 |
|----------------------------------------------------------------------------------------|

Le câblage de la LED sur la platine de prototypage utilise deux câbles.
L'un (orange) va du rail 3.3 V à la résistance, l'autre (noir) va de la LED
au rail de masse.
Sauriez-vous construire le même circuit sans utiliser ces deux câbles 
(réponse au bas de cette page) ?

### LED clignotante

Nous avons fait clignoter la LED du Pico, faisons la même chose avec une
autre LED.

Commençons par dessiner le schéma de câblage.
Pour cela, nous devons commencer par choisir quelle broche de la carte
Raspberry Pi Pico nous utiliserons pour commander la LED.

Nous allons utiliser la broche 20 de la carte qui correspond au port
GPIO 15 du microcontrôleur RP2040.

![picow-pinout_wbg.svg](../../Images/picow-pinout_wbg.svg)

Ce choix est un peu arbitraire.
Mais nous préférerons de conserver les ports GPIO 26, 27 et 28 qui
peuvent être utilisés pour convertir des signaux analogiques en numérique.
Nous reviendrons à ce sujet plus tard.

Le schéma du circuit est simple. C'est la broche du Raspberry Pi Pico
que nous avons choisie qui fournit l'énergie pour alimenter la LED.
Le microcontrôleur RP2040 fonctionnant avec une tension de 3.3 V, la broche
produira cette tension quand nous la programmerons à 1 et sera connectée
à la masse quand nous la programmerons à 0.

À noter cependant que si la broche `3V3(OUT)` peut délivrer 300 mA,
ce n'est pas le cas des broches GPIO.
Ces broches délivrent jusqu'à 4 mA mais cela peut être ajusté
par programmation entre 2 et 12 mA.

![LED_1_sch_wbg.svg](assets/LED_1_sch_wbg.svg)

La mise en œuvre du circuit sur la plaque de prototypage est directe.

La broche 20 du Pico est connectée à une résistance de 220 Ω,
elle même connectée à l'anode de la LED. La seconde patte de la LED
(la cathode) est reliée à l'un des rails de masse de la plaque de prototypage
(sans toucher la patte de la résistance).

![LED_1_proto_wbg.svg](assets/LED_1_proto_wbg.svg)

Le code permettant de faire clignoter la LED connectée au GPIO 15 utilise
la classe `PWMControl` contenue dans le module `pwm_control`.
Le module est donc importé au début du programme. Il doit également être
copié dans le répertoire racine du Raspberry Pi Pico.

https://github.com/jlp6k/art-programming_physical-computing/blob/0b90145ba2e12ff4e4c5ed7a42bc5aaebe92f7d6/Ateliers/2_LED/LED_1.py

### Trois LEDs clignotantes

Trois LEDs clignotantes, c'est mieux qu'une seule.











### Solutions des questions

Valeurs de résistances, de haut en bas :

- 4.7kΩ ±5%
- 2.2kΩ ±5%
- 100Ω ±5%
- 1.5kΩ ±5%
- 47Ω ±5%
- 39kΩ ±5%

![6 résistances de différentes valeurs](https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Electronic-Axial-Lead-Resistors-Array.png/168px-Electronic-Axial-Lead-Resistors-Array.png)

Source de l'image : https://en.wikipedia.org/wiki/Resistor#/media/File:Electronic-Axial-Lead-Resistors-Array.png

Version compacte du circuit d'alimentation de la LED :

![Photographie de la version compacte du circuit d'alimentation de la LED](assets/alimentation%20LED.jpg)
