from time import sleep

from pwm_control import PWMControl
# Penser à copier le module pwm_control dans le répertoire racine du Raspberry Pi Pico.

# Le programme est inclus dans un gestionnaire d'exception afin de s'arrêter proprement
# s'il est interrompu.
try:
    # La LED est connectée sur la broche 20 qui correspond au GPIO 15.
    ext_led_gpio = 15

    # On crée un objet de classe PWMControl pour gérer le clignotement. On lui indique
    # quelle broche il doit contrôler.
    led = PWMControl(ext_led_gpio)

    while True:
        # On commence par indiquer à l'objet led que la largeur d'impulsion doit être maximale.
        # La LED s'allume à son intensité maximale (compte tenu de sa tension d'alimentation, de la résistance
        # en série avec le LED, etc.
        led.set_width(1.0)
        # Puis le programme attend pendant 1 seconde.
        sleep(1)
        # On commande l'extinction immédiate de la LED.
        led.set_width(0.0)
        # Le programme attend pendant 1 seconde.
        sleep(1)
        # La LED s'éclairera progressivement pendant la prochaine seconde et demi.
        led.set_width(1.0, duration=1.5)
        # Pendant ce temps, le programme attend 1 seconde et demi.
        sleep(1.5)
        # Après ce délai, on commande l'extinction progressive de la LED pendant 1 seconde et demi.
        led.set_width(0.0, duration=1.5)
        # Puis le programme attend pendant 1 seconde et demi.
        sleep(1.5)
        # On recommence depuis le début de la boucle.

    # Normalement l'exécution n'atteint jamais la ligne suivante puisque la boucle est infinie.
    led.deinit()

except KeyboardInterrupt:
    # L'utilisateur a interrompu le programme, on réinitialise la carte.
    machine.reset()
