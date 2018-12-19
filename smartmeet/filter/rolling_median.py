from scipy import signal

from smartmeet.core.filter import Filter


class RollingMedian(Filter):
    """
    This class perform a median filter on an N-dimensional array.
    """

    def __init__(self, kernel_size: int, name: str = ""):
        """ Create a RollingMedian element.

        :param kernel_size: A scalar or an N-length list giving the size of the median filter window in each dimension.
        :param name: Element's name also known as alias
        """
        super().__init__(name)
        self.kernel_size = kernel_size

    def process(self, data, extra=None):
        """ Perform a median filter on an N-dimensional array.

        Apply a median filter to the input array using a local window-size given by `kernel_size`

        :param data: An array containing the data
        :param extra: Dictionary storing any extra information previously computed.
        :return: An array the same size as input containing the median filtered result.
        """
        return signal.medfilt(data, kernel_size=self.kernel_size), extra
