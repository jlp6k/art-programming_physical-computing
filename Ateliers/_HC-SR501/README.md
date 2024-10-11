## HC-SR501 : capteur de mouvement infrarouge passif

Le HC-SR501 est module électronique capteur infrarouge passif.
Il n'émet lui-même aucun rayonnement (contrairement à un radar, par exemple)
Il se sert de la lumière infrarouge émise par les objets et les personnes ou réfléchie par eux.
Quand il détecte une variation de l'illumination sa sortie change d'état : elle passe de 0 à 1,
c'est-à-dire, dans le cas de ce capteur, de 0 volt à 3.3 volts.

Le champ du capteur HC-SR501 est une portion conique de sphere centrée sur le capteur (qui se trouve
sous le dôme blanc).

Pour plus d'information, consultez les notices (en anglais) :
- [HC-SR501 Passive Infrared (PIR) Motion Sensor](https://www.epitran.it/ebayDrive/datasheet/44.pdf)
- [HC-SR501 PIR Motion Detector](https://www.mpja.com/download/31227sc.pdf)

Le module HC-SR501 se connecte à l'aide de 3 broches :

- GND / masse / 0 volt
- VCC / 4.5 à 20 volts
- OUT / signal en sortie

Le module comporte deux potentiomètres miniatures.
L'un permet de régler la sensibilité du dispositif de 3 à 7 mètres, 
l'autre permet de régler la durée pendant laquelle la sortie reste à un niveau haut (à 3.3 volts) 
lorsqu'un mouvement a été détecté (de quelques secondes à quelques minutes).

Après une détection, la sortie du module passe à l'état haut pendant un temps déterminé par
l'un des potentiomètres.
La position du cavalier (_jumper_ en anglais) détermine comment le module répond à une nouvelle
détection qui surviendrait avant que la sortie soit retournée à l'état bas.
Deux configurations sont possibles :
- les nouveaux mouvements sont ignorés quand la sortie du module est dans l'état haut,
- chaque nouveau mouvement prolonge la durée pendant laquelle la sortie reste à un niveau haut.

![éléments constituants le modules HC-SR105](assets/HC-SR105.svg)

À noter que le capteur a besoin d'une minute environ pour stabiliser son fonctionnement.
Pendant ce temps, il se peut que la sortie change d'état plusieurs fois même en l'absence
de détection.

Il faut également prendre en considération qu'après qu'un mouvement a été détecté et que la sortie
est passée à l'état haut, si aucun mouvement n'est plus détecté, la sortie repasse à l'état bas.
Mais elle restera à l'état bas pendant 3 secondes même s'il y a un mouvement.

La mise en œuvre est très simple :

- GND, la masse, est reliée au rail de masse à 0 volt,
- VCC, la broche d'alimentation est reliée au rail à 5 volts (il faut une tension d'au moins
4.5 volts pour alimenter le module).
- OUT, la sortie est reliée à l'un des GPIO du Pico. Nous choisirons arbitrairement 
la broche 12 / GPIO 9.

![Prototype de circuit utilisant un capteur HC-SR501](assets/HC-SR501_proto_wbg.svg)

Il y a deux manières de surveiller les changements d'état d'un port GPIO :
par scrutation et par interruption.
Commençons par la scrutation (_polling_ en anglais) qui consiste à lire régulièrement
l'état de la broche que l'on veut surveiller et à agir en cas de changement.
```python
from machine import Pin
from time import sleep

# Nous surveillons le port 9 qui est relié au module PIR.
# La broche est configurée en entrée.
pin = Pin(9, Pin.IN)

# La variable previous_state va servir à garder la mémoire de l'état
# de la broche afin de déterminer s'il change.
previous_state = pin.value()
while True:
    # On lit l'état de la broche
    new_state = pin.value()
    # S'il a changé...
    if new_state != previous_state:
        # on affiche un message
        print("L'état à changé, il est à", new_state)
        # et on garde la mémoire du nouvel état
        previous_state = new_state
    
    # On attend 1/10e de seconde
    sleep(0.1)
```

Attention, si le module PIR vient d'être alimenté, son fonctionnement sera perturbé
pendant environ une minute.

Le principe de fonctionnement de ce programme est simple mais il sollicite le microcontrôleur
qui doit souvent interroger l'état de la broche surveillée.
Si le programme doit réaliser simultanément d'autres tâches, il peut devenir compliqué de tout
gérer dans la même boucle.

L'approche par interruption est un peu plus complèxe à mettre en œuvre mais elle est plus
économique en terme de temps passé par le microcontrôleur pour interroger la broche.
Pour mettre en œuvre ce style de programmation, il faut écrire une fonction appelée
routine d'interruption (_Interrupt Service Routine_ en anglais ou ISR).

La routine sera automatiquement appelée lorsque l'état de la broche changera.

Pour simplifier la mise en œuvre nous emploierons la classe `Monitor` du module `monitor`.

```python
from monitor import Monitor

# the take_state() function will take care of the state of the pin
def isr(state):
    # le paramètre 
    # on affiche un message
    print("L'état à changé, il est à", state)

    


```



