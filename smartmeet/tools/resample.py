from scipy import signal
from numpy import ndarray

class Resample:
    """This class resamples N-dimensional array.

    The input signal is up-sampled by the factor `up` , a zero-phase low-pass
    FIR filter is applied, and then it is down-sampled by the factor `down` .
    The resulting sample rate is ``up / down`` times the original sample rate.
    Values beyond the boundary of the signal are assumed to be zero during the
    filtering step.
    """

    def __init__(self, up: int, down: int):
        """Create a Resample element.

        Args:
            up (int): The up-sampling factor.
            down (int): The down sampling factor.
        """
        self.up = up
        self.down = down

    def process(self, data: ndarray) -> ndarray:
        """Resample the input data using polyphase filtering.

        Args:
            data (ndarray): An array containing the data

        Returns:
            An array containing the resampled signal.
        """
        return signal.resample_poly(x=data, up=self.up, down=self.down)
