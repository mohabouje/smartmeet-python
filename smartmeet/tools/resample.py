from smartmeet.core.element import Element
from scipy import signal


class Resample(Element):
    """
    This class resamples N-dimensional array.

    The input signal is upsampled by the factor `up`, a zero-phase low-pass
    FIR filter is applied, and then it is downsampled by the factor `down`.
    The resulting sample rate is ``up / down`` times the original sample
    rate. Values beyond the boundary of the signal are assumed to be zero
    during the filtering step.

    """
    def __init__(self,  up: int, down: int, name: str = ""):
        """ Create a RollingMedian element.

        :param up: The upsampling factor.
        :param down: The down sampling factor.
        """
        super().__init__(name)
        self.up = up
        self.down = down

    def process(self, data, extra=None):
        """ Resample the input data using polyphase filtering.

        :param data: An array containing the data to be filtered
        :param extra: Dictionary storing any extra information previously computed.
        :return: An array containing the resampled signal.
        """
        return signal.resample_poly(x=data, up=self.up, down=self.down), extra
