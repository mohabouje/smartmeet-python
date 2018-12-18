import numpy
from smartmeet.core.filter import Filter


class RollingMean(Filter):
    """
    This class perform a mean filter on an N-dimensional array.
    """
    def __init__(self, kernel_size: int, name: str = ""):
        """ Create a RollingMean element.

        :param kernel_size: A scalar or an N-length list giving the size of the mean filter window in each dimension.
        :param name: Element's name also known as alias
        """
        super().__init__(name)
        self.kernel_size = kernel_size

    @staticmethod
    def __running_mean(x, N):
        cumsum = numpy.cumsum(numpy.insert(x, 0, 0))
        return (cumsum[N:] - cumsum[:-N]) / float(N)

    def process(self, data, extra=None):
        """ Perform a mean filter on an N-dimensional array.

        Apply a mean filter to the input array using a local window-size given by `kernel_size`

        :param data: An array containing the data
        :param extra: Dictionary storing any extra information previously computed.
        :return: An array the same size as input containing the mean filtered result.
        """
        return RollingMean.__running_mean(x=data, N=self.kernel_size), extra
