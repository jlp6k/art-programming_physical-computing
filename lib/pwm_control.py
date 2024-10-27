# Ce programme définit la classe PWMControl.

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

        if self._duration_ms == 0:
            self._gpio_pwm.duty_u16(self._goal_duty)
        
        # print("at", self._initial_ticks, "width will change from", self._initial_duty, "to", self._goal_duty, "in", self._duration_ms, "ms")

    def get_width(self):
        """The get_width() returns the current width of the pulse.
        """
        return self._gpio_pwm.duty_u16() / 65535.0
        
    def toggle(self, duration=0.0):
        """The toggle() method changes the desired width of the pulses.
        The new desired width is equal to 1 - the current desired width.

        :param duration: float, durée de la mise à jour en secondes. Si duration=0 alors la mise
        à jour est instantanée.
        :return: None
        """
        self.set_width(1.0 - self.get_goal(), duration=duration)

    def get_goal(self):
        """
        :return: float, the current desired width.
        """
        return self._goal_duty / 65535.0

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


class Servo:
    def __init__(self, gpio,
                 timing_range=(500, 2500), angle_range=(0, 180), start_angle=None,
                 pwm_freq=50, update_rate=50):
        """La méthode d'initialisation de la classe Servo n'a qu'un seul paramètre obligatoire,
        le numéro de la broche du micro-contrôleur à laquelle est relié le servomoteur à piloter.

        Please note that the angle values are processed using an arbitrary unit/scale.
        Hence the angle_range could be (0, 180), (-90, 90), (0, 1), (-1, 1) or any pair of
        values that suits your application.

        Les paramètres sont :
        gpio (int): le numéro de la broche à contrôler.
        timing_range (int, int): les largeurs minimales et maximales (en microsecondes) des impulsions
        envoyées au servomoteurs.
        angle_range (float, float): les positions angulaires minimales et maximales.
        start_angle (float): la position initiale du servomoteur.
        pwm_freq (float): la fréquence porteuse des impulsions (en Hertz).
        update_rate (float): la fréquence (en Hertz) à laquelle la position du servomoteur est mise à jour.
        """
        self._gpio = gpio

        self.min_us, self.max_us = timing_range  # in μs
        self.min_angle, self.max_angle = angle_range  # in whatever unit you want

        self._pwm_freq = pwm_freq
        self._update_rate = update_rate

        if start_angle is None:
            self._angle = (self.min_angle + self.max_angle) / 2
        else:
            self._angle = start_angle

        # Configuration de la broche en sortie.
        self._pin = Pin(self._gpio, Pin.OUT)

        # On crée un objet Timer. Il sera utilisé pour appeler la méthode _update_position de façon répétée.
        self._timer = Timer()

    @staticmethod
    def timing_calibration_helper(servo_gpio, start_timing_us=1500, pwm_freq=50):
        """La méthode statique timing_calibration_helper() sert à trouver les valeurs minimales et
        maximales de durée des impulsions à envoyer au servomoteur. La méthode est intéractive via
        la console Python.

        Elle necessite au moins qu'on lui passe en paramètre le numéro de la broche du micro-contrôleur
        à laquelle est raccordé le servomoteur à tester.
        servo_gpio (int): le numéro de la broche à contrôler.
        start_timing_us (int): la durée initiale (en microsecondes) des impulsions envoyées au servomoteur.
        pwm_freq (float): la fréquence porteuse des impulsions (en Hertz).
        """
        timing_us = int(start_timing_us)
        pwm = PWM(Pin(servo_gpio, Pin.OUT), freq=pwm_freq)

        print("""Usually on a 180 degrees servo:
1000 μs corresponds to the 0 degree position
1500 μs corresponds to the 90 degrees position
2000 μs corresponds to the 180 degree position

Search for the minima and maxima of the timing by decreasing/increasing
the pulse length. When the servo doesn't react anymore to a timing change,
go back a little to a safe value.

Take note of the timing values as well as the angles the servo arm has 
reached at the two extreme positions. Then use them on the timing_range
and angle_range parameters when instantiating a Servo class object.""")

        usage = """
Enter a number to set the timing or
+ to increase pulse timing by 1 μs,
- to decrease pulse timing by 1 μs,
* to increase pulse timing by 10 μs,
/ to decrease pulse timing by 10 μs.
Enter E or e to exit the calibration fonction.
? prints this help.
Other characters are ignored.
"""

        print(usage)

        # On entre dans une boucle dont le programme ne sortira que lorsque la variable in_loop
        # passera de True à False
        in_loop = True
        while in_loop:
            # On calcule duty_u16 à partir de timing_us
            duty_u16 = int(timing_us * pwm_freq * 65535 / 1000000)
            # Et on fait trourner le servo en appliquant la valeur de PWM
            pwm.duty_u16(duty_u16)

            command = input(f"""{timing_us} μs {duty_u16}/65535
Enter command or commands (? prints help): """)

            # La chaîne de caractères command contient les caractères qu'il faut analyser pour effectuer
            # les actions correspondantes.
            try:
                # On essaie de convertir la chaîne de caractères en un entier
                # Si cela ne fonctionne pas, cela déclenchera une exception de type ValueError.
                timing_us = int(command)

            except ValueError:
                # La chaîne command ne représente pas un nombre entier, son contenu est décodé
                for c in command:
                    if c == "+":
                        timing_us += 1
                    elif c == "-":
                        timing_us -= 1
                    elif c == "*":
                        timing_us += 10
                    elif c == "/":
                        timing_us -= 10
                    elif c.lower() == "e":
                        in_loop = False
                    elif c == "?":
                        print(usage)

            finally:
                # Qu'une exception se soit produite ou non, on s'assure que timing_us est toujours positif.
                timing_us = max(0, timing_us)

        pwm.deinit()

    def start(self):
        """Démarre le contrôle du servomoteur"""
        self._gpio_pwm = PWM(self._pin, freq=self._pwm_freq)
        self._timer.init(freq=self._update_rate, mode=Timer.PERIODIC, callback=self._update_position)

    def stop(self):
        """Arrête le contrôle du servomoteur"""
        self._gpio_pwm.deinit()
        self._timer.deinit()

    def get_angle(self):
        """Renvoie la position actuelle du servomoteur.
        Attention la valeur renvoyée ne sera valide qu'après le positionnement du servo.
        Il n'est donc pas possible d'obtenir la position du servo avant l'appel de la méthode start().
        """
        return self._angle

    def set_angle(self, angle):
        """Positionne le servomoteur à l'angle souhaité.
        Attention, cette fonction n'a d'effet qu'après que la méthode start() ait démarré
        le contrôle du servo.
        """
        self._angle = max(self.min_angle, min(self.max_angle, angle))

    def _angle_to_timing_us(self, angle):
        angle_ratio = (angle - self.min_angle) / (self.max_angle - self.min_angle)
        timing_us = self.min_us + ((self.max_us - self.min_us) * angle_ratio)

        return timing_us

    def _timing_us_to_duty_u16(self, timing_us):
        # Calcule la valeur de contrôle de la PWM à partir de la durée d'impulsion
        # duty_u16 = int((timing_us / 1000000) / ((1 / self._freq) / 65535))
        duty_u16 = int(timing_us * self._pwm_freq * 65535 / 1000000)

        return duty_u16

    def _duty_u16_to_timing_us(self, duty_u16):
        # Calcule la durée d'impulsion à partir de la valeur de contrôle de la PWM
        timing_us = duty_u16 * 1000000 / (self._pwm_freq * 65535)

        return timing_us

    def _timing_us_to_angle(self, timing_us):
        timing_us_ratio = (timing_us - self.min_us) / (self.max_us - self.min_us)
        angle = self.min_angle + ((self.max_angle - self.min_angle) * timing_us_ratio)

        return angle

    def _update_position(self, timer):
        # La méthode _update_position est appelée de façon répétée par un timer (c'est une fonction callback).
        # Elle prend (obligatoirement) un paramètre qui recevra le timer qui l'appelle.

        # Met à jour la position du servomoteur.
        self._gpio_pwm.duty_u16(self._timing_us_to_duty_u16(self._angle_to_timing_us(self.get_angle())))


