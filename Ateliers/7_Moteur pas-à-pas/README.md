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

Le moteur 28BYJ-48 compte 64 pas par tour et il est équipé d'un jeu d'engrenage réducteur
1÷64. Cela porte le nombre de pas par tour à 4096. Il existe une version alimentée en 5 volts
et une autre en 12 volts (et l'une ne remplace évidemment pas l'autre).

Le circuit ULN2003 est relativement simple. C'est seulement une interface entre le microcontrôleur,
dont les broches ne peuvent commander que des composants de faible puissance, et le moteur
qui consomme un courant plus important que celui que broches peuvent fournir.

Un autre circuit fréquemment utilisé est l'Allegro A4988 popularisé par le fabricant de
matériel de hobby [Pololu](https://www.pololu.com/product/1182).
Il permet de piloter des moteurs pas-à-pas en utilisant seulement 2 ports gpio (au minimum)
contre 4 ports pour le contrôleur ULN2003.
Par ailleurs, une grande partie des difficultés à surmonter pour coder le mouvement d'un
moteur pas-à-pas en utilisant un circuit ULN2003 est prise en charge par le circuit A4988.
Cela simplifie d'autant la charge du microcontrôleur que vous utilisez.

Pour notre part, nous utiliserons le couple 28BYJ-48 + ULN2003.

### Positionnement d'un moteur pas-à-pas

Nous allons commander la position d'un moteur pas-à-pas en fonction de la position
d'un potentiomètre.

Le moteur n'est pas directement connecté au microcontrôleur, il est connecté au _driver_
(circuit intégré de pilotage) qui lui-même connecté au Pico.
Le moteur est alimenté par le rail à 5 volts (venant du port USB).

![Prototype de circuit de contrôle d'un moteur pas-à-pas 28BYJ-48 à l'aide d'un Raspberry Pico et d'un driver ULN2003](assets%2FStepper_0_proto_wbg.svg)

Le potentiomètre est connecté au rail de masse, au rail à 3.3 volts et à l'entrée ADC0
(gpio 26, broche 31) du Pico.

Le code met en œuvre la classe `ULN2003` du module `stepper_control`.
Cette classe illustre bien l'idée qu'une classe est l'abstraction (ou le modèle informatique)
d'un objet ou de son fonctionnement.
L'instanciation de la classe `ULN2003` permet de décrire comment le _driver_ est connecté 
au Pico et permet de piloter à l'aide de la méthode `step()` le moteur qui y est attaché
(_step_ est la traduction de _pas_ en anglais).


```python
from averaging_adc import AveragingADC
from stepper_control import ULN2003
from helpers import print_every

# On crée un objet de classe AveragingADC.
# Il sert à mesurer la position du potentiomètre connecté au GPIO 26.
adc = AveragingADC(0, average_size=4)

# On crée une instance de la classe ULN2003 pour contrôler un moteur pas-à-pas.
# Le circuit est connecté comme suit :
#   Pico        ULN2003
#   GPIO_13 --> IN_1
#   GPIO_12 --> IN_2
#   GPIO_11 --> IN_3
#   GPIO_10 --> IN_4
stepper_driver = ULN2003(13, 12, 11, 10)


# On choisit arbitrairement la position initiale du moteur comme étant
# la position médiane.
current_position = 0

while True:
    # On lit l'entrée analogique et on translate la valeur de sorte que la variable
    # target position varie de -32767 à 32768, la position médianne du potentiomètre
    # revoyant la valeur 0.
    target_position = adc.read_u16() - (65535 // 2)
    # On divise target_position par 40 afin de réduire la course du moteur pas-à-pas.
    # La division par 40 est choisie arbitrairement. La course totale du moteur
    # est de 1639 pas, c'est-à-dire 820 pas vers la gauche de la position centrale
    # et 819 pas vers la droite.
    target_position //= 40
    
    # On calcule le nombre de pas par rapport à la position courante.
    delta_position = target_position - current_position
    # Le nombre de pas est toujours un entier positif.
    steps = abs(delta_position)
    # Et le signe de delta_position nous indique dans quel sens le moteur doit tourner.
    direction = 1 if delta_position >= 0 else -1
    
    if steps > 0:
        # On affiche une fois par seconde le nombre de pas à faire, 
        # la direction et la position à atteindre
        print_every(f"{steps} pas vers {'==>' if direction >= 0 else '<=='} pour atteindre la position {current_position}", id=0, delay_ms=1000)
    # On fait tourner le moteur.
    stepper_driver.step(steps, direction, full_steps=False)
    # Le moteur est aintenant dans la position à laquelle il devait arriver,
    # on met à jour current_position.
    current_position = target_position
```









