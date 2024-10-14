## Servomoteur

Un [servomoteur](https://fr.wikipedia.org/wiki/Servomoteur) (ou simplement _servo_)
est un type d'[actionneur](https://fr.wikipedia.org/wiki/Actionneur)
constitué d'un moteur électrique (le plus souvent) et d'un capteur de mouvement liés de façon à 
créer une boucle de rétroaction (_feedback loop_ en anglais).

Ce fonctionnement en circuit fermé va permettre d'actionner le servo afin qu'il atteigne
une position qu'il maintiendra même si une force extérieure est exercée pour lui faire 
changer de position.

Il existe des servomoteurs que toutes tailles et puissances.
Certains produisent un mouvement rotatif, d'autres un mouvement linéaire.

Nous nous intéresserons ici aux servomoteurs employés dans le monde du modélisme (par opposition
avec les servomoteurs industriels).

Les caractéristiques importantes d'un servomoteur sont :

- sa taille et son poids,
- son couple (_torque_ en anglais),
- sa vitesse,
- sa tension d'alimentation,
- son type de circuit interne ; analogique ou numérique.

Le couple d'un servo est exprimé en kg/cm, c'est-à-dire la force disponible ou produite par le
dispositif exprimée en kilogramme à un centimètre de l'axe de rotation.
D'après le fonctionnement du [levier](https://fr.wikipedia.org/wiki/Levier_(m%C3%A9canique)),
la force disponible en s'éloignant de l'axe décroit proportionnellement à la distance.
Ainsi à 2 cm de l'axe la force sera 2 fois moindre qu'à 1 cm.

La vitesse d'un servomoteur rotatif est exprimée seconde par degré (ou un multiple de cette
unité tel qu'en seconde pour 60 degrés).

Le couple et la vitesse dépendent souvent de la tension d'alimentation. Dans les valeurs de tension
admissibles par le servo, la vitesse et le couple sont plus grands quand la tension augmente.

Il existe des servomoteurs dits analogiques ou numériques (_analog or 
digital servos_).
Ils sont mis en œuvre de façons similaires mais les premiers
sont entièrement analogiques tandis que les seconds ont un circuit interne
de contrôle numérique.
Cette différence permet aux servos numériques de recalculer leur position
dans la boucle de rétroaction environ dix fois plus souvent que les 
servos analogiques.

Ainsi, toutes choses étant égales par ailleurs, un servo analogique :

- réagira plus lentement à une modification de sa position,
- il sera moins précis qu'un servo numérique,
- son couple sera généralement moins élevé.

Mais les servos analogiques consomment moins d'énergie, ils sont plus
silencieux et ils coûtent moins cher que les servos numériques.

### Choisir le bon servomoteur

La base de données [servodatabase.com](https://servodatabase.com/servos/all) recense des milliers
de références de servos.
Malheureusement dans les listes présentées sur ce site, les caractéristiques
sont affichées en mesures impériales.
Il faut cliquer sur une référence de servo pour consulter les données dans le système métrique.

La base de données nous permet d'apprendre que l'un des plus petits servomoteurs de hobby (recensé ici),
le [Dymond D1.5](https://servodatabase.com/servo/dymond/d1-5-jst) pèse seulement 1.5 grammes,
il peut exercer une force de 0.14 kg/cm soit 140 g à 1 cm de son axe de rotation
et il fait à peu près le volume de 3 pièces 2 centimes d'euro superposées !

<img alt="Photographie d'un servomoteur Dymond D1.5 à côté d'une pièce de monnaie" src="https://servodatabase.com/images/servos/dymond-d1-5-jst.jpg" title="Dymond D1.5" width="250"/>

À l'autre extrémité de la liste, un servomoteur [MKS HV6150](https://servodatabase.com/servo/mks/hv6150)
de 16.4 g, peut exercer une force de 6.29 kg/cm soit presque 400 fois son propre poids.

<img alt="Photographie d'un servomoteur MKS HV6150" src="https://images.amain.com/cdn-cgi/image/f=auto,width=950/images/large/mks/mks-hv6150.jpg" title="MKS HV6150" width="250"/>

D'autres caractéristiques telles que les matériaux employés pour la construction
du servo ou la nature du moteur électrique ont un effet sur ses performances.

La plupart des servos rotatifs peuvent être positionnés de façon absolue
dans une plage d'angles allant de 0 à 180 degrés avec une précision de l'ordre
du dixième de degré.

Il existe néanmoins des moteurs de type hobby appelé servos à rotation
continue.
Ce ne sont pas à proprement parler des servomoteurs car leur positionnement
n'est pas absolu.
Ils ont de nombreuses caractéristiques mécanique et électronique
communes avec les servos classiques.
Il est d'ailleurs parfois possible de modifier un servo pour en faire 
un servo à rotation continue.

### Commande d'un servomoteur

Un servomoteur de type hobby est piloté à l'aide de 3 connexions.
Deux connexions servent à l'alimentation, la troisième recevra le signal
de contrôle de la position.

![servo-pinout.svg](assets%2Fservo-pinout.svg)

La plupart des fabricants de servos respectent le code couleur ci-dessus qui permet
d'identifier les différentes connexions.

Si le connecteur est branché à l'envers, la masse sera connectée à l'entrée du signal,
le signal sera connecté à la masse du servo : le servo ne fonctionnera pas mais il
ne sera pas endommagé.

La commande d'un servo consiste à envoyer sur l'entrée du signal une impulsion électrique 
toutes les 20 millisecondes pendant un temps variant de 1 ms à 2 ms environ.

Le graphique ci-dessous montre la relation entre la durée des impulsions et la position de l'axe
du servomoteur.

![Graphique montrant la relation entre la durée de l'impulsion et la position de l'axe d'un servo](..%2F..%2FImages%2FServoPWControl_wbg.svg)

### Mise en œuvre d'un servomoteur

Nous avons à notre disposition un clone de servomoteur [SG90](https://servodatabase.com/servo/towerpro/sg90).
Nous allons le câbler afin de de pilôter à partir du Raspberry Pi Pico.

![Prototypage de la connexion d'un servomoteur à un Raspberry Pi Pico W](assets/servo_0_proto_wbg.svg)

Le circuit est simple. Le servo est alimenté par le rail à 5 volts et la masse.
Le signal de contrôle est fourni par le GPIO 8 (broche 11).

Nous allons commencer par un programme court qui fait osciller l'axe du servo
entre ses deux positions extrêmes.

```python
from time import sleep
from pwm_control import Servo

# On crée une instance de la classe Servo pour contrôler un servomoteur à partir
# du GPIO 8. Puis on démarre le contrôle.
servo = Servo(8)
servo.start()

# On fixe le temps de pause entre chaque mouvement.
t = 1  # 1 seconde
while True:
    # On positionne le servo à 0 degré.
    servo.set_angle(0)
    sleep(t)  # Pause
    # On positionne le servo à 180 degrés.
    servo.set_angle(180)
    sleep(t)  # Pause
```

Un servomoteur peut consommer beaucoup de courant, notamment lorsqu'il doit
effectuer un mouvement important à grande vitesse (comme dans le
test ci-dessus).
On veillera toujours à disposer d'une alimentation électrique adaptée au besoin
du ou des servos. Si ce n'est pas le cas, le servo pourrait tirer un courant
si important que le microcontrôleur pourrait n'en avoir plus assez pour son
fonctionnement.
Le phénomène se manifestera par un redémarrage inopiné du microcontrôleur.

Il est toutefois peu probable que le phénomène se produise en alimentant
un micro-servo tel que le SG90 depuis un port USB.

### Servomoteur + potentiomètre

Un montage, tel que celui présenté précédemment, pourrait servir à animer un robot, un automate, ...
Mais il manque d'interactivité. Voici un autre montage dans lequel nous contrôlons la position 
du servo à l'aide d'un potentiomètre.

![Prototypage du contrôle d'un servomoteur à partir d'un potentiomètre](assets/servo_1_proto_wbg.svg)

```python
from time import sleep
from averaging_adc import AveragingADC
from pwm_control import Servo

# On crée un objet de classe AveragingADC.
# Il sert à mesurer la position du potentiomètre connecté au GPIO 26 / ADC0.
adc = AveragingADC(0, average_size=4)

# On crée une instance de la classe Servo pour contrôler un servomoteur à partir
# du GPIO 8. Puis on démarre le contrôle.
servo = Servo(8)
servo.start()

while True:
    # On lit l'entrée analogique et on change l'échelle de la valeur de sorte que la
    # variable target position varie de 0 à 180,
    # La méthode read_unit() renvoie une valeur de type float dans l'intervalle [0..1].
    target_angle = int(adc.read_unit() * 180)
    print("target =", target_angle)
    
    # On fait tourner le moteur.
    servo.set_angle(target_angle)
    
    # 20 lectures du potentiomètre par seconde et mises à jour de la position
    # du servo devraient suffire. On peut donc suspendre un instant l'exécution du programme.
    sleep(1/20)
```

Lorsqu'on tourne le bouton d'une extrémité de sa course à l'autre, le servomoteur est supposé
tourner de 180 degrés.
Mais tous les servos ne sont pas exactement identiques et il peut arriver que l'angle entre les deux
positions extrêmes fasse un peu plus ou un peu moins de 180 degrés.
Pour corriger cela, le classe `Servo` possède la méthode de classe (une méthode que l'on peut appeler
sans avoir préalablement besoin d'instancier un objet de cette classe) `timing_calibration_helper()`.
Le mini-programme ci-dessous montre comment utiliser cette méthode.

```python
from pwm_control import Servo

# On va chercher les durées d'implusion permettant de tourner de 180 degrés.
# Le servo à calibrer est piloté par le GPIO 8 / broche 11 du Raspberry Pi Pico.
Servo.timing_calibration_helper(8)
```

La méthode affiche sur la console comment elle doit être utilisée.
En particulier, elle indique les valeurs minimales et maximales des durées d'impulsion correspondant
habituellement aux positions à 0 et 180 degrés.
Néanmoins, le servomoteur SG90 que nous utilisons dans cet atelier à des valeurs mini/maxi différentes.
Sa fiche technique indique que la durée d'impulsion minimale est de 500 μs et la durée maximale
est de 2400 μs.
