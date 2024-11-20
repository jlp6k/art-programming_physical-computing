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
        """The measure() method returns the measured distance in centimeters or -1
        if the distance to measure exceeds the range of the sensor.
        """
        # Send a 10 microseconds impulse on the trigger input
        self._trig.on()
        sleep_us(10)
        self._trig.off()

        # Then keep track of time passing
        start_time = ticks_us()

        # Wait for the echo to get back
        while True:
            current_time = ticks_us()
            if self._echo.value() == 1:
                break
            if ticks_diff(current_time, start_time) >= HCSR04.TIMEOUT_US:
                return -1

        # The time the echo pin is at 1 is proportional to the distance measured
        echo_start_time = ticks_us()

        while True:
            current_time = ticks_us()
            if self._echo.value() == 0:
                break
            if ticks_diff(current_time, start_time) >= HCSR04.TIMEOUT_US:
                return -1

        # Distance computation is done at centimeters resolution
        return ticks_diff(current_time, echo_start_time) * HCSR04.SPEED_OF_SOUND // (1_000_000 * 2)


if __name__ == "__main__":
    from time import sleep

    # The HC-SR04 needs two GPIOs:
    #     - the trigger initiates the measurement
    #     - the echo returns the measurement.

    trigger_gpio = 20
    echo_gpio = 19

    # Create an instance of the HC-SR04 class. It will handle the measurement process.
    hcsr04 = HCSR04(trigger_gpio, echo_gpio)

    # Take a measurement once per second.
    while True:
        # Call the measure() method, it returns the measured distance in centimeters
        # or -1 if the distance exceeds the HC-SR04 range.
        distance_cm = hcsr04.measure()

        if distance_cm != -1:
            print(f"distance: {distance_cm} cm")
        else:
            print(f"Out of range")

        # Wait a second
        sleep(1)
