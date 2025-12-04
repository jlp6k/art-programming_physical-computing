from machine import Pin, reset
from time import sleep, sleep_us, sleep_ms, ticks_diff, ticks_us, ticks_ms
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
        self._pressed_state = pressed_state
        self._on_press = on_press

        if callable(on_press):
            change = Pin.IRQ_RISING if pressed_state == 1 else Pin.IRQ_FALLING
            self._monitor = Monitor(self._gpio, on_change=self._handler, change=change, pull=pull)
        else:
            self._monitor = None

    def _handler(self, state):
        self._debounce()
        self._on_press(self)

    def wait_press(self):
        # Wait for the button to be pressed
        while not self.is_pressed:
            pass

        self._debounce()

    def _debounce(self):
        last_state = self._pressed_state
        last_change = ticks_ms()

        while ticks_diff(ticks_ms(), last_change) > self._debounce_ms:
            if self.state != last_state:
                last_state = self.state
                last_change = ticks_ms()
            sleep_ms(1)

    @property
    def gpio(self):
        return self._gpio_number

    @property
    def state(self):
        return self._gpio.value()

    @property
    def is_pressed(self):
        return self._gpio.value() == self._pressed_state

    def deinit(self):
        if self._monitor is not None:
            self._monitor.deinit()


def button_demo(button_1_gpio, button_2_gpio):
    def do_something(button):
        print("Just Do It on button", button.gpio)

    try:
        button_1 = Button(button_1_gpio, pull=Pin.PULL_UP, on_press=do_something, pressed_state=0, debounce_ms=50)
        button_2 = Button(button_2_gpio, pull=Pin.PULL_UP, pressed_state=0)

        while True:
            button_2.wait_press()
            print("wait_press() exited")
            sleep(0.1)

    except KeyboardInterrupt:
        # Deactivate the buttons
        button_1.deinit()


if __name__ == "__main__":
    # The HC-SR04 needs two GPIOs:
    #     - the trigger initiates the measurement
    #     - the echo returns the measurement.
    # hcsr04_demo(20, 19)


    # The button demo needs 2 GPIO
    #     - first button, handled by interruption
    #     - second button, handled in a loop
    button_demo(16, 17)



