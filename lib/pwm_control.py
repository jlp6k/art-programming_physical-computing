# Ce programme définit la classe PWMControl.

import math

from time import ticks_ms, ticks_diff
from machine import Pin, PWM, Timer


class PWMControl:
    """La classe PWMControl permet de faire varier automatiquement et à une vitesse contrôlée
    la largeur d'impulsion d'une broche en PWM. La largeur d'impulsion est une valeur dans
    l'intervalle 0..1.
    

    La mise à jour de la largeur d'impulsion est linéaire.
    La classe a des limites de fonctionnement imposées par le microcontrôleur.
    """
    def __init__(self, gpio, pwm_freq=1760, update_rate=30):
        """L'initialisation de la classe PWMControl nécessite deux paramètres :
        gpio (int) : la broche du micro-contrôleur qui sera pilotée par la classe.
        pwm_freq (int) : la fréquence du signal.
        update_rate (float) : la fréquence de mise à jour de la broche.
        """
        self._gpio = gpio
        self._pwm_freq = pwm_freq
        self._update_rate = update_rate

        # _initial_ticks and _duration_ms are used to keep track of the time
        # while _initial_duty and _goal_duty keep track of the width
        # for setting and updating the width of the pulsesby the _pulse() method
        # called by the _timer.
        self._initial_ticks = ticks_ms()
        self._duration_ms = 0
        self._initial_duty = self._goal_duty = 0
        
        # Configuration de la broche
        self._pin = Pin(self._gpio, Pin.OUT)

        # On crée un objet Timer. Il sera utilisé pour appeler la méthode _pulse de façon répétée.
        self._timer = Timer()
        
        self.init()
        
    def init(self):
        """Active le contrôle de la broche.
        """
        # TODO: think about the right values of self._initial_ticks, _duration_ms,
        # _initial_duty and _goal_duty.
        # TODO: this may be the right place to allow _freq and _update_rate change.
        self._gpio_pwm = PWM(self._pin, freq=self._pwm_freq, duty_u16=self._initial_duty)
        self._timer.init(freq=self._update_rate, mode=Timer.PERIODIC, callback=self._pulse)
        
    def deinit(self):
        """Désactive le contrôle de la broche.
        """
        # Interrompt la mise à jour de la largeur d'impulsion.
        self._timer.deinit()

        # Interrompt la modulation de la broche.
        self._gpio_pwm.deinit()        

    def set_width(self, width, duration=0.0):
        """Met à jour la largeur d'impulsion en passant de la valeur courante à la valeur
        précisée par le paramètre width.
        width (float): nouvelle valeur de la largeur d'impulsion (dans l'intervalle 0..1).
        duration (float): durée de la mise à jour en secondes. Si duration=0 alors la mise
        à jour est instantanée.
        """
        self._initial_ticks = ticks_ms()
        self._duration_ms = int(duration * 1000)
        self._initial_duty = self._gpio_pwm.duty_u16()
        self._goal_duty = int(width * 65535)
        
        # print("at", self._initial_ticks, "width will change from", self._initial_duty, "to", self._goal_duty, "in", self._duration_ms, "ms")
        
    def get_width(self):
        """
        """
        return self._gpio_pwm.duty_u16() / 65535.0
        
    def _pulse(self, timer):
        # La methode _pulse est appelée de façon répétée par un timer (c'est une fonction callback).
        # Elle prend (obligatoirement) un paramètre qui recevra le timer qui l'appelle.

        # print("at", ticks_ms(), "current duty is", self._gpio_pwm.duty_u16(), end=' ')
        
        if self._duration_ms > 0:
            # Calcul du rapport entre le temps écoulé depuis _initial_ticks et la durée _duration_ms.
            ratio = ticks_diff(ticks_ms(), self._initial_ticks) / self._duration_ms

            # print("ratio is", ratio, end=' ')
            
            # On met à jour la largeur d'impulsion en fonction de ce rapport.
            duty = self._initial_duty + int((self._goal_duty - self._initial_duty) * min(ratio, 1))
        else:
            # On doit appliquer le nouvel objectif de largeur d'impulsion immédiatement.
            duty = self._goal_duty
            
        # print("new duty is", duty)


        # Mise à jour de la largeur d'impulsion.
        self._gpio_pwm.duty_u16(duty)
        
    def __del__(self):
        # La méthode __del__ est appelée quand l'objet est détruit.
        # Elle arrête proprement tout ce qui doit l'être.
        self.deinit()
        

# On teste le contenu de la variable spéciale __name__ afin de déterminer si le module
# est exécuté comme un programme ou importé dans un autre programme.
if __name__ == "__main__":
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
        pwm_ctrl = PWMControl(ext_led_gpio)
        
        
        test_duration = 30  # secondes        
        print_per_second = 10
        
        for s in range(test_duration):
            # On choisit une largeur d'impulsion au hasard
            width = random()  # dans l'intervalle 0..1
            # On applique cette largeur d'impulsion dans un délai spécifié
            delay = random()
            pwm_ctrl.set_width(width, duration=delay)
            print(f"largeur mise à {width:.2f} en {delay:.2f} secondes")
            
            for p in range(print_per_second):
                print(f"largeur courante = {pwm_ctrl.get_width():.2f}")
            
                # L'exécution du programme principal est suspendue
                sleep(1 / print_per_second)
            
        pwm_ctrl.deinit()
            
    except KeyboardInterrupt:
        # L'utilisateur à interrompu le programme, on réinitialise la carte.
        machine.reset()
