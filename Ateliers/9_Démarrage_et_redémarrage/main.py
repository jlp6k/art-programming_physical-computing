import machine, sys

import time


try:
    # Ici commence le code de mon application
    
    # Le code ci-dessous vient de l'atelier sur les LEDs
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
        
except Exception as e:
    print("Fatal error in main:")
    sys.print_exception(e)

# Après une exception qui aurait interrompu l'application ou après la fin normale de celle-ci,
# le microcontrôleur est redémarré.
machine.reset()
