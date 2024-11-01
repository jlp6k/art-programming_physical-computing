from machine import Pin
from time import sleep_us, ticks_diff, ticks_us

class HCSR04:
    SPEED_OF_SOUND = 34400  # Speed of sound in air in centimeters per second
    # Leave out any measurement farther than 500 centimeters (the HC-SR04 isn't supposed to
    # be able to measure that far).
    TIMEOUT_US = 1_000_000 * 500 // SPEED_OF_SOUND

    def __init__(self, trig_gpio, echo_gpio):
        self._trig = Pin(trig_gpio, Pin.OUT)
        self._echo = Pin(echo_gpio, Pin.IN)

    def measure(self):
        # Send a 10 microseconds impulse on the trigger input
        self._trig.on()
        sleep_us(10)
        self._trig.off()

        # Then keep track of time passing
        start_time = ticks_us()

        while True:
            current_time = ticks_us()
            if self._echo.value() == 1:
                break
            if ticks_diff(current_time, start_time) >= HCSR04.TIMEOUT_US:
                return None

        while True:
            current_time = ticks_us()
            if self._echo.value() == 0:
                break
            if ticks_diff(current_time, start_time) >= HCSR04.TIMEOUT_US:
                return None

        # Distance computation is done at centimeters resolution
        return ticks_diff(current_time, start_time) * HCSR04.SPEED_OF_SOUND // (1_000_000 * 2)
