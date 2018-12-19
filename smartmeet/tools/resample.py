from scipy import signal

from smartmeet.core.filter import Filter


class Resample(Filter):
    """This class resamples N-dimensional array.

    The input signal is up-sampled by the factor `up` , a zero-phase low-pass
    FIR filter is applied, and then it is down-sampled by the factor `down` .
    The resulting sample rate is ``up / down`` times the original sample rate.
    Values beyond the boundary of the signal are assumed to be zero during the
    filtering step.
    """

    def __init__(self, up: int, down: int, name: str = ""):
        """Create a Resample element.

        Args:
            up (int): The up-sampling factor.
            down (int): The down sampling factor.
            name (str):
        """
        super().__init__(name)
        self.up = up
        self.down = down

    def process(self, data, extra=None):
        """Resample the input data using polyphase filtering.

        Args:
            data: An array containing the data
            extra: Dictionary storing any extra information previously computed.

        Returns:
            An array containing the resampled signal.
        """
        return signal.resample_poly(x=data, up=self.up, down=self.down), extra
