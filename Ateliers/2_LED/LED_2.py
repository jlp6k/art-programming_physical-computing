from machine import Pin
import machine

from pwm_control import PWMControl
from scene_control import SceneControl
# Penser à copier les deux modules importés dans le répertoire racine du Raspberry Pi Pico.

# Le programme est inclus dans un gestionnaire d'exception afin de s'arrêter proprement
# s'il est interrompu.
try:

    # La LED bleue est connectée sur la broche 19 qui correspond au GPIO 14.
    # La LED verte est connectée sur la broche 20 qui correspond au GPIO 15.
    blue_led_gpio = 14
    green_led_gpio = 15

    # On crée un objet de classe PWMControl pour gérer le clignotement. On lui indique
    # quelle broche il doit contrôler.
    green_led = PWMControl(green_led_gpio)
    blue_led = PWMControl(blue_led_gpio)

    # La LED qui équipe le Raspberry Pi Pico W ne peut être contrôlée en PWM.
    onboard_led = Pin("LED", Pin.OUT)

    # Création d'instances de SceneControl.
    # Une même instance de SceneControl peut contrôler plusieurs LED (ou appeler des fonctions quelconques).
    # Cependant toutes les entités contrôlées fonctionnent dans une même boucle temporelle c'est-à-dire la même
    # fréquence d'activation.
    # scene_a va être utilisé pour contrôler la LED sur la carte Raspberry Pi Pico et la LED verte.
    scene_a = SceneControl()
    # scene_b contrôlera la LED blue.
    scene_b = SceneControl()

    # Quand les méthodes start() des objets scene_a et scene_b seront appelées,
    # les scénarios correspondant seront exécutés.

    # On n'appelle pas la méthode toggle de l'objet onboard_led. À la place, on programme son exécution immédiate
    # au moment où la méthode start sera appelée.
    scene_a.add_call_after(0, onboard_led.toggle)
    scene_a.add_call_after(1000, onboard_led.toggle)
    scene_a.add_call_after(2000, onboard_led.toggle)
    scene_a.add_call_after(3000, onboard_led.toggle)
    scene_a.add_call_after(0, green_led.set_width, 1.0)
    scene_a.add_call_after(500, green_led.set_width, 0.0, duration=1.0)
    scene_a.add_call_after(1500, green_led.set_width, 1.0, duration=1.0)
    scene_a.add_call_after(2500, green_led.set_width, 0.0)
    # Enfin au bout de 3 secondes, la méthode reinit() sera appelée et le scénario se reproduira
    scene_a.add_call_after(3000, scene_a.reinit)
    # On notera que le fonctionnement de la LED du Pico et de la LED verte est synchronisé et se reproduit
    # à l'identique toutes les 3 secondes.

    # On fait de même avec un autre scénario pour contrôler la LED bleue.
    scene_b.add_call_after(0, blue_led.set_width, 1.0)
    scene_b.add_call_after(500, blue_led.set_width, 0.0)
    scene_b.add_call_after(1000, blue_led.set_width, 1.0)
    scene_b.add_call_after(1500, blue_led.set_width, 0.0)
    scene_b.add_call_after(2000, blue_led.set_width, 1.0)
    scene_b.add_call_after(2500, blue_led.set_width, 0.0)
    scene_b.add_call_after(3000, blue_led.set_width, 1.0, duration=0.5)
    scene_b.add_call_after(3500, blue_led.set_width, 0.0, duration=0.5)
    scene_b.add_call_after(3501, scene_b.reinit)
    # La période de fonctionnement de la scene_b est de 3,5 secondes.
    # Les 2 dernières tâches sont espacées de 1ms pour garantir que l'appel de scene_b.reinit()
    # sera effectué après l'appel de blue_led.set_width(0.0, duration=0.5)

    # On démarre les scénarios.
    scene_a.start()
    scene_b.start()

except KeyboardInterrupt:
    # L'utilisateur a interrompu le programme, on réinitialise la carte.
    machine.reset()
