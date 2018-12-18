from smartmeet.core.element import Element
from scipy import signal


class Detrend(Element):
    """
    This class removes the mean value or linear trend from a N-dimensional array, usually for FFT processing.

    The algorithm computes the least-squares fit of a straight line (or composite line for piecewise linear trends)
    to the data and subtracts the resulting function from the data.
    """
    def __init__(self, ftype: str = "linear", name: str = ""):
        """ Create a Detrend element.

        :param ftype: The ftype of detrending {'linear', 'constant'}.
        If ``ftype == 'linear'`` (default), the result of a linear least-squares fit to `data` is subtracted from `data`.
        If ``ftype == 'constant'``, only the mean of `data` is subtracted.
        :param name: Element's name also known as alias
        """
        super().__init__(name)
        self.ftype = ftype

    def process(self, data, extra=None):
        """ Removes the mean value or linear trend from a N-dimensional array.

        :param data: An array containing the data
        :param extra: Dictionary storing any extra information previously computed.
        :return: An array the same size as input containing the median filtered result.
        """
        return signal.detrend(data=data, axis=0, type=self.ftype), extra
