from scipy import signal
from numpy import ndarray
from profilehooks import profile

class RollingMedian:
    """This class perform a median filter on an N-dimensional array."""

    def __init__(self, kernel_size: int):
        """Create a RollingMedian element.

        Args:
            kernel_size (int): A scalar or an N-length list giving the size of
                the median filter window in each dimension.
        """
        self.kernel_size = kernel_size

    @profile
    def process(self, data : ndarray) -> ndarray:
        """Perform a median filter on an N-dimensional array.

        Apply a median filter to the input array using a local window-size
        given by `kernel_size`

        Args:
            data (ndarray): An array containing the data

        Returns:
            An array the same size as input containing the median filtered
            result.
        """
        return signal.medfilt(data, kernel_size=self.kernel_size)
