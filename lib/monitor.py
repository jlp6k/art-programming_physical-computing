from machine import Pin

class Monitor:
    def __init__(self, pin_or_number, on_change=None, change=None, pull=None):
        """This class helps to monitor a digital pin.

        It can be polled, the ``state`` property reflects the state of the pin.

        It can set a callback function. The function must have a single ``int``parameter which
        receives the state on of pin upon call (the ``state`` property is still available).
        In this use case, the ``on_change`` parameter will receive the callback function,
        the ``change`` parameter will be set to the condition that triggers the function call, and
        the ``pull`` parameter value will be used to configure the pull resistors of the pin.

        Note when the ``pin_or_number`` is a Pin, it is reconfigured as necessary.

        :param pin_or_number: ``int`` | ``machine.Pin``
        :param on_change: a callable with one mandatory parameter
        :param change: ``machine.Pin.IRQ_RISING`` or ``machine.Pin.IRQ_FALLING``
        :param pull: ``None``, ``machine.Pin.PULL_UP`` or ``machine.Pin.PULL_DOWN``
        """
        assert isinstance(pin_or_number, Pin) or (isinstance(pin_or_number, int) and 0 <= pin_or_number <= 29),\
            f"int [0..29] or Pin expected, {pin_or_number if isinstance(pin_or_number, int) else type(pin_or_number)} provided"

        assert on_change is None or (callable(on_change) and (change is None or (change & Pin.IRQ_RISING | Pin.IRQ_FALLING))),\
            f"on_change must be either None or a function and change must be Pin.IRQ_RISING | Pin.IRQ_FALLING or None"

        if isinstance(pin_or_number, int):
            # pin_or_number is a GPIO number
            # Configure it as an input
            pin_or_number = Pin(pin_or_number, mode=Pin.IN, pull=pull)
        else:
            # pin_or_number is a Pin instance.
            if pin_or_number.mode() != Pin.IN:
                pin_or_number.init(mode=Pin.IN, pull=pull)

        self._pin = pin_or_number

        if change is None:
            # call the on change function on rising and falling edges
            change = Pin.IRQ_RISING | Pin.IRQ_FALLING
        self._change = change

        if on_change:
            # on_change is a function -> prepare an interrupt handler
            self._on_change_function = on_change
            self._pin.irq(handler=self._handler, trigger=change)

    def _handler(self, pin):
        self._pin.irq(handler=None, trigger=0)
        self._on_change_function(pin.value())
        self._pin.irq(handler=self._handler, trigger=self._change)

    @property
    def state(self):
        return self._pin.value()

    def deinit(self):
        self._pin.irq(handler=None)


def monitor_demo(gpio):
    monitor = Monitor(gpio)

    # Use the LED to have a visual feedback
    led = Pin("LED", Pin.OUT)

    # the take_state() function will take care of the state of the pin
    def take_state(s):
        print(s)
        led.value(s)

    # Check the state of the monitored pin once a second during 20 seconds
    print("Monitoring by polling")
    for t in range(200):
        take_state(monitor.state)
        sleep(0.1)

    # Then use the interrupt style to do the same
    # Reinitialize the pin, but give a function to handle the changes as soon as they occur
    print("Monitoring by IRQ")
    monitor = Monitor(gpio, on_change=take_state)

    # Then wait for 20 seconds before exiting the program
    # If changes occur while waiting, they will be reported
    for t in range(20):
        sleep(1)

    # Deactivate monitoring by IRQ
    monitor.deinit()


if __name__ == "__main__":
    # Le programme est inclus dans un gestionnaire d'exception afin de s'arrêter proprement
    # s'il est interrompu.
    from machine import reset

    try:
        from time import sleep

        # Test using GPIO 9 / Pico pin 12 as the monitored input
        monitor_demo(9)

    except KeyboardInterrupt:
        # L'utilisateur a interrompu le programme, on réinitialise la carte.
        reset()
