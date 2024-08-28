from pwm_control import PWMControl

# Le programme est inclus dans un gestionnaire d'exception afin de s'arrêter proprement
# s'il est interrompu.
try:
    # Le module random va être utilisé pour faire varier la vitesse de clignotement
    # d'une LED.
    from random import random
    from time import sleep

    # La LED est connectée sur la broche 20 qui correspond au GPIO 15.
    ext_led_gpio = 15

    # On crée un objet de classe PWMControl pour gérer le clignotement. On lui indique
    # quelle broche il doit contrôler.
    led = PWMControl(ext_led_gpio)


    while True:
        led.set_width(1.0)
        sleep(1)
        led.set_width(0.0)
        sleep(1)
        led.set_width(1.0, 1.5)
        sleep(1.5)
        led.set_width(0.0, 1.5)
        sleep(1.5)


    led.deinit()

except KeyboardInterrupt:
    # L'utilisateur à interrompu le programme, on réinitialise la carte.
    machine.reset()
