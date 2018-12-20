import numpy
from profilehooks import profile


class RollingMean:
    """This class perform a mean filter on an N-dimensional array."""

    def __init__(self, kernel_size: int):
        """Create a RollingMean element.

        Args:
            kernel_size (int): A scalar or an N-length list giving the size of
                the mean filter window in each dimension.
        """
        self.kernel_size = kernel_size

    @staticmethod
    def __running_mean(data, kernel_size):
        """
        Args:
            data:
            kernel_size:
        """
        cumsum = numpy.cumsum(numpy.insert(data, 0, 0))
        return (cumsum[kernel_size:] - cumsum[:-kernel_size]) / float(kernel_size)

    @profile
    def process(self, data: numpy.ndarray) -> numpy.ndarray:
        """Perform a mean filter on an N-dimensional array.

        Apply a mean filter to the input array using a local window-size
        given by `kernel_size`

        Args:
            data (numpy.ndarray): An array containing the data

        Returns:
            An array the same size as input containing the mean filtered result.
        """
        return RollingMean.__running_mean(data=data, kernel_size=self.kernel_size)