def led_demo(ext_led_gpio):
    # ext_led_gpio is the GPIO number the LED is connected to.

    # Le module random va être utilisé pour faire varier la vitesse de clignotement
    # d'une LED.
    from random import random
    from time import sleep

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


def servo_demo(servo_gpio):
    from time import sleep

    servo = Servo(servo_gpio, timing_range=(500, 2610), angle_range=(0, 205.72), start_angle=101.205, pwm_freq=50)
    servo.start()
    while True:
        for a in range(180):
            servo.set_angle(a)
            sleep(0.005)
        for a in range(180,0,-1):
            servo.set_angle(a)
            sleep(0.005)
        
    servo.stop()


# On teste le contenu de la variable spéciale __name__ afin de déterminer si le module
# est exécuté comme un programme ou importé dans un autre programme.
if __name__ == "__main__":
    # Le programme est inclus dans un gestionnaire d'exception afin de s'arrêter proprement
    # s'il est interrompu.
    from machine import reset

    try:
        # Uncomment the following line to run a demo with an LED wired to GPIO 15
        #led_demo(15)
        
        # Uncomment the following line to run a demo with a servomotor wired to GPIO 8
        Servo.timing_calibration_helper(8)

        # Uncomment the following line to run a demo with a servomotor wired to GPIO 8
        servo_demo(8)

    except KeyboardInterrupt:
        # L'utilisateur a interrompu le programme, on réinitialise la carte.
        reset()
