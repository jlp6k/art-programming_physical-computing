## Potentiomètre

Dans l'atelier sur les LED, nous avons utilisé des résistances pour
abaisser la tension.

La représentation schématique ci-dessous de la combinaison de deux résistances
forme ce que l'on appelle un (pont) [diviseur de tension](https://fr.wikipedia.org/wiki/Diviseur_de_tension). 
En vertu de la loi d'Ohm, nous pouvons déduire que la tension entre A et B est proportionnelle 
à la tension entre A et C et au rapport des valeurs des résistances.

```mermaid
flowchart LR
    left(("A")) --- A[résistance 1]
    A --- B(("B"))
    B --- C[résistance 2]
    C --- right(("C"))
```

Ainsi, quand la résistance 1 est nulle, la tension en B est identique à celle
de A et quand la résistance 2 est nulle, la tension en B est identique à celle
de C. Quand les résistances 1 et 2 sont identiques, la tension mesurée entre
A et B sera égale à celle mesurée entre B et C et ces tensions seront 
la moitié de celle mesurée entre A et C.

Un potentiomètre est un composant à trois bornes qui permet de faire varier
de façon continue les résistances 1 et 2 : la résistance 1 croît
quand la resistance 2 décroît (et inversement).

Les potentiomètres sont généralement représentés schématiquement par les
symboles ci-dessous ([IEC](https://fr.wikipedia.org/wiki/Commission_%C3%A9lectrotechnique_internationale)
à gauche, [ANSI](https://fr.wikipedia.org/wiki/American_National_Standards_Institute) à droite).

![Symbole potentiomètre IEC](../../Images/symbole_potentiometre_IEC.svg)
![Symbole potentiomètre ANSI](../../Images/symbole_potentiometre_US.svg)

Ces schémas permettent également d'entrevoir la disposition mécanique des
potentiomètres : un point de contact est déplacé à l'aide d'un axe
sur une piste résistive.
La résistance entre le point de contact lié à B et
les bornes A et C est proportionelle à la distance du point de contact
aux extrémités A et C de la piste résistive.

![potentiomètre](../../Images/potentiometre.svg)

Les potentiomètres peuvent avoir de nombreuses formes et dimensions
qui diffèrent selon l'usage auxquels ils sont destinés.
Certains sont miniatures et destinés à être directement soudés à un circuit
imprimé et réglés une fois pour toutes. 
La plupart des potentiomètres sont rotatifs mais certains ont un curseur
qui glisse dans un rail.

![potentiomètres.png](../../Images/potentiometres.png)

Les caractéristiques électriques d'un potentiomètre sont sa résistance
totale, sa puissance et sa courbe de variation. Ce dernier point détermine
comment la résistance varie lorsqu'on déplace le curseur : 
- linéairement, la résistance mesurée entre A et B varie en proportion constante de l'angle 
de rotation,
- logarithmiquement, la résistance varie rapidement au début de la course et plus lentement 
à la fin.

### Régler l'intensité d'une LED

Nous pouvons régler l'intensité lumineuse d'une LED à l'aide de code mais un
potentiomètre permet également de régler la tension d'alimentation d'une LED
et donc sa luminosité.

Le schéma ci-dessous met en œuvre un potentiomètre et une LED.
Une résistance demeure nécessaire pour protéger la LED car lorsque le bouton
du potentiomètre sera tourné à fond à droite, la résistance du circuit
qui conduit à l'anode (borne +) de la LED sera nulle.

![Schéma d'alimentation d'une LED avec tension variable via un potentiomètre](assets/Pot_0_sch_wbg.svg)

![Platine de prototypage de la LED et son alimentation variable](assets/Pot_0_proto_wbg.svg)

#### Avec deux LEDs

Le montage précédent démontre comment la tension d'alimentation varie en fonction de la position
du potentiomètre.
Mais nous l'avons vu, un potentiomètre a (d'une certaine façon) deux résistances, l'une croissant
quand l'autre décroît.
Le tableau ci-après présente les valeurs des deux résistances d'un potentiomètre linéaire de 10kΩ
quand on tourne le bouton.
À partir des valeurs de ces deux résistances, et connaissant la tension d'alimentation du circuit,
on peut calculer les tensions aux bornes du potentiomètre.

![Tableau et graphiques montrant comment la résistance et la tension varient aux bornes du potentiomètre quand on tourne le bouton](assets/PotCalc.svg)

Vous pouvez vérifier expérimentalement les valeurs de ce tableau à l'aide d'un multimètre.

Le câblage de deux LEDs exploitant les deux résistances d'un potentiomètre ne présente pas
de difficulté. Il faut cependant bien prendre garde à la polarité (l'orientation des bornes)
des LEDs :
- La `LED1` est branchée à la masse d'un côté (cathode -) et à la borne centrale du potentiomètre 
de l'autre (anode +).
- La `LED2` est branchée à la borne centrale du potentiomètre d'un côté (cathode -) et au rail à 3.3V
de l'autre (anode +).

![Schéma d'alimentation de 2 LEDs avec tension variable via un potentiomètre](assets/Pot_1_proto_wbg.svg)
![Platine de prototypage de 2 LEDs avec alimentation variable](assets/Pot_1_sch_wbg.svg)

En position médiane du potentiomètre, la tension d'alimentation des LEDs est la moitié de la
différence de potentiel entre le rail de masse à 0 V et celui à 3.3 V, c'est-à-dire 1.65 V.
C'est une tension presque insuffisante pour allumer l'une ou l'autre des 2 LEDs.
Cela signifie que l'on est très proche de la tension de seuil des deux LEDs (en dessous de cette
tension, elles ne s'allumeraient pas du tout).

### _Analog to Digital Converter_

Nous allons maintenant utiliser une fonction très utile de beaucoup de microcontrôleurs et
présente dans le RP2040.
Il s'agit de l'ADC (_Analog to Digital Converter_), le [convertisseur analogique-numérique](https://fr.wikipedia.org/wiki/Convertisseur_analogique-num%C3%A9rique).
C'est un composant qui permet de mesurer la tension appliquée à une broche du microcontrôleur
afin d'obtenir une valeur numérique proportionnelle à cette tension.

![Identification des broches du Raspberry Pi Pico](../../Images/picow-pinout_wbg.svg)

Le microcontrôleur RP2040 possède un convertisseur AD qui peut gérer jusqu'à 5 entrées 
analogiques dont 4 sont disponibles sur les broches du microcontrôleur.
La 5e entrée analogique est utilisée par le microcontrôleur pour mesurer sa température 
de fonctionnement. Elle ne peut être utilisée pour un autre usage.
Les 4 entrées restantes sont disponibles sur les broches GPIO 26 à 29.
Néanmoins, sur la carte Raspberry Pi Pico le port GPIO 29 est utilisé pour la mesure de 
la tension d'entrée `VSYS` et sur le Raspberry Pi Pico W le GPIO 29 est également utilisé
pour la gestion du module radio WiFi et Bluetooth.
Le GPIO 29 ne pourra donc pas être utilisé pour nos applications.

Par ailleurs, les entrées analogiques ne peuvent être simultanément employées dans un
usage numérique (cf. [1_Base/Brochage du Pico](https://github.com/jlp6k/art-programming_physical-computing/blob/main/Ateliers/1_Base/README.md#brochage-du-pico)).

#### Résolution

Le convertisseur analogique-numérique du RP2040 a une résolution de 12 bits.
Cela signifie qu'il peut produire des valeurs entre 0 et 4095 pour des 
tensions d'entrée allant de 0 V à 3.3 V.
Il faut néanmoins modérer cette résolution car, dans les faits, le niveau 
de bruit du convertisseur, les défauts de la tension de référence, etc. 
sont tels que la résolution effective 
([ENOB](https://en.wikipedia.org/wiki/Effective_number_of_bits))
est plutôt de l'ordre de 8.7 bits 
(cf. [RP2040 datasheet](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf), section 4.9.3).

En pratique, cela signifie que la valeur de 12 bits obtenue après une
mesure comporte 3.3 bits d'erreur : par exemple la valeur 2720 devrait être
interprétée comme étant en réalité égale à 2720 ± 4.925.
Si l'on rapporte cela à la tension mesurée cela représente
une erreur de l'ordre de ±0.004 V.

### Mesure de la tension avec le Pico

Nous allons mesurer la tension sortant de la borne médiane d'un potentiomètre en utilisant
l'entrée ADC0 (GPIO 26 / broche 31 de la carte Raspberry Pi Pico ou Pico W).

Le câblage est simple. Comme précédemment nous connectons les deux bornes latérales 
du potentiomètre, l'une au rail de masse, l'autre au rail à 3.3V.
La broche médiane du potentiomètre est connectée à l'entrée ADC0 du Pico.

| 🔴⚠️ Ne jamais connecter une broche d'entrée du Raspberry Pi Pico à une tension supérieure à 3.3 V ⚠️ 🔴 |
|----------------------------------------------------------------------------------------------------------|

![Pot_3_proto_wbg.svg](assets/Pot_3_proto_wbg.svg)

![Pot_3_sch_wbg.svg](assets/Pot_3_sch_wbg.svg)

MicroPython propose d'accéder à l'ADC du RP2040 à l'aide de la classe `ADC`.
Pour créer un objet/une instance de cette classe, il faut appeler le constructeur de la classe
en lui passant un objet de la classe `Pin`.
Ensuite, pour lire la valeur mesurée sur l'entrée correspondante, il suffit d'appeler
la méthode `read_u16()`.
Notez que les valeurs renvoyées par la méthode `read_u16()` sont des entiers non signés sur 16 bits,
cela signifie que les valeurs rendues sont dans l'intervalle 0..65535.

```python
from machine import ADC, Pin
from time import sleep

# On crée un objet de classe ADC à partir d'un objet de classe Pin en précisant le numéro
# de l'entrée utilisée (ici le GPIO 26).
adc = ADC(Pin(26))
# Alternativement, il est possible de passer le numéro de l'ADC à la place du numéro du GPIO.
# Ainsi, ADC(0) est équivalent à ADC(Pin(26)).

# Dans une boucle infinie,..
while True:
    # On lit la valeur mesurée à l'entrée
    raw_value = adc.read_u16()
    # et on la convertit en volts.
    raw_volt_value = 3.3 * raw_value / 65535
    # Puis on affiche les valeurs sur la console (avec 3 décimales pour les volts).
    print(f"{raw_value} {raw_volt_value:.3f} V")
    # On attend 1/4 de seconde avant de recommencer
    sleep(1/4)
```

Les valeurs renvoyées par la méthode `read_u16()` sont obtenues à partir des valeurs 
sur 12 bits produites par l'ADC [décalées de 4 bits vers la gauche](https://fr.wikipedia.org/wiki/Op%C3%A9ration_bit_%C3%A0_bit#D%C3%A9calages_de_bit)
(en réalité, c'est un peu plus complexe).
Si cela vous intéresse vous pouvez aller voir le code source en C de la fonction `adc_config_and_read_u16` de la 
[bibliothèque `machine_adc.c` pour le microcontrôleur RP2040](https://github.com/micropython/micropython/blob/master/ports/rp2/machine_adc.c).

```python
from machine import ADC, Pin
from time import sleep

# On crée un objet de classe ADC à partir d'un objet de classe Pin en précisant le numéro
# de l'entrée utilisée (ici le GPIO 26).
adc = ADC(Pin(26))

# Dans une boucle infinie,..
while True:
    # On lit la valeur mesurée à l'entrée
    raw_value = adc.read_u16()
    # et on la convertit en volts.
    raw_volt_value = 3.3 * raw_value / 65535

    # On réduit la valeur lue en la décalant de 8 bits vers la droite
    # (4 bits pour revenir à des valeurs sur 12 bits + (3.3 bits arrondis à) 4 bits pour l'erreur).
    reduced_value = raw_value >> 8
    reduced_volt_value = 3.3 * reduced_value / (65535 >> 8)

    # Puis on affiche les valeurs sur la console (avec 3 décimales pour les volts).
    print(f"{raw_value} {raw_volt_value:5.3f} V\t{reduced_value} {reduced_volt_value:5.3f} V")
    # On attend 1/4 de seconde avant de recommencer
    sleep(1/4)
```

Ce programme produit un affichage sur la console du genre de celui ci-dessous lorsque le bouton
du potentiomètre est tourné à fond à gauche.
Chaque exécution produit un résultat légèrement différent car les variations de valeurs mesurées
sont essentiellement aléatoires.

```
>>> %Run -c $EDITOR_CONTENT

  MPY: soft reboot
  288 0.015 V	1 0.013 V
  256 0.013 V	1 0.013 V
  272 0.014 V	1 0.013 V
  208 0.010 V	0 0.000 V
  224 0.011 V	0 0.000 V
  288 0.015 V	1 0.013 V
  272 0.014 V	1 0.013 V
  224 0.011 V	0 0.000 V
```

Nous notons malheureusement que, les valeurs de la colonne de droite fluctuent,
même divisées de moitié par rapport aux valeurs de la colonne de gauche.

Une technique pour lisser les variations de l'ADC consiste à faire la
moyenne des dernières mesures.
C'est ce que propose la classe `AveragingADC` du module `averaging_adc`.

```python
from time import sleep
from averaging_adc import AveragingADC

# On crée un objet de classe AveragingADC.
# Par défaut, la moyenne est calculée sur les 16 dernières mesures...
# Dans cet exemple, nous ferons la moyenne sur les 128 dernières mesures.
adc = AveragingADC(0, average_size=128)

# Dans une boucle infinie...
while True:
    # On affiche les résultats de mesures sur la console (avec 3 décimales pour les volts).
    # Les méthodes read_u16() et volts() renvoient la moyenne des mesures tandis que les méthodes
    # raw_u16() et raw_volts() renvoient la mesure instantanée.
    print(f"{adc.raw_u16()} {adc.raw_volts():5.3f} V\t{adc.read_u16()} {adc.volts():5.3f} V")
    # On attend 1/4 de seconde avant de recommencer
    sleep(1 / 4)
```

Le paramètre `average_size`du constructeur de la classe `AveragingADC` peut être un entier 
positif quelconque (à concurrence de la mémoire disponible).
Cependant, le lissage produit à pour effet de ralentir  les variations puisqu'il faut 
`average_size` nouvelles mesures pour changer la moyenne.

Ce phénomène peut être minimisé en multipliant le nombre de mesures (par rapport aux mesures
dont on a réellement besoin) et en en faisant la moyenne.
Cette technique s'appelle _oversampling_.
Le programme suivant illustre sa mise en œuvre à l'aide de la classe `AveragingADC`.

```python
from time import sleep
from averaging_adc import AveragingADC

# On crée un objet de classe AveragingADC.
# Par défaut, la moyenne est calculée sur les 16 dernières mesures...
# Dans cet exemple, nous ferons la moyenne sur les 128 dernières mesures.
adc = AveragingADC(0, average_size=128)

# Dans une boucle infinie...
while True:
    # On affiche les résultats de mesures sur la console (avec 3 décimales pour les volts).
    # Les méthodes read_u16() et volts() renvoient la moyenne des mesures tandis que les méthodes
    # raw_u16() et raw_volts() renvoient la mesure instantanée.
    print(f"{adc.raw_u16()} {adc.raw_volts():5.3f} V\t{adc.read_u16()} {adc.volts():5.3f} V")
    # On attend 1/4 de seconde avant de recommencer... Mais pendant ce temps,
    # le programme fait 100 mesures.
    for _ in range(100):
        adc.raw_u16()
        sleep(1 / 400)
```

### Choix de la résistance du potentiomètre

Les potentiomètres que nous utilisons ont une résistance de 10kΩ.
Bien que ce soit plutôt le rapport des résistances aux extrémités du
potentiomètre qui nous intéresse pour former un pont diviseur de tension,
la valeur totale de la résistance du potentiomètre n'est pas choisie au hasard.

Les bornes extrèmes du potentiomètre étant reliées aux rails 0V et 3.3V, le courant qui traverse 
le potentiomètre est `I = U/R = 3.3 / 10000 = 330µA` (ou 1.089mW).
Pour notre usage, ce courant est négligeable, une pile AA 1.5V alcaline pourrait le fournir 
pendant au moins 150 jours.

En revanche, si nous utilisions des potentiomètres de 100Ω, le courant consommé par cette partie
de notre circuit serait de 33mA (ou 108.9mW), ce qui est inutilement élevé puisque nous avons
seulement besoin de mesurer la tension et non alimenter un dispositif.

Inversement, il n'est pas non plus toujours opportun d'augmenter la résistance du potentiomètre
pour diminuer la consommation du circuit.
En effet, certains convertisseurs analogique-numérique fonctionnent à l'aide d'un circuit
capacitif, c'est par exemple le cas des cartes Arduino qui pourraient ne pas fonctionner de façon
optimale pour mesurer la tension issue d'un potentiomètre de plus de 10kΩ, le courant 
traversant le convertisseur serait insuffisant.

### Régler le clignotement d'une LED

Nous allons maintenant écrire un programme qui fera clignoter une LED à une fréquence réglée à
l'aide d'un potentiomètre.

- La LED sera connectée au GPIO 19.
- Le potentiomètre sera connecté au GPIO 26.

```python
from time import sleep
from averaging_adc import AveragingADC
from pwm_control import PWMControl

# On crée un objet de classe AveragingADC.
# Par défaut, la moyenne est calculée sur les 16 dernières mesures...
# Dans cet exemple, nous ferons la moyenne sur les 128 dernières mesures.
adc = AveragingADC(0, average_size=128)

# La LED est connectée sur la broche 20 qui correspond au GPIO 15.
led_gpio = 15

# On crée un objet de classe PWMControl pour gérer le clignotement. On lui indique
# quelle broche il doit contrôler.
led = PWMControl(led_gpio)

# Dans une boucle infinie...
while True:
    # On calcule une valeur comprise entre 0 (quand adc.read_u16() renvoie 0) 
    # et 1 (quand adc.read_u16() renvoie 65535).
    # La période du cycle de clignotement de la LED varie donc de 0 à 2 secondes.
    half_period_duration = adc.read_u16() / 65535
    # On affiche la durée de la demi période
    print(half_period_duration)
    # On bascule l'état de la LED
    led.toggle()
    # Puis le programme s'interrompt pour la durée de la demi période.
    sleep(half_period_duration)
```

Ce programme fonctionne mais il manque de réactivité quand la période est longue.
Pourquoi ?

Ce programme lisse les valeurs mesurées à la sortie du potentiomètre en faisant la moyenne
des 128 dernières valeurs lues... Et il lit une nouvelle valeur à chaque appel de
la méthode `read_u16()`.

Quand la valeur lue est proche de 0 le délai entre deux lectures est court
(comme le délai entre deux changement d'état de la LED).
En revanche, quand la valeur renvoyée par `read_u16()` est proche du maximum,
le délai entre deux lectures est long (jusqu'à 1 seconde) de même que l'évolution
des valeurs renvoyées.
Il faudra donc près de 2 minutes pour passer d'un clignotement lent à
un clignotement rapide.

Sauriez-vous améliorer le temps de réponse du programme à un changement
de la position du potentiomètre en ne modifiant qu'une seule ligne du programme ?
(Solution en bas de page.)

Une bonne solution pour résoudre le problème de réactivité du contrôle de la LED
à partir du potentiomètre consiste à lire l'ADC indépendamment de la mise à jour de
l'état de la LED.

Pour cela nous allons utiliser les fonctions `ticks_ms()` et `ticks_diff()` du module
`time` (cf. [documentation de MicroPython](https://docs.micropython.org/en/latest/library/time.html#time.ticks_ms))

La fonction `ticks_ms()` renvoie une valeur correspondant au nombre de millisecondes
depuis un moment fixe dans le passé (par exemple le démarrage du RP2040).
La fonction `ticks_diff()` permet de calculer le temps écoulé entre deux valeurs renvoyées
par `ticks_ms()`.

Par exemple, si on exécute le programme suivant (en le collant dans la console par exemple),
il affichera deux valeurs entières correspondant à `t0` et `t1` puis 1000, le temps écoulé
entre `t0` et `t1`.

```python
from time import ticks_ms, ticks_diff, sleep

t0 = ticks_ms()
sleep(1)  # on dort pendant 1 seconde
t1 = ticks_ms()
print(t0, t1, ticks_diff(t1, t0))
```

Nous pouvons donc exploiter ces fonctions pour déterminer quand changer l'état de la LED

```python
from time import sleep_ms, ticks_ms, ticks_diff
from averaging_adc import AveragingADC
from pwm_control import PWMControl

# On crée un objet de classe AveragingADC.
# Par défaut, la moyenne est calculée sur les 16 dernières mesures...
# Dans cet exemple, nous ferons la moyenne sur les 128 dernières mesures.
adc = AveragingADC(0, average_size=128)

# La LED est connectée sur la broche 20 qui correspond au GPIO 15.
led_gpio = 15

# On crée un objet de classe PWMControl pour gérer le clignotement. On lui indique
# quelle broche il doit contrôler.
led = PWMControl(led_gpio)

# On note le moment du début de la première demi période.
state_start_ticks = ticks_ms()
# Dans une boucle infinie...
while True:
    # On calcule une valeur comprise entre 0 (quand adc.read_u16() renvoie 0) 
    # et 1 (quand adc.read_u16() renvoie 65535).
    # La période du cycle de clignotement de la LED varie donc de 0 à 2000 millisecondes.
    half_period_duration = adc.read_u16() * 1000 / 65535
    
    # On calcule le temps (en millisecondes) écoulé depuis le début de
    # la demi période courante. Si le temps écoulé depuis le début de la demi période
    # est supérieur (on peut effectivement avoir dépassé la durée souhaitée) ou égal 
    # à la durée de la demi période...
    if ticks_diff(ticks_ms(), state_start_ticks) >= half_period_duration:
        # Alors on bascule l'état de la LED
        led.toggle()
        # Et on note le moment du début de cette nouvelle demi période.
        state_start_ticks = ticks_ms()
        # Et on affiche la durée de la demi période pour information
        print(half_period_duration)
    
    # Puis le programme s'interrompt pendant 10 millisecondes.
    sleep_ms(10)
```

Si on fait une mesure du potentiomètre toutes les 10ms (la durée approximative d'un tour
de la boucle, cela fait 100 mesures par seconde ce qui est probablement assez pour notre
usage.
Toutefois, si on prend en compte que la valeur renvoyée par notre instance de
`AveragingADC` est calculée sur une moyenne de 128 valeurs, alors il faudra environ
1.28 secondes pour passer atteindre la valeur souhaitée lorsqu'on tourne le bouton du
potentiomètre.

Dans les programmes précédents, nous changeons l'état de la LED de façon instantanée.
Cependant, la classe `PWMControl` permet de faire varier progressivement l'intensité
lumineuse apparente de la LED.
Sauriez-vous améliorer le programme précédent afin que le clignotement de la LED soit
progressif, c'est-à-dire qu'elle s'allume progressivement et qu'elle s'éteigne de même,
tandis que l'utilisateur réglera la vitesse à laquelle cela se produit avec
le potentiomètre ?
(Solution en bas de page.)


### Solutions des questions

Voici comment modifier (très simplement) le programme de contrôle de la vitesse de
clignotement d'une LED afin que la réaction au réglage du potentiomètre soit plus rapide.

Remplacer la ligne :

```python
adc = AveragingADC(0, average_size=128)
```

par

```python
adc = AveragingADC(0, average_size=1)
```


```python
from time import sleep_ms, ticks_ms, ticks_diff
from averaging_adc import AveragingADC
from pwm_control import PWMControl

# On crée un objet de classe AveragingADC.
# Par défaut, la moyenne est calculée sur les 16 dernières mesures...
# Dans cet exemple, nous ferons la moyenne sur les 128 dernières mesures.
adc = AveragingADC(0, average_size=128)

# La LED est connectée sur la broche 20 qui correspond au GPIO 15.
led_gpio = 15

# On crée un objet de classe PWMControl pour gérer le clignotement. On lui indique
# quelle broche il doit contrôler.
# Il est nécessaire d'augmenter la fréquence à laquelle l'intensité de la LED est mise
# à jour sinon lorsque la LED clignote rapidement les variations n'auront pas le temps
# de s'effectuer.
led = PWMControl(led_gpio, update_rate=150)

# On note le moment du début de la première demi période.
state_start_ticks = ticks_ms()
# Dans une boucle infinie...
while True:
    # On calcule une valeur comprise entre 0 (quand adc.read_u16() renvoie 0) 
    # et 1 (quand adc.read_u16() renvoie 65535).
    # La période du cycle de clignotement de la LED varie donc de 0 à 2000 millisecondes.
    half_period_duration = adc.read_u16() * 1000 / 65535
    
    # On calcule le temps (en millisecondes) écoulé depuis le début de
    # la demi période courante. Si le temps écoulé depuis le début de la demi période
    # est supérieur (on peut effectivement avoir dépassé la durée souhaitée) ou égal 
    # à la durée de la demi période...
    if ticks_diff(ticks_ms(), state_start_ticks) >= half_period_duration:
        # Alors on bascule l'état de la LED, en indiquant en combien de temps
        # cela doit se produire = la durée de la demi période exprimé en secondes.
        led.toggle(duration=half_period_duration/1000)
        # Et on note le moment du début de cette nouvelle demi période.
        state_start_ticks = ticks_ms()
        # Pour information, on affiche la durée de la demi période ainsi que la fréquence
        # du clignotement.
        print(f"{half_period_duration:.3f}ms {500/half_period_duration:.3f}Hz")
    
    # Puis le programme s'interrompt pendant 10 millisecondes.
    sleep_ms(10)
```