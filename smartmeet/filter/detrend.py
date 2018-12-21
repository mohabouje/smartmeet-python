from scipy import signal
from numpy import ndarray
from profilehooks import profile

class Detrend:
    """This class removes the mean value or linear trend from a N-dimensional
    array, usually for FFT processing.

    The algorithm computes the least-squares fit of a straight line (or
    composite line for piecewise linear trends) to the data and subtracts the
    resulting function from the data.
    """

    def __init__(self, type: str = "linear"):
        """Create a Detrend element.

        If ``ftype == 'linear'`` (default), the result of a linear
        least-squares fit to `data` is subtracted from `data` . If
        ``ftype == 'constant'``, only the mean of `data` is subtracted.

        Args:
            type (str):
        """
        self.type = type

    @profile
    def process(self, data : ndarray) -> ndarray:
        """Removes the mean value or linear trend from a N-dimensional array.

        Args:
            data (ndarray): An array containing the data

        Returns:
            An array the same size as input containing the median filtered
            result.
        """
        return signal.detrend(data=data, type=self.type)
