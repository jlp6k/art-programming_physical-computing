from machine import Pin
from time import sleep, sleep_us, ticks_diff, ticks_us
from monitor import Monitor

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


def hcsr04_demo(trigger_gpio, echo_gpio):
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



class Button:
    def __init__(self, gpio, on_press=None, pressed_state=1, debounce_ms=20, pull=None):
        assert on_press is None or callable(on_press), f"{on_press} must be callable."

        self._debounce_ms = debounce_ms
        self._gpio_number = gpio
        self._gpio = Pin(gpio, mode=Pin.IN, pull=pull)
        self._on_press = on_press

        if callable(on_press):
            change = Pin.IRQ_RISING if pressed_state == 1 else Pin.IRQ_FALLING
            self._monitor = Monitor(self._gpio, on_change=self._handler, change=change, pull=pull)
        else:
            self._monitor = None

    def _handler(self, pin):
        self._on_press(self)

    def wait(self):
        # This code come from https://docs.micropython.org/en/latest/pyboard/tutorial/debounce.html
        # wait for pin to change value
        # it needs to be stable for a continuous 20ms
        cur_value = self.state
        active = 0
        while active < self._debounce_ms:
            if self.state != cur_value:
                active += 1
            else:
                active = 0
            sleep(0.001)

    @property
    def gpio(self):
        return self._gpio_number

    @property
    def state(self):
        return self._gpio.value()


def deinit(self):
        if self._monitor is not None:
            self._monitor.deinit()


if __name__ == "__main__":
    # The HC-SR04 needs two GPIOs:
    #     - the trigger initiates the measurement
    #     - the echo returns the measurement.
    # hcsr04_demo(20, 19)

    from machine import reset

    try:
        def do_something(button):
            print("Just Do It on button", button.gpio)

        button_1_gpio = 16
        button_2_gpio = 17

        button_1 = Button(button_1_gpio, pull=Pin.PULL_UP, on_press=do_something, pressed_state=0)
        button_2 = Button(button_2_gpio, pull=Pin.PULL_UP, on_press=do_something, pressed_state=0)

        while True:
            sleep(1)

    except KeyboardInterrupt:
        # Deactivate the buttons
        button_1.deinit()
        button_2.deinit()

