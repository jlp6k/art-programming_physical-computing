## Démarrage automatique

Quand nous mettons au point un programme en Micropython, nous utilisons Thonny (ou un autre IDE)
pour écrire le code, puis il faut cliquer sur l'icône d'exécution pour le tester.
Mais lorsque le programme est correctement [débogué](https://fr.wiktionary.org/wiki/bogue#fr-nom-5),
il serait souhaitable de pouvoir automatiquement lancer son exécution lorsque le Pico est alimenté.
Il serait ainsi possible de se passer d'ordinateur.

### Séquence de démarrage de Micropython

Une fusée, un ordinateur, une gazinière, ou tout autre appareil complexe nécessite généralement
que ses composants soient activés dans un ordre particulier afin qu'il fonctionne de manière satisfaisante.

Dans le cas d'un microcontrôleur, les composants matériels seront activés dans un ordre généralement 
immuable dépendant du modèle de microcontrôleur (celui du Pico est le RP2040).
L'ordre d'activation des éléments logiciels dépendra du langage de programmation employé.

Pour ce qui est de Micropython, l'ordre d'activation est :

1. `boot.py` est exécuté s'il existe, puis...
2. `main.py` est exécuté s'il existe, puis...
3. La REPL (Read-Eval-Print-Loop) est exécutée.

Pour plus de détails, vous pouvez consulter la page
[Boot Sequence](https://docs.micropython.org/en/latest/reference/reset_boot.html#boot-sequence).

Le code de `boot.py` est chargé de l'initialisation matérielle.
Par exemple, il peut être utilisé pour configurer la connexion WiFi sur le Raspberry Pi Pico W ou
pour préparer un circuit externe connecté au Pico.
Il peut cependant être plus pratique de placer ces codes de configuration/initialisation au début
de `main.py`.

L'exécution de `boot.py` doit se terminer : il ne peut contenir de boucle infinie.

`main.py` contient le code de l'application ou l'appelle s'il est écrit dans un autre fichier.
Ce code sera ainsi automatiquement exécuté au démarrage de Micropython sur le Pico.

Lorsque l'exécution de `main.py` se termine, Micropython va lancer son interpréteur en mode
interactif (la REPL) qui attendra qu'on lui envoie des instructions.

`main.py` (et éventuellement `boot.py`) doit être copié à la racine (`/`) du disque virtuel du Pico.

![Capture partielle d'écran montrant l'opération de copie d'un fichier
intitulé main.py à la racine de la mémoire du Pico](assets/main_upload.jpg)

### Précautions d'usage

Si l'application est automatiquement exécutée au démarrage du Pico, il est important de prendre
des précautions afin qu'une erreur d'exécution du code ne laisse pas le microcontrôleur
dans un état dysfonctionnel dont il ne pourrait sortir puisqu'il y retournerait 
à chaque démarrage.

Le code ci-dessous est à placer dans `main.py`.
Il encadre le fonctionnement de l'application, capture les erreurs et, le cas échéant, 
il réinitialise le microcontrôleur.

```python
import machine, sys

try:
    # Ici commence le code de mon application
    ...
except Exception as e:
    print("Fatal error in main:")
    sys.print_exception(e)

# Après une exception interrompant l'application ou après la fin normale de celle-ci,
# le microcontrôleur est réinitialisé (et l'exécution se poursuit dans la REPL).
machine.reset()
```

Un exemple, complet faisant clignoter la LED du Pico est disponible [dans le fichier `main.py`](main.py).

Une fois le fichier copié à la racine du Pico, l'ordinateur peut être déconnecté et le Pico alimenté avec
une batterie USB (c'est le plus simple) ou par la broche `VSYS`.

### Récupération

Il se pourrait, malgré les précautions proposées ci-dessus, qu'il ne semble pas possible de reprendre la
main sur le Pico : il ne répond pas au bouton stop de Thonny, ni au ctrl+c (la combinaison des touches
control et c).
Nous pourrions dire (en bon franglais) que le Pico est _briqué_ (_bricked_ en anglais).
On dit cela d'un dispositif électronique qui paraît ne plus fonctionner, comme transformé en une
brique inerte.

Mais comme il est impossible de détruire le Pico par une mauvaise programmation, il est possible de retrouver
le fonctionnement normal du Pico.

Pour cela, nous aurons besoin :

1. du _firmware_ spécial de réinitialisation intitulé `flash_nuke.uf2` et disponible à l'adresse
https://datasheets.raspberrypi.com/soft/flash_nuke.uf2. 
2. du _firmware_ Micropython sous la forme d'un fichier `.uf2` disponible
à l'adresse https://www.raspberrypi.com/documentation/microcontrollers/micropython.html#drag-and-drop-micropython.

Attention, le fichier à télécharger dépend de la version de votre microcontrôleur.
Ainsi, un _firmware_ pour Raspberry Pi Pico, ne conviendra pas à un Pico W, à un Pico 2 ou à un Pico 2 W
(et réciproquement).

Installez `flash_nuke.uf2` sur votre Pico, sa mémoire de stockage sera réinitialisée, les fichiers qu'il
contient seront effacés.
Puis réinstallez le _firmware_ Micropython.
Voilà, votre Raspberry Pi Pico est comme neuf. Il reste à le connecter à Thonny.

## Reset

Le verbe _to reset_ en anglais signifie réinitialiser.
Nous avons parfois besoin de redémarrer le Pico, par exemple pour installer son _firmware_ Micropython,
ou pour relancer un programme.
Pour cela, il suffit de débrancher puis rebrancher le câble USB par lequel nous communiquons et alimentons
le Pico.
Mais c'est fastidieux, difficile à faire d'une seule main (l'autre pouvant être occupée) et cela peut finir
par endommager le connecteur USB du Pico ou le câble.
De plus, certains capteurs ne sont pas immédiatement opérationnels lorsque leur
alimentation est (r)établie.
C'est le cas du capteur PIR HC-SR501 (cf. [l'atelier correspondant](../6_HC-SR501/README.md))

La broche numéro 30 appelée `RUN` permet de faire un _reset_ (une réinitialisation) du Pico
sans débrancher le câble USB ou couper l'alimentation.
Pour cela, il faut connecter la broche `RUN` à la masse (le rail à 0 volt).
Cela suspend le fonctionnement du microcontrôleur.
Lorsque la broche sera déconnectée, l'exécution reprendra comme si le microcontrôleur venait d'être alimenté.

Nous pouvons utiliser cette procédure pour réinstaller le _firmware_.

1. Connectez `RUN` à la masse.
2. Appuyez sur le bouton `BOOTSEL`.
3. Déconnectez `RUN` de la masse.
4. Relâchez le bouton `BOOTSEL`.
5. Glissez et déposez le fichier MicroPython `.uf2` sur le volume `RPI-RP2`.
