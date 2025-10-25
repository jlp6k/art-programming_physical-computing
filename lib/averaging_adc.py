from array import array

import machine

class AveragingADC:
    """The Averaging_ADC class computes a running average over a window of size ADC values."""

    def __init__(self, pin_or_adc_number, average_size=16):
        """The initialization method of the Averaging_ADC class expects a average_size parameter used
        to set the maximum size of the window over the incoming values.
        """
        self._raw_adc = machine.ADC(pin_or_adc_number)

        assert average_size > 0, f"size must be greater than 0 (got {average_size})."

        self._size = average_size
        # The ADC values are unsigned 16 bits integers, hence the 'I' below.
        # Doing this instead of using a plain list may save few bytes of memory.
        self._buffer = array('I')
        self._sum = 0
        self._oldest_value_index = 0

    def raw_u16(self):
        """The raw_u16(value) method reads the ADC and adds the value to the average computation, then it
        return the value (not the average).

        If the number of averaged values exceeds average_size, the oldest value is removed
        from the average computation.
        """
        value = self._raw_adc.read_u16()

        if len(self._buffer) < self._size:
            # The buffer grows up to self._size values
            self._buffer.append(value)
        else:
            oldest_value = self._buffer[self._oldest_value_index]
            self._buffer[self._oldest_value_index] = value
            self._sum -= oldest_value
            self._oldest_value_index = (self._oldest_value_index + 1) % self._size

        self._sum += value

        return value

    def read(self):
        """The read() method returns the average of the last size (at most) values read from the ADC.
        """
        self.raw_u16()

        return self._sum / len(self._buffer)

    def read_u16(self):
        """The read_u16() method returns the value returned by the read() method cast into an int.
        It is provided for compatibility with the ADC read_u16() method as it has the same signature.
        """
        return int(self.read())
    
    def read_unit(self):
        return self.read() / 65535

    @staticmethod
    def _value_to_volts(value):
        return 3.3 * value / 65535

    def raw_volts(self):
        """The raw_volts() method return the input voltage.
        """
        return self._value_to_volts(self.raw_u16())

    def volts(self):
        """The volts() method return the averaged input voltage.
        """
        return self._value_to_volts(self.read())


if __name__ == "__main__":
    from time import sleep

    # On crée un objet de classe AveragingADC.
    adc = AveragingADC(0)

    # Dans une boucle infinie...
    while True:
        # On affiche les résultats de mesures sur la console (avec 3 décimales pour les volts).
        print(f"{adc.raw_u16()} {adc.raw_volts():5.3f} V\t{adc.read():7.1f} {adc.volts():5.3f} V")
        # On attend 1/4 de seconde avant de recommencer
        sleep(1 / 4)
